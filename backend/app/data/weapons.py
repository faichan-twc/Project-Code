# Weapons Data
from typing import Dict, Any
from .tutorial_data import TUTORIAL_WEAPONS
from .advanced_tutorial_data import ADVANCED_WEAPONS
from .qin_dynasty_data import QIN_WEAPONS

WEAPONS: Dict[str, Any] = {
    **TUTORIAL_WEAPONS,  # 新手教学武器
    **ADVANCED_WEAPONS,  # 进阶教学武器
    **QIN_WEAPONS,  # 寻秦记武器
    # ===== 可拾取的簡易武器 =====
    "碎石": {
        "damage_bonus": 1,
        "desc": "粗糙的石頭，可以用來投擲或近戰",
        "en_name": "Rock",
        "type": "throwable"
    },
    "尖銳碎石": {
        "damage_bonus": 2,
        "desc": "邊緣鋒利的石頭，比普通碎石更具殺傷力",
        "en_name": "Sharp Rock",
        "type": "throwable"
    },
    "樹枝": {
        "damage_bonus": 1,
        "desc": "乾枯的樹枝，脆弱但能用來防身",
        "en_name": "Branch",
        "type": "melee"
    },
    "粗壯木棒": {
        "damage_bonus": 3,
        "desc": "結實的木棒，適合揮擊",
        "en_name": "Wooden Club",
        "type": "melee"
    },
    "骨頭": {
        "damage_bonus": 2,
        "desc": "不明生物的骨頭，堅硬且鋒利",
        "en_name": "Bone",
        "type": "throwable"
    },
    "破損的劍": {
        "damage_bonus": 4,
        "desc": "斷裂的劍刃，雖已損壞但仍能使用",
        "en_name": "Broken Sword",
        "type": "melee"
    },
    "生鏽匕首": {
        "damage_bonus": 3,
        "desc": "鏽跡斑斑的匕首，鋒利度大打折扣",
        "en_name": "Rusty Dagger",
        "type": "melee"
    },
    
    # ===== 正常武器 =====
    "火把": {
        "damage_bonus": 2, 
        "desc": "簡易火焰武器，適合照明和基礎攻擊",
        "en_name": "Torch"
    },
    "劍": {
        "damage_bonus": 5, 
        "desc": "標準武器，平衡的攻擊力",
        "en_name": "Sword"
    },
    "匕首": {
        "damage_bonus": 3, 
        "desc": "輕型快刀，適合精準打擊",
        "en_name": "Dagger"
    },
    "長劍": {
        "damage_bonus": 7,
        "desc": "鋒利長刃，增加攻擊威力",
        "en_name": "Long Sword"
    },
    "斧頭": {
        "damage_bonus": 8,
        "desc": "重型武器，造成毀滅性傷害",
        "en_name": "Axe"
    },
    "戰斧": {
        "damage_bonus": 10,
        "desc": "雙刃戰斧，強大的劈砍力量",
        "en_name": "Battle Axe"
    },
    "錘子": {
        "damage_bonus": 6,
        "desc": "鈍器武器，對骨骼敵人有效",
        "en_name": "Hammer"
    },
    "戰錘": {
        "damage_bonus": 9,
        "desc": "巨型鐵錘，粉碎性打擊",
        "en_name": "War Hammer"
    },
    "長矛": {
        "damage_bonus": 6,
        "desc": "長柄兵器，保持安全距離",
        "en_name": "Spear"
    },
    "弓箭": {
        "damage_bonus": 5,
        "desc": "遠程武器，可瞄準弱點",
        "en_name": "Bow and Arrow",
        "type": "throwable"
    },
    "長弓": {
        "damage_bonus": 7,
        "desc": "超遠程攻擊，威力強大",
        "en_name": "Long Bow",
        "type": "throwable"
    },
    "十字弓": {
        "damage_bonus": 8,
        "desc": "精準射擊武器，穿透力強",
        "en_name": "Crossbow",
        "type": "throwable"
    },
    "飛刀": {
        "damage_bonus": 4,
        "desc": "投擲武器，攻擊迅速",
        "en_name": "Throwing Knife",
        "type": "throwable"
    },
    "法杖": {
        "damage_bonus": 4,
        "desc": "魔法武器，對靈體有效",
        "en_name": "Staff",
        "type": "melee"
    },
    "火焰法杖": {
        "damage_bonus": 7,
        "desc": "火焰魔法杖，持續灼燒",
        "en_name": "Fire Staff",
        "type": "melee"
    },
    "冰霜法杖": {
        "damage_bonus": 6,
        "desc": "冰霜魔法杖，減緩敵人",
        "en_name": "Frost Staff",
        "type": "melee"
    },
    "鐵棍": {
        "damage_bonus": 4,
        "desc": "簡易鈍器，可攻可守",
        "en_name": "Iron Rod",
        "type": "melee"
    },
    "雙刀": {
        "damage_bonus": 6,
        "desc": "雙持武器，連續攻擊",
        "en_name": "Dual Blades",
        "type": "melee"
    },
    "鎖鏈": {
        "damage_bonus": 5,
        "desc": "金屬鎖鏈，束縛攻擊",
        "en_name": "Chain",
        "type": "melee"
    },
    "鞭子": {
        "damage_bonus": 4,
        "desc": "長鞭武器，範圍攻擊",
        "en_name": "Whip",
        "type": "melee"
    },
    "神聖劍": {
        "damage_bonus": 12,
        "desc": "神聖力量加持，對不死生物威力倍增",
        "en_name": "Holy Sword",
        "type": "melee"
    },
    "暗影刃": {
        "damage_bonus": 11,
        "desc": "暗影之力，致命一擊",
        "en_name": "Shadow Blade",
        "type": "melee"
    }
}
