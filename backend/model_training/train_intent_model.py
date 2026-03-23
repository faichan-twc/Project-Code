# backend/model_training/train_intent_model.py
import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import (
    BertTokenizer, 
    BertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np
from tqdm import tqdm


class Tee:
    """Write output to multiple streams (console + report file)."""
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)
            stream.flush()

    def flush(self):
        for stream in self.streams:
            stream.flush()

class IntentDataset(Dataset):
    """意圖分類數據集"""
    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

class IntentClassifierTrainer:
    def __init__(self, model_name='bert-base-multilingual-cased'):
        """
        ✅ 針對中英混合場景優化
        """
        self.model_name = model_name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🖥️  使用設備: {self.device}")
        print(f"🤖 模型: {model_name}")
        print(f"🌍 語言支持: 中文 + 英文 + 混合")
    
    def load_data(self, json_path='intent_training_data_enhanced.json'):
        """加載增強的訓練數據"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 創建標籤映射
        unique_labels = sorted(list(set(item['label'] for item in data)))
        self.label2id = {label: idx for idx, label in enumerate(unique_labels)}
        self.id2label = {idx: label for label, idx in self.label2id.items()}
        
        print(f"📋 標籤映射: {self.label2id}")
        
        # 準備數據
        texts = [item['text'] for item in data]
        labels = [self.label2id[item['label']] for item in data]
        
        return texts, labels
    
    def train(self, epochs=15, batch_size=32, learning_rate=2e-5, output_dir='../models/intent_classifier'):
        """訓練模型"""
        # 加載數據
        texts, labels = self.load_data()
        
        # 分割訓練集和驗證集
        train_texts, val_texts, train_labels, val_labels = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"📊 訓練集: {len(train_texts)} 樣本")
        print(f"📊 驗證集: {len(val_texts)} 樣本")
        
        # 初始化 tokenizer 和模型
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(self.label2id)
        ).to(self.device)
        
        # 創建數據集
        train_dataset = IntentDataset(train_texts, train_labels, self.tokenizer)
        val_dataset = IntentDataset(val_texts, val_labels, self.tokenizer)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # 優化器和學習率調度器
        optimizer = AdamW(self.model.parameters(), lr=learning_rate)
        total_steps = len(train_loader) * epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(0.1 * total_steps),
            num_training_steps=total_steps
        )
        
        # 訓練循環
        best_val_acc = 0
        for epoch in range(epochs):
            print(f"\n{'='*50}")
            print(f"🔄 Epoch {epoch + 1}/{epochs}")
            print(f"{'='*50}")
            
            # 訓練階段
            self.model.train()
            train_loss = 0
            train_correct = 0
            train_total = 0
            
            progress_bar = tqdm(train_loader, desc="Training")
            for batch in progress_bar:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['label'].to(self.device)
                
                optimizer.zero_grad()
                
                outputs = self.model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                logits = outputs.logits
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                
                train_loss += loss.item()
                predictions = torch.argmax(logits, dim=1)
                train_correct += (predictions == labels).sum().item()
                train_total += labels.size(0)
                
                progress_bar.set_postfix({
                    'loss': f'{loss.item():.4f}',
                    'acc': f'{train_correct/train_total:.4f}'
                })
            
            avg_train_loss = train_loss / len(train_loader)
            train_acc = train_correct / train_total
            
            # 驗證階段
            self.model.eval()
            val_loss = 0
            val_correct = 0
            val_total = 0
            all_preds = []
            all_labels = []
            
            with torch.no_grad():
                for batch in tqdm(val_loader, desc="Validation"):
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['label'].to(self.device)
                    
                    outputs = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=labels
                    )
                    
                    loss = outputs.loss
                    logits = outputs.logits
                    
                    val_loss += loss.item()
                    predictions = torch.argmax(logits, dim=1)
                    val_correct += (predictions == labels).sum().item()
                    val_total += labels.size(0)
                    
                    all_preds.extend(predictions.cpu().numpy())
                    all_labels.extend(labels.cpu().numpy())
            
            avg_val_loss = val_loss / len(val_loader)
            val_acc = val_correct / val_total
            
            print(f"\n📈 訓練損失: {avg_train_loss:.4f} | 訓練準確率: {train_acc:.4f}")
            print(f"📉 驗證損失: {avg_val_loss:.4f} | 驗證準確率: {val_acc:.4f}")
            
            # 保存最佳模型
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                print(f"✅ 找到更好的模型！驗證準確率: {val_acc:.4f}")
                self.save_model(output_dir)
        
        # 最終評估
        print(f"\n{'='*50}")
        print("📊 最終評估報告")
        print(f"{'='*50}")
        print(classification_report(
            all_labels, 
            all_preds,
            target_names=[self.id2label[i] for i in range(len(self.id2label))]
        ))
        
        return best_val_acc
    
    def save_model(self, output_dir):
        """保存模型"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存模型和 tokenizer
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        # 保存標籤映射
        label_map_path = os.path.join(output_dir, 'label_map.json')
        with open(label_map_path, 'w', encoding='utf-8') as f:
            json.dump({
                'label2id': self.label2id,
                'id2label': self.id2label
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 模型已保存到: {output_dir}")

if __name__ == "__main__":
    output_dir = '../models/intent_classifier'
    report_path = Path(output_dir) / f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    original_stdout = sys.stdout
    original_stderr = sys.stderr

    with open(report_path, 'w', encoding='utf-8') as report_file:
        tee_stream = Tee(original_stdout, report_file)
        try:
            # tqdm 預設走 stderr，因此同時重定向 stdout/stderr 才能完整保留訓練輸出
            sys.stdout = tee_stream
            sys.stderr = tee_stream

            # 使用多語言模型
            trainer = IntentClassifierTrainer(
                model_name='bert-base-multilingual-cased'  # ⭐
            )

            best_acc = trainer.train(
                epochs=15,        # ⬆️ 增加訓練輪數
                batch_size=32,    # ⬆️ 較大的批次
                learning_rate=2e-5,
                output_dir=output_dir
            )
            print(f"\n🎉 訓練完成！最佳驗證準確率: {best_acc:.4f}")
            print(f"📝 訓練報告檔案: {report_path.resolve()}")
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    print(f"📝 訓練報告已輸出到: {report_path.resolve()}")