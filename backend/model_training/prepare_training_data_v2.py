# backend/app/prepare_training_data_v2.py
import json
import os
import sys
from pathlib import Path
from typing import List, Dict

# Add parent directory to path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data.synonyms import SYNONYMS
from app.game_data import GameData

def generate_enhanced_training_data() -> List[Dict[str, str]]:
    """生成更真實、更豐富的訓練數據"""
    training_data = []
    game_data = GameData()

    # ==================== 1. 基礎同義詞 ====================
    for intent, synonyms in SYNONYMS.items():
        for synonym in synonyms:
            training_data.append({
                "text": synonym,
                "label": intent.upper()
            })
    
    # ==================== 2. 攻擊指令 (最重要！) ====================
    attack_verbs = ["攻擊", "打", "殺",
                    "attack", "hit", "fight"]
    
    # 所有敵人名稱
    enemies = ["野狗", "dog", "狼", "wolf"]
    
    weapons = ["石頭", "sword", "火把", "torch"]

    print(enemies)
    print(weapons)
    # 生成「動詞 + 敵人」組合
    for verb in attack_verbs:
        for enemy in enemies[:4]:  # 取前 4 個敵人
            for weapon in weapons[:4]:  # 取前 4 個武器
                training_data.extend([
                    {"text": f"{verb} {enemy}", "label": "ATTACK"},
                    {"text": f"用 {weapon} {verb} {enemy}", "label": "ATTACK"},
                    {"text": f"快速 {verb} {enemy}", "label": "ATTACK"},
                    {"text": f"{verb} {enemy} with {weapon} ", "label": "ATTACK"},
                    {"text": f"{verb} {enemy} using {weapon} ", "label": "ATTACK"},
                    {"text": f"{verb} {enemy} using {weapon} quickly", "label": "ATTACK"},
                ])
    
    # 添加更多變體
    attack_templates = [
        "{verb}那隻{enemy}",
        "向{enemy} {verb}",
        "對{enemy} {verb}",
        "我要{verb} {enemy}",
        "{verb} the {enemy}",
        "{verb} at {enemy}",
        "I want to {verb} {enemy}",
    ]
    
    sample_enemies = ["狼", "怨靈", "wolf", "king"]
    for template in attack_templates:
        for verb in attack_verbs[:3]:
            for enemy in sample_enemies:
                try:
                    text = template.format(verb=verb, enemy=enemy)
                    training_data.append({"text": text, "label": "ATTACK"})
                except:
                    pass
    
    # ==================== 3. 移動指令 ====================
    move_verbs = ["前往", "去", "走到", "到", "move", "go", "walk", "goto"]
    locations = ["森林深處", "古井", "山洞", "神殿", "地下墓穴",
                 "temple", "forest", "well", "cave", "dungeon"]
    
    for verb in move_verbs:
        for loc in locations:
            training_data.extend([
                {"text": f"{verb} {loc}", "label": "MOVE"},
                {"text": f"{verb} to {loc}", "label": "MOVE"},
                {"text": f"我想{verb} {loc}", "label": "MOVE"},
                {"text": f"i want to {verb} {loc}", "label": "MOVE"},
            ])
    
    # ==================== 4. 觀察指令 ====================
    observe_verbs = ["觀察", "查看", "看", "調查", "look", "check"]
    observe_targets = ["四周", "周圍", "地面", "敵人", "線索", "野狗", "狼", "怨靈", "不死之王",
                      "around", "ground", "enemy", "clue", "dog", "wolf", "ghost", "king"]
    
    for verb in observe_verbs:
        training_data.append({"text": verb, "label": "OBSERVE"})
        training_data.append({"text": f"{verb}四周", "label": "OBSERVE"})
        for target in observe_targets:
            training_data.extend([
                {"text": f"{verb} {target}", "label": "OBSERVE"},
                {"text": f"i want to {verb} {target}", "label": "OBSERVE"},
                {"text": f"我想 {verb} {target}", "label": "OBSERVE"},
            ])
    
    # ==================== 5. 拾取指令 ====================
    pick_verbs = ["拾取", "撿", "拿", "取", "pick", "take", "get"]
    items = ["碎石", "藥水", "草藥", "stone", "potion", "sword", "torch"]
    
    for verb in pick_verbs:
        for item in items:
            training_data.extend([
                {"text": f"{verb} {item}", "label": "PICK"},
                {"text": f"{verb} 那個{item}", "label": "PICK"},
                {"text": f"i want to {verb} {item}", "label": "PICK"},
                {"text": f"我想 {verb} {item}", "label": "PICK"},
            ])
    
    # ==================== 6. 使用指令 ====================
    use_verbs = ["使用", "喝", "吃", "use", "drink", "eat"]
    usable_items = ["治療藥水", "藥水", "火把", "地圖",
                    "potion", "torch", "healing potion", "map"]
    
    for verb in use_verbs:
        for item in usable_items:
            training_data.extend([
                {"text": f"{verb} {item}", "label": "USE"},
                {"text": f"我要 {verb} {item}", "label": "USE"},
                {"text": f"我想 {verb} {item}", "label": "USE"},
                {"text": f"i want to {verb} {item}", "label": "USE"},
            ])
    
    # ==================== 7. 問題指令 ====================
    question_base = [
        "這是什麼？",
        "這裡是哪裡？",
        "怎麼走？",
        "為什麼有霧？",
        "霧從哪來？",
        "What is this?",
        "Where am I?",
        "How do I get there?",
        "Why is there fog?",
        "Where is the fog from?",
        "什麼是{item}？",
        "這個{item}是什麼？",
        "{location}在哪裡？",
        "怎麼去{location}？",
    ]

    # ==================== 7.1 線索相關問題 (World Data Clues) ====================
    # 從遊戲數據中提取所有線索對象
    clue_objects = [
        # 森林場景
        "樹", "tree", "地面", "ground", "霧", "fog", "倒木", "log", "武器", "weapon",
        "石碑", "monument", "井", "well", "符文", "rune", "水", "water",
        "石柱", "pillar", "門", "door", "聖壇", "altar", "壁畫", "mural",
        
        # 沙漠場景
        "帳篷", "tent", "石柱", "pillars", "箱子", "chest", "骨骸", "bones",
        "祭壇", "altar", "守護者", "guardian", "浮雕", "relief",
        
        # 秦朝場景
        "書房", "study", "竹簡", "scroll", "密信", "letter", "玉佩", "jade",
        "文字", "text", "石碑", "stone",
        
        # 通用對象
        "四周", "around", "周圍", "surroundings", "這裡", "here",
    ]
    
    # 線索問題模板 - what is (基本描述)
    what_templates = [
        "what is {obj}",
        "what's {obj}",
        "{obj} 是什麼",
        "這個 {obj} 是什麼",
        "什麼是 {obj}",
        "{obj} 是什麼東西",
        "tell me about {obj}",
        "describe {obj}",
        "關於 {obj}",
    ]
    
    # 線索問題模板 - where/origin (來源/歷史)
    where_templates = [
        "where {obj}",
        "where is {obj} from",
        "{obj} 從哪來",
        "{obj} 的來源",
        "{obj} 從哪裡來",
        "{obj} 的歷史",
        "origin {obj}",
        "origin of {obj}",
        "{obj} origin",
        "{obj} 起源",
    ]
    
    # 線索問題模板 - why/reason (原因/目的)
    why_templates = [
        "why {obj}",
        "why is {obj} here",
        "為什麼有 {obj}",
        "{obj} 為什麼在這",
        "{obj} 的原因",
        "reason {obj}",
        "reason for {obj}",
        "{obj} reason",
        "{obj} 目的",
        "為何 {obj}",
    ]
    
    # 線索問題模板 - how/method (方法/解決方案)
    how_templates = [
        "how {obj}",
        "how to {obj}",
        "怎麼 {obj}",
        "{obj} 怎麼用",
        "{obj} 的方法",
        "method {obj}",
        "method for {obj}",
        "{obj} method",
        "如何 {obj}",
        "怎麼使用 {obj}",
    ]
    
    # 生成所有線索問題組合
    clue_questions = []
    for obj in clue_objects[:15]:  # 取前15個對象避免數據過多
        for template in what_templates[:4]:
            try:
                text = template.format(obj=obj)
                clue_questions.append({"text": text, "label": "QUESTION"})
            except:
                pass
        
        for template in where_templates[:4]:
            try:
                text = template.format(obj=obj)
                clue_questions.append({"text": text, "label": "QUESTION"})
            except:
                pass
        
        for template in why_templates[:4]:
            try:
                text = template.format(obj=obj)
                clue_questions.append({"text": text, "label": "QUESTION"})
            except:
                pass
        
        for template in how_templates[:4]:
            try:
                text = template.format(obj=obj)
                clue_questions.append({"text": text, "label": "QUESTION"})
            except:
                pass
    
    training_data.extend(clue_questions)

    for template in question_base:
        try:
            text = template.format(item="石頭", location="神殿")
            training_data.append({"text": text, "label": "QUESTION"})
        except:
            training_data.append({"text": template, "label": "QUESTION"})
    
    # ==================== 8. 其他指令 ====================
    
    # ==================== 3. 防禦指令 (大幅增強！) ====================
    defend_base = ["防禦", "防守", "格擋", "架勢", "守住", "defend", "block", "guard", "parry"]
    
    # 增加豐富的上下文變體
    defend_variants = [
        # 完整句子
        "我要防禦",
        "進入防守姿態",
        "準備防禦",
        "舉起盾牌",
        "擺出防守架勢",
        "保持防守",
        "專心防守",
        "小心防禦",
        "快防",
        "趕快防守",
        
        # 口語化
        "先守一下",
        "防一下",
        "守好",
        "穩住防守",
        "hold defense",
        "stay defensive",
        "keep guard",
        
        # 戰鬥情境
        "防禦攻擊",
        "防守住",
        "擋下攻擊",
        "格擋來襲",
        "防禦敵人",
        "防住敵人的攻擊",
        
        # 簡寫/變體
        "防",
        "守",
        "擋",
        "hold",
        "guard up",
        "defense mode",
        
        # 祈使句
        "防禦！",
        "快防禦！",
        "防守！",
        "擋住！",
    ]
    
    for phrase in defend_base + defend_variants:
        training_data.append({"text": phrase, "label": "DEFEND"})
    
    # ==================== 4. 休息指令 (大幅增強！) ====================
    rest_base = ["休息", "睡覺", "療傷", "打坐", "恢復", "rest", "sleep", "heal", "recover"]
    
    rest_variants = [
        # 完整句子
        "我要休息",
        "休息一下",
        "睡一覺",
        "恢復體力",
        "恢復生命",
        "療傷休息",
        "停下來休息",
        "找地方休息",
        "坐下休息",
        
        # 口語化
        "先休息",
        "休息下",
        "歇一會",
        "歇息",
        "打個盹",
        "take a rest",
        "have a rest",
        "take a break",
        
        # 治療相關
        "治療傷勢",
        "回血",
        "補血",
        "恢復HP",
        "heal up",
        "recover health",
        
        # 簡寫
        "息",
        "歇",
        "睡",
        "break",
        "nap",
        
        # 祈使句
        "休息！",
        "快休息！",
        "趕快休息！",
        "先休息一下！",
    ]
    
    for phrase in rest_base + rest_variants:
        training_data.append({"text": phrase, "label": "REST"})
    
    # ==================== 5. 逃跑指令 (大幅增強！) ====================
    escape_base = ["逃跑", "逃走", "逃離", "撤退", "快跑", "escape", "flee", "run", "retreat"]
    
    escape_variants = [
        # 完整句子
        "趕快逃",
        "快逃",
        "逃命",
        "撤退吧",
        "快點逃跑",
        "逃離這裡",
        "離開戰鬥",
        "撤離",
        
        # 口語化
        "跑路",
        "溜了",
        "閃人",
        "先走",
        "撤",
        "run away",
        "get out",
        "get away",
        
        # 緊急情境
        "打不過快逃",
        "逃離戰鬥",
        "逃出去",
        "趕緊跑",
        "快跑啊",
        
        # 簡寫
        "逃",
        "跑",
        "走",
        "閃",
        "run",
        "flee!",
        
        # 祈使句
        "逃跑！",
        "快逃！",
        "撤退！",
        "快跑！",
    ]
    
    for phrase in escape_base + escape_variants:
        training_data.append({"text": phrase, "label": "ESCAPE"})
    
    # ==================== 9. 對話指令 (新增) ====================
    talk_templates = [
        "說話", "對話", "交談", "聊天", "talk", "speak", "chat",
        "和{target}說話",
        "跟{target}聊天",
        "問{target}",
        "talk to {target}",
        "speak with {target}",
    ]
    
    targets = ["守衛", "旅人", "神秘人", "商人", "guard", "traveler", "merchant"]
    for template in talk_templates:
        try:
            for target in targets:
                text = template.format(target=target)
                training_data.append({"text": text, "label": "TALK"})
        except:
            training_data.append({"text": template, "label": "TALK"})
    
    return training_data

def generate_mixed_language_data() -> List[Dict[str, str]]:
    """生成中英混合訓練數據"""
    training_data = []
    
    # ========== 中英混合攻擊命令 ==========
    mixed_attack_templates = [
        # 中文動詞 + 英文名詞
        "攻擊 the wolf",
        "砍 the enemy",
        "打 the ghost",
        "用 sword 攻擊狼",
        "用 stone 砸怨靈",
        
        # 英文動詞 + 中文名詞
        "attack 影牙狼",
        "kill 怨靈",
        "hit 不死之王",
        "strike the 狼",
        
        # 完全混合
        "use sword 砍 wolf",
        "快速 attack 敵人",
        "用力 hit the enemy",
    ]
    
    for template in mixed_attack_templates:
        training_data.append({
            "text": template,
            "label": "ATTACK"
        })
    
    # ========== 中英混合移動命令 ==========
    mixed_move_templates = [
        "go to 神殿",
        "前往 temple",
        "walk to 森林",
        "去 the forest",
        "move to 古井",
        "enter the 地下墓穴",
    ]
    
    for template in mixed_move_templates:
        training_data.append({
            "text": template,
            "label": "MOVE"
        })
    
    # ========== 中英混合拾取命令 ==========
    mixed_pick_templates = [
        "pick up 碎石",
        "拾取 stone",
        "撿 the sword",
        "take 治療藥水",
        "grab the 火把",
        "拿 potion",
    ]
    
    for template in mixed_pick_templates:
        training_data.append({
            "text": template,
            "label": "PICK"
        })
    
    # ========== 添加玩家真實輸入模式 ==========
    realistic_mixed = [
        # 懶人輸入（混合拼音）
        "gong ji wolf",  # 攻擊 wolf
        "qu temple",     # 去 temple
        "na stone",      # 拿 stone
        
        # 口語化混合
        "打那個 wolf",
        "去一下 temple",
        "拿個 stone",
        
        # 錯別字容錯
        "atack 狼",      # attack 打錯
        "攻機 wolf",     # 攻擊 打錯
    ]
    
    # 根據上下文推斷 intent
    intent_map = {
        "gong ji": "ATTACK", "atack": "ATTACK", "攻機": "ATTACK",
        "qu": "MOVE", "na": "PICK"
    }
    
    for text in realistic_mixed:
        # 簡單規則推斷
        for key, intent in intent_map.items():
            if key in text.lower():
                training_data.append({
                    "text": text,
                    "label": intent
                })
                break
    
    return training_data

# 整合到主函數
def save_enhanced_training_data():
    data = generate_enhanced_training_data()  # 原有數據
    data.extend(generate_mixed_language_data())  # 新增混合數據
    
    for item in data:
        item['text'] = normalize(item['text'])
        item['label'] = item['label'].strip().upper()

    # 去重並保存
    unique_data = []
    seen = set()
    for item in data:
        key = (item['text'], item['label'])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
    
    # 統計
    label_counts = {}
    for item in unique_data:
        label = item["label"]
        label_counts[label] = label_counts.get(label, 0) + 1
    
    print("📊 增強訓練數據統計:")
    for label, count in sorted(label_counts.items()):
        print(f"  {label}: {count} 樣本")
    print(f"\n✅ 總共生成 {len(unique_data)} 個訓練樣本")
    
    # 保存
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "intent_training_data_enhanced.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 數據已保存到: {output_path}")
    return unique_data

def normalize(text: str) -> str:
    """輕量級預處理（僅用於規則方法）"""
    
    text = text.strip()
    text = text.replace("！", "!").replace("？", "?")
    text = " ".join(text.split())
    text = text.lower()

    
    return text

if __name__ == "__main__":
    save_enhanced_training_data()