# backend/test_bert_intent.py (新文件)
from app.nlp import ChineseNLP
from app.game_data import GameData

def test_bert_predictions():
    """測試 BERT 模型預測"""
    nlp = ChineseNLP(use_bert=True)
    
    test_cases = [
        "攻擊影牙狼",
        "用劍快速攻擊",
        "前往森林深處",
        "觀察四周",
        "拾取碎石",
        "使用治療藥水",
        "防禦",
        "休息一下",
        "逃跑",
        "where is the fog come from?",
        "attack the wolf",
        "go to temple",
        "pick up stone",
    ]
    
    print("🧪 BERT 模型測試\n")
    print(f"{'指令':<20} {'BERT預測':<12} {'信心度':<10} {'實體提取'}")
    print("="*70)
    
    for command in test_cases:
        intent_obj = nlp.parse(command)
        intent, confidence = nlp.predict_intent_bert(command)
        
        # Handle None returns when BERT is not available
        if intent is None:
            intent = intent_obj.intent
            confidence = 0.0
        
        entities = []
        if intent_obj.target:
            entities.append(f"目標:{intent_obj.target}")
        if intent_obj.item:
            entities.append(f"物品:{intent_obj.item}")
        if intent_obj.location:
            entities.append(f"地點:{intent_obj.location}")
        
        entities_str = ", ".join(entities) if entities else "-"
        
        print(f"{command:<20} {intent:<12} {confidence:>6.1%}    {entities_str}")

if __name__ == "__main__":
    test_bert_predictions()