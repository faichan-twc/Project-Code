# NLP Processing with Chinese and English support
import re
from typing import Optional, List, Dict, Tuple
from app.game_data import GameData
from app.models import CommandIntent, AttackStyle, Sentiment
from app.embedding_utils import BERTEmbedder

# 添加 BERT 模型導入
try:
    import torch
    from transformers import BertTokenizer, BertForSequenceClassification
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False

class ChineseNLP:
    """Enhanced NLP for Chinese and English command parsing with advanced features"""
    
    def __init__(self, game_data: GameData = None, use_bert: bool = True):
        self.data = game_data if game_data else GameData()
        self.use_bert = use_bert and BERT_AVAILABLE
        self.embedder = BERTEmbedder() 
        
        # 加載 BERT 模型
        if self.use_bert:
            self._load_bert_model()
        
        # 功能1：身體部位詞彙
        self.body_parts = {
            "頭": [
                "head", "heads", "頭", "頭部", "頭顱", "腦袋", "腦袋瓜", 
                "skull", "cranium", "頭部核心", "head core"
            ],
            "眼睛": [
                "eye", "eyes", "眼", "雙眼", "眼睛", "眼球", "瞳", 
                "瞳孔", "目"
            ],
            "腿": [
                "leg", "legs", "腿", "腿部", "下肢", "大腿", "小腿", 
                "hind leg", "hind legs"
            ],
            "尾巴": [
                "tail", "tails", "尾", "尾巴", "尾端"
            ],
            "身體": [
                "body", "bodies", "身體", "軀幹", "身軀", "Torso"
            ],
            "腹部": [
                "belly", "stomach", "abdomen", "腹部", "肚子", "肚皮", 
                "胃部"
            ],
            "手臂": [
                "arm", "arms", "手", "手臂", "臂", "前臂", "上臂", 
                "hand", "hands"
            ],
            "翅膀": [
                "wing", "wings", "翼", "羽翼", "翅", "鳥翼", 
                "翼膀", "羽"
            ],
            "鉗子": [
                "pincer", "pincers", "claw", "claws", "鉗", "鉗子", 
                "螯", "夾子"
            ],
            "王冠": [
                "crown", "crowns", "冠", "王冠", "皇冠"
            ],
            "權杖": [
                "scepter", "sceptre", "杖", "權杖", "魔杖", "杖棒"
            ],
            "胸甲": [
                "breastplate", "chestplate", "armor chest", 
                "chest", "胸", "胸甲", "胸部護甲"
            ],
            "骨骼": [
                "skeleton", "bone", "bones", "骨", "骨頭", 
                "骸骨", "骨骼"
            ],
            "核心": [
                "core", "核心", "心臟", "heart", "heart core", 
                "energy core", "power core"
            ],
            "護甲": [
                "armor", "armour", "armor piece", 
                "甲", "護甲", "裝甲"
            ],
            "石劍": [
                "sword", "stone sword", "劍", "石劍", "刀劍", "寶劍",
                "blade", "石刃"
            ]
        }

        
        # 功能1：攻擊方式關鍵詞
        self.attack_modifiers = {
            AttackStyle.QUICK: [
                "快速", "迅速", "敏捷", "急速", "飛快", "極快", "瞬間", "電光石火",
                "快攻", "馬上", "立刻", "瞬發", "迅捷", "閃動", "敏捷地",
                "quickly", "fast", "swift", "rapid", "speedy", "instantly",
                "in a flash", "at once", "with haste", "in quick succession"
            ],
            AttackStyle.HEAVY: [
                "用力", "全力", "重擊", "猛擊", "猛烈", "強力", "大力", "沉重", "狠砸",
                "暴力", "使出全力", "全力以赴", "強攻",
                "heavily", "hard", "powerful", "forceful", "with full strength",
                "mighty", "overwhelming", "brutal strike", "smash"
            ],
            AttackStyle.PRECISE: [
                "精準", "準確", "瞄準", "細緻", "細心", "精密", "點刺", "直擊要害",
                "命中要點", "精準控制", "不中不偏",
                "precisely", "accurately", "aim", "targeted", "exact",
                "pinpoint", "with precision", "carefully aimed", "on point"
            ],
            AttackStyle.DEFENSIVE: [
                "小心", "謹慎", "防守", "保護", "格擋", "防禦性", "穩固", "退守", "迴避",
                "戒備", "抵禦", "穩健", "防備",
                "carefully", "defensive", "cautious", "guarded", "protective",
                "on guard", "shielding", "playing safe", "holding back"
            ]
        }
        
        # 功能2：情感關鍵詞
        self.sentiment_keywords = {
            Sentiment.FRIENDLY: [
                "請", "謝謝", "幫", "友善", "好", "拜託", "辛苦了", "麻煩你", 
                "感謝", "謝啦", "不好意思", "有勞了", "很棒", "太好了",
                "請問", "可不可以", "麻煩幫忙", "真貼心", "感激",

                "please", "thanks", "thank you", "thx", "help", "friendly",
                "appreciate", "kind", "nice", "could you", "would you please",
                "sorry to trouble you", "much appreciated", "so kind of you"
            ],
            Sentiment.HOSTILE: [
                "滾", "走開", "討厭", "去死", "閉嘴", "垃圾", "廢物", "娘炮",
                "白癡", "蠢貨", "煩", "滾開", "臭", "噁心", "崩潰吧", "我受夠了",
                "別惹我", "給我滾", "去你的", "死開",

                "get lost", "hate", "die", "shut up", "stupid", "idiot",
                "trash", "useless", "disgusting", "annoying", "screw you",
                "back off", "piss off", "i hate you", "go away"
            ],
            Sentiment.INTIMIDATING: [
                "投降", "認輸", "放棄", "受傷", "害怕", "小心點", "別動", "我警告你",
                "別逼我出手", "你完了", "最好乖乖的", "危險", "不要輕舉妄動",
                "我不想再說第二次", "別亂來", "下馬威", "威脅", "恐嚇",

                "surrender", "give up", "afraid", "fear", "watch out",
                "don’t move", "i warn you", "you’re finished", "this is a warning",
                "don’t push it", "danger", "intimidate", "threaten", "back down"
            ]
        }
        
        # 功能4：問題類型關鍵詞
        self.question_patterns = {
            "search": [
                "有什麼", "有沒有", "看到", "發現", "找到", "有", 
                "查", "看看", "看一下", "找一下", "找找", "搜尋", "查一下",
                "知道哪些", "有哪些", "列出", "清單", "推薦",
                "what", "any", "find", "is there", "list", "lookup", "search for",
                "show me", "anything about", "what are", "what is available"
            ],
            "origin": [
                "從哪", "哪裡來", "來源", "出自", "起源", "來自", 
                "哪裡發生", "哪邊", "根源", "源頭",
                "where from", "origin", "where", "come from", "source of",
                "where does it start", "where is it from"
            ],
            "method": [
                "怎麼", "如何", "怎樣", "怎麼辦", "要怎麼", "能不能教我",
                "步驟", "方式", "怎麼做", "應該怎麼", "教我一下", "方法",
                "how", "what to do", "how do i", "how can i", 
                "how to", "way to", "method", "steps", "procedure", 
                "what should i do", "guide me"
            ],
            "reason": [
                "為什麼", "為何", "原因", "怎會", "怎麼會", "理由", 
                "為什麼會這樣", "為什麼會發生", "怎麼造成的", "為什麼會有",
                "why", "reason", "how come", "why is it", 
                "what causes", "what's the reason", "why does this happen"
            ]
        }

    def normalize(self, text: str) -> str:
        """輕量級預處理（僅用於規則方法）"""
        
        text = text.strip()
        text = text.replace("！", "!").replace("？", "?")
        text = " ".join(text.split())
        text = text.lower()

        return text

    def has_any(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords (with word boundary matching)"""
        import re
        
        # Split text into words for exact word matching
        text_words = text.split()
        
        # First try exact word match (case-insensitive)
        text_lower = text.lower()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Use word boundary regex for English words, direct match for Chinese
            if len(keyword) > 1 and keyword.isascii():
                # English word - use word boundary
                pattern = r'\b' + re.escape(keyword_lower) + r'\b'
                if re.search(pattern, text_lower):
                    return True
            else:
                # Chinese or single char - use substring match
                if keyword_lower in text_lower:
                    return True
        
        # If no exact match, try fuzzy matching on individual words
        for word in text_words:
            for keyword in keywords:
                # Only fuzzy match English words (length > 3) to avoid false positives
                if len(word) > 3 and len(keyword) > 3:
                    from difflib import SequenceMatcher
                    similarity = SequenceMatcher(None, word, keyword).ratio()
                    if similarity >= 0.85:  # Slightly higher threshold for intent detection
                        return True
        
        return False
        
        # ========== 舊方法保持兼容（內部調用新方法）==========
    def extract_enemy(self, text: str) -> Optional[str]:
        """提取敵人（兼容舊接口）"""
        return self._extract_entity(text, "enemy", optional=False)
    
    def extract_weapon(self, text: str) -> Optional[str]:
        """提取武器（兼容舊接口）"""
        return self._extract_entity(text, "weapon", optional=True)
    
    def extract_body_part(self, text: str) -> Optional[str]:
        """提取身體部位（兼容舊接口）"""
        return self._extract_entity(text, "body_part", optional=True)
    

    def extract_attack_style(self, text: str) -> AttackStyle:
        """從文本中提取攻擊方式"""
        for style, keywords in self.attack_modifiers.items():
            if self.has_any(text, keywords):
                return style
        return AttackStyle.NORMAL
    
    def extract_modifiers(self, text: str) -> List[str]:
        """提取動作修飾詞"""
        modifiers = []
        all_modifiers = ["繞到", "側面", "背後", "後退", "前進", "跳躍", 
                        "flank", "side", "behind", "retreat", "advance", "jump"]
        for mod in all_modifiers:
            if mod in text:
                modifiers.append(mod)
        return modifiers
    
    # ========== 功能2：情感分析 ==========
    def detect_sentiment(self, text: str) -> Sentiment:
        """檢測文本情感"""
        scores = {sentiment: 0 for sentiment in Sentiment}
        
        for sentiment, keywords in self.sentiment_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[sentiment] += 1
        
        # 返回得分最高的情感，但至少要有一個關鍵字匹配
        max_sentiment = max(scores, key=scores.get)
        if scores[max_sentiment] > 0:
            return max_sentiment
        return Sentiment.NEUTRAL
    
    # ========== 功能4：環境互動問答 ==========
    def detect_question_type(self, text: str) -> Optional[str]:
        """檢測問題類型"""
        #if "？" in text or "?" in text or any(q in text for q in ["什麼", "哪", "怎麼", "為什麼", "what", "where", "how", "why"]):
        for q_type, keywords in self.question_patterns.items():
            if self.has_any(text, keywords):
                return q_type
        return None

    
    def _load_bert_model(self):
        """加載預訓練的 BERT 意圖分類模型"""
        try:
            import json
            import os

            # Get the backend directory (parent of app/)
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(backend_dir, 'models', 'intent_classifier')
            
            print(f"🔍 Looking for model at: {model_path}")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model directory not found at {model_path}")
            
            print("🤖 正在加載 BERT 意圖分類模型...")
            self.bert_tokenizer = BertTokenizer.from_pretrained(model_path)
            self.bert_model = BertForSequenceClassification.from_pretrained(model_path)
            self.bert_model.eval()
            
            # 加載標籤映射
            with open(f"{model_path}/label_map.json", 'r', encoding='utf-8') as f:
                label_map = json.load(f)
                self.bert_id2label = {int(k): v for k, v in label_map['id2label'].items()}
            
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.bert_model.to(self.device)
            
            print(f"✅ BERT 模型已加載 (設備: {self.device})")
            print(f"📋 支持的意圖: {list(set(self.bert_id2label.values()))}")
            
        except Exception as e:
            print(f"⚠️  BERT 模型加載失敗: {e}")
            print("   將使用傳統規則方法")
            self.use_bert = False
    
   
    def predict_intent_bert(self, text: str) -> Tuple[str, float]:
        """使用 BERT 模型預測意圖"""
        if not self.use_bert:
            return None, 0.0
        
        # Tokenize
        inputs = self.bert_tokenizer(
            text,
            add_special_tokens=True,
            max_length=64,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        ).to(self.device)
        
        # 預測
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            confidence, predicted_id = torch.max(probabilities, dim=1)
        
        intent = self.bert_id2label[predicted_id.item()]
        confidence_score = confidence.item()
        
        return intent, confidence_score
    

    def parse(self, input_text: str) -> CommandIntent:
        """解析指令 - 優先使用 BERT，低信心時使用規則方法"""

        text = self.normalize(input_text)

        # 先檢測情感（用於所有指令）
        sentiment = self.detect_sentiment(text)
        
        # 方法 1: 使用 BERT 模型預測
        if self.use_bert:
            bert_intent, confidence = self.predict_intent_bert(text)
            
            print(f"🤖 BERT 預測: {bert_intent} (信心度: {confidence:.2%})")
            
            # 如果信心度高，使用 BERT 結果
            if confidence >= 0.75:
                return self._create_intent_from_bert(
                    bert_intent, input_text, text, sentiment
                )
            else:
                print(f"⚠️  BERT 信心度較低 ({confidence:.2%})，使用規則方法")
        
        # 方法 2: 傳統規則方法 (後備)
        return self._parse_by_rules(input_text, text, sentiment)
    
    def _create_intent_from_bert(self, bert_intent: str, 
                                 input_text: str, normalized_text: str,
                                 sentiment: Sentiment) -> CommandIntent:
        """根據 BERT 預測結果創建 CommandIntent（使用統一實體提取）"""
        
        # 🎯 使用新的統一實體提取方法
        entities = self.extract_entities(normalized_text, bert_intent)
        
        if bert_intent == "ATTACK":
            return CommandIntent(
                intent="ATTACK",
                target=entities["target"],
                weapon=entities["weapon"],
                body_part=entities["body_part"],
                attack_style=entities["attack_style"],
                sentiment=sentiment,
                modifiers=entities["modifiers"]
            )
        
        elif bert_intent == "MOVE":
            return CommandIntent(
                intent="MOVE",
                location=entities["location"],
                sentiment=sentiment
            )
        
        elif bert_intent == "USE":
            return CommandIntent(
                intent="USE",
                item=entities["item"],
                target=entities.get("target"),
                sentiment=sentiment
            )
        
        elif bert_intent == "PICK":
            return CommandIntent(
                intent="PICK",
                item=entities["item"],
                sentiment=sentiment
            )
        
        elif bert_intent == "OBSERVE":
            return CommandIntent(
                intent="OBSERVE",
                object=entities["object"],
                sentiment=sentiment
            )
        
        elif bert_intent == "TALK" or sentiment == "intimidating":
            return CommandIntent(
                intent="TALK",
                target=entities["target"],
                sentiment=sentiment,
                raw=input_text
            )
        
        elif bert_intent in ["DEFEND", "REST", "ESCAPE"]:
            return CommandIntent(
                intent=bert_intent,
                sentiment=sentiment
            )
        elif bert_intent == "QUESTION":
            question_type = self.detect_question_type(normalized_text)
            if question_type:
                #target = self.extract_question_target(normalized_text)
                return CommandIntent(
                    intent="QUESTION",
                    object=entities["object"],
                    question_type=question_type,
                    sentiment=sentiment,
                    raw=input_text
                )
        else:
            return CommandIntent(
                intent="UNKNOWN",
                raw=input_text,
                sentiment=sentiment
            )

    def _parse_by_rules(self, input_text: str, normalized_text: str, 
                       sentiment: Sentiment) -> CommandIntent:
        """使用傳統規則方法解析 (保留原有邏輯)"""
        text = normalized_text
        
        # 檢測是否為問題（功能4：環境互動）
        question_type = self.detect_question_type(text)
        if question_type:
            entities = self.extract_entities(text, "QUESTION")
            return CommandIntent(
                intent="QUESTION",
                object=entities["object"],
                question_type=question_type,
                sentiment=sentiment,
                raw=input_text
            )

        # Defend intent
        if self.has_any(text, self.data.synonyms["defend"]):
            return CommandIntent(
                intent="DEFEND",
                sentiment=sentiment
            )
        
        # Attack intent with advanced parsing（功能1+3）
        if self.has_any(text, self.data.synonyms["attack"]):
            entities = self.extract_entities(text, "ATTACK")
            return CommandIntent(
                intent="ATTACK",
                target=entities["target"],
                weapon=entities["weapon"],
                body_part=entities["body_part"],
                attack_style=entities["attack_style"],
                sentiment=sentiment,
                modifiers=entities["modifiers"]
            )

        # Observe intent
        if self.has_any(text, self.data.synonyms["observe"]):
            entities = self.extract_entities(text, "OBSERVE")
            return CommandIntent(
                intent="OBSERVE",
                object=entities["object"],
                sentiment=sentiment
            )
        
        # Talk intent with sentiment（功能2）- 包括威嚇
        if self.has_any(text, self.data.synonyms["talk"]) or sentiment == "intimidating":
           #target = self.pick_slot_fuzzy(text, ["神秘人", "旅人", "守衛"]) or "未知"
           return CommandIntent(intent="TALK", sentiment=sentiment, raw=input_text)

        # Use intent with modifiers（功能3）
        if self.has_any(text, self.data.synonyms["use"]):
            entities = self.extract_entities(text, "USE")
            return CommandIntent(
                intent="USE",
                item=entities["item"],
                target=entities.get("target"),
                sentiment=sentiment
            )
        
        # Move intent - Check BEFORE rest to avoid "rest area" being matched as "rest"
        if self.has_any(text, self.data.synonyms["move"]):
            entities = self.extract_entities(text, "MOVE")
            return CommandIntent(
                intent="MOVE",
                location=entities["location"],
                sentiment=sentiment
            )
        
        # Rest intent
        if self.has_any(text, self.data.synonyms["rest"]):
            return CommandIntent(
                intent="REST",
                sentiment=sentiment
            )
        
        # Escape intent with sentiment（功能2：可能是投降）
        if self.has_any(text, self.data.synonyms["escape"]):
            return CommandIntent(
                intent="ESCAPE",
                sentiment=sentiment
            )
        
        # Pick intent
        if self.has_any(text, self.data.synonyms["pick"]):
            entities = self.extract_entities(text, "PICK")
            return CommandIntent(
                intent="PICK",
                item=entities["item"],
                sentiment=sentiment
            )

        # Unknown intent
        return CommandIntent(intent="UNKNOWN", raw=input_text, sentiment=sentiment)


    
    # ========== 核心方法：統一實體提取接口 ==========
    def extract_entities(self, text: str, intent: str) -> Dict[str, any]:
        """
        根據 intent 提取相關實體
        
        Args:
            text: 原始命令文本
            intent: BERT 預測的意圖（ATTACK, MOVE, USE 等）
        
        Returns:
            實體字典，包含該 intent 需要的所有實體
        """
        text_lower = text.lower()
        entities = {}
        
        # 根據不同 intent 提取不同實體
        if intent == "ATTACK":
            entities = {
                "target": self._extract_entity(text, "enemy"),
                "weapon": self._extract_entity(text, "weapon"),
                "body_part": self._extract_entity(text, "body_part"),
                "attack_style": self._extract_attack_style(text),
                "modifiers": self._extract_modifiers(text)
            }
        
        elif intent == "MOVE":
            entities = {
                "location": self._extract_entity(text, "location")
            }
        
        elif intent == "USE":
            entities = {
                "item": self._extract_entity(text, "item"),
                "target": self._extract_entity(text, "enemy", optional=True)
            }
        
        elif intent == "PICK":
            entities = {
                "item": self._extract_entity(text, "item")
            }
        
        elif intent == "OBSERVE":
            # 觀察可以針對敵人、物品、線索或四周
            clue = None
            enemy = None
            item = None

            clue = self._extract_entity(text, "clue", optional=True)
            if clue:
                target = clue
            else:
                enemy = self._extract_entity(text, "enemy", optional=True)
                if enemy:
                    target = enemy
                else:
                    item = self._extract_entity(text, "item", optional=True)
                    if item:
                        target = item
                    else:
                        target = "四周"
            # ✅ 智能選擇：優先級 clue > item > enemy > 四周
            print(f"🔍 [OBSERVE] 提取結果: enemy={enemy}, item={item}, clue={clue}")

            entities = {"object": target}
        elif intent == "QUESTION":

            clue = self._extract_entity(text, "clue", optional=True)

            # 優先選擇最具體的目標
            target = clue or "四周"
            
            entities = {"object": target}
        
        elif intent == "TALK":
            entities = {
                "target": self._extract_entity(text, "npc", optional=True) or "未知"
            }
        
        return entities
    
    # ========== 統一實體提取核心（三層策略）==========
    def _extract_entity(self, text: str, entity_type: str, optional: bool = False) -> Optional[str]:
        """
        通用實體提取方法（三層策略）
        
        策略優先級：
        1. 精確匹配（中文名稱）
        2. 字典映射（英文名稱）
        3. Embeddings 語義匹配（最後手段）
        
        Args:
            text: 命令文本
            entity_type: 實體類型 (enemy, weapon, item, location, body_part, npc, clue)
            optional: 是否可選（True = 未找到返回 None，False = 返回默認值）
        
        Returns:
            提取到的實體名稱（中文）
        """
        # 獲取該類型的候選列表
        candidates = self._get_candidates(entity_type)
        print(f"\n🔍 提取實體: '{entity_type}' 從文本: '{text}'，候選詞: {candidates}")
        if not candidates:
            return None
        
        text_lower = text.lower()
        
        # ========== 策略 1: 精確匹配 ==========
        if entity_type == "body_part":
            # 特殊處理：匹配同義詞後返回中文名稱
            for cn_name, synonyms in self.body_parts.items():
                # 檢查中文名稱
                if cn_name in text:
                    print(f"✅ [{entity_type}] 精確匹配: '{cn_name}'")
                    return cn_name
                
                # 檢查所有同義詞
                for synonym in synonyms:
                    if synonym.lower() in text_lower:
                        print(f"✅ [{entity_type}] 同義詞匹配: '{synonym}' → '{cn_name}'")
                        return cn_name
        else:
            # 按長度排序，優先匹配長詞（避免「影牙狼」被識別為「狼」）
            sorted_candidates = sorted(candidates, key=len, reverse=True)
            
            for candidate in sorted_candidates:
                if candidate in text:
                    print(f"✅ [{entity_type}] 精確匹配: '{candidate}'")
                    return candidate
        
        _candidates = []
        # ========== 策略 2: 英文名稱映射 ==========
        # 使用 en_to_cn 字典
        for word in text.split():
            word_lower = word.lower()
            
            # 直接字典查找
            if word_lower in self.data.en_to_cn:
                cn_name = self.data.en_to_cn[word_lower]
                if cn_name in candidates:
                    print(f"✅ [{entity_type}] 英文映射: '{word}' → '{cn_name}'")
                    return cn_name
            
            
            # 檢查遊戲數據中的 en_name 字段
            for candidate in candidates:
                en_name = self._get_en_name(entity_type, candidate)

                if en_name:
                    _candidates.append(en_name)
                if en_name and en_name.lower() == word_lower:
                    print(f"✅ [{entity_type}] 英文名稱匹配: '{word}' → '{candidate}'")
                    return candidate
        
        candidates_with_en = candidates.copy()
        candidates_with_en.extend(_candidates)
        candidates_with_en = list(set(candidates_with_en))  # 去重

        print(f"🔍 [{entity_type}] 候選詞: {candidates_with_en}")

        # ========== 策略 3: Embeddings 語義匹配 ==========
        return self._extract_entity_by_embeddings(text, entity_type, candidates_with_en, optional)
    
    def _extract_entity_by_embeddings(self, text: str, entity_type: str, 
                                     candidates: List[str], optional: bool) -> Optional[str]:
        """使用 BERT Embeddings 做語義匹配（最後手段）"""
        
        # 只對敵人、物品、地點使用 Embeddings（避免對身體部位等誤匹配）
        if entity_type not in ["enemy", "item", "location", "weapon", "npc"]:
            return None if optional else self._get_default_value(entity_type)
        
        # 逐詞計算相似度，取最高分
        best_match = None
        best_score = 0.0
        best_word = None
        
        # 過濾停用詞
        stopwords = {'the', 'a', 'an', 'with', 'to', 'at', 'in', 'on', 'and', 'or', 'is'}
        
        for word in text.split():
            if word.lower() in stopwords or len(word) < 3:
                continue
            
            # 在候選詞中搜索（使用中文名稱）
            match, score = self.embedder.find_most_similar(
                query=word,
                candidates=candidates
            )
            
            print(f"🔍 [{entity_type}] Embedding: '{word}' → '{match}' ({score:.2%})")
            
            if score > best_score:
                best_score = score
                best_match = self.data.en_to_cn[match] if match in self.data.en_to_cn else match
                best_word = word
        
        # 閾值判斷
        threshold = 0.85  # 實體提取需要更高的信心度
        
        if best_score > threshold:
            print(f"✅ [{entity_type}] 最佳 Embedding 匹配: '{best_word}' → '{best_match}' ({best_score:.2%})")
            return best_match
        
        # 未找到匹配
        if optional:
            print(f"❌ [{entity_type}] 未找到匹配 (最高: {best_score:.2%})")
            return None
        else:
            default = self._get_default_value(entity_type)
            print(f"⚠️  [{entity_type}] 使用默認值: '{default}'")
            return default
    
    # ========== 輔助方法 ==========
    def _get_candidates(self, entity_type: str) -> List[str]:
        """獲取實體類型的候選列表"""
        mapping = {
            "enemy": self.data.lexicon["enemies"],
            "weapon": self._get_weapon_candidates(),
            "item": self.data.lexicon["items"],
            "location": self.data.lexicon["locations"],
            "body_part": self._get_body_part_candidates(),
            "npc": ["神秘人", "旅人", "守衛", "商人", "村民"],
            "clue": self.data.clue_names if hasattr(self.data, 'clue_names') else []
        }
        return mapping.get(entity_type, [])

    def _get_weapon_candidates(self) -> List[str]:
        """獲取所有武器候選詞（包括中英文名稱）"""
        candidates = []
        
        # 添加所有中文 key（主名稱）
        candidates.extend(self.data.weapons.keys())
        
        #print(f"🔍 武器候選詞: {candidates}")
        return candidates


    def _get_body_part_candidates(self) -> List[str]:
        """獲取所有身體部位候選詞（包括中英文同義詞）"""
        candidates = []
        
        # 添加所有中文 key（主名稱）
        candidates.extend(self.body_parts.keys())
        
        # 添加所有同義詞（包括英文）
        for cn_name, synonyms in self.body_parts.items():
            candidates.extend([syn.lower() for syn in synonyms])
        
        return candidates

    def _get_en_name(self, entity_type: str, cn_name: str) -> Optional[str]:
        """獲取實體的英文名稱"""
        if entity_type == "enemy":
            enemy_data = next(
                (data for data in self.data.enemies.values() if data.get("name") == cn_name),
                None
            )
            return enemy_data.get("en_name") if enemy_data else None
        
        elif entity_type == "weapon":
            #return self.data.weapons.get(cn_name, {}).get("en_name")
            # 從 en_to_cn 反查
            for en, cn in self.data.en_to_cn.items():
                if cn == cn_name:
                    return en
        elif entity_type == "item":
            # 從 en_to_cn 反查
            for en, cn in self.data.en_to_cn.items():
                if cn == cn_name:
                    return en
        elif entity_type == "clue":
            # 從 en_to_cn 反查
            for en, cn in self.data.en_to_cn.items():
                if cn == cn_name:
                    return en
        
        return None
    
    def _get_default_value(self, entity_type: str) -> str:
        """獲取實體類型的默認值"""
        defaults = {
            "enemy": "當前敵人",
            "weapon": None,
            "item": "未知物品",
            "location": "未知地點",
            "body_part": None,
            "npc": "未知人物"
        }
        return defaults.get(entity_type, "未知")
    
    def _extract_attack_style(self, text: str) -> AttackStyle:
        """提取攻擊方式（規則方法更可靠）"""
        for style, keywords in self.attack_modifiers.items():
            if any(kw in text for kw in keywords):
                return style
        return AttackStyle.NORMAL
    
    def _extract_modifiers(self, text: str) -> List[str]:
        """提取動作修飾詞（規則方法）"""
        modifiers = []
        all_modifiers = ["繞到", "側面", "背後", "後退", "前進", "跳躍", 
                        "flank", "side", "behind", "retreat", "advance", "jump"]
        for mod in all_modifiers:
            if mod in text:
                modifiers.append(mod)
        return modifiers
    