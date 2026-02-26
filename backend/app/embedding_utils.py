# backend/app/embedding_utils.py
import torch
from transformers import BertModel, BertTokenizer
import numpy as np

class BERTEmbedder:
    """提取 BERT Embeddings 做語義相似度計算"""
    
    def __init__(self, model_name='bert-base-multilingual-cased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def get_embeddings(self, text: str) -> np.ndarray:
        """提取文本的 BERT embeddings"""
        
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=64
        ).to(self.device)
        
        # 取得 BERT 的 hidden states
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 使用 [CLS] token 的 embedding (第一個 token)
        cls_embedding = outputs.last_hidden_state[0, 0, :].cpu().numpy()
        # Shape: (768,) - 768 維向量
        
        return cls_embedding
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """計算兩個文本的語義相似度"""
        
        emb1 = self.get_embeddings(text1)
        emb2 = self.get_embeddings(text2)
        
        # 計算余弦相似度
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(similarity)
    
    def find_most_similar(self, query: str, candidates: list[str]) -> tuple[str, float]:
        """從候選列表中找最相似的"""
        
        query_emb = self.get_embeddings(query)
        
        best_match = None
        best_score = -1
        
        for candidate in candidates:
            cand_emb = self.get_embeddings(candidate)
            similarity = np.dot(query_emb, cand_emb) / \
                        (np.linalg.norm(query_emb) * np.linalg.norm(cand_emb))
            
            if similarity > best_score:
                best_score = similarity
                best_match = candidate
        
        return best_match, best_score