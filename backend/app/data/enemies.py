# Enemies Data
from typing import Dict, Any
from .tutorial_data import TUTORIAL_ENEMIES
from .advanced_tutorial_data import ADVANCED_ENEMIES
from .qin_dynasty_data import QIN_ENEMIES

ENEMIES: Dict[str, Any] = {
    **TUTORIAL_ENEMIES,  # 新手教学敌人
    **ADVANCED_ENEMIES,  # 进阶教学敌人
    **QIN_ENEMIES,  # 寻秦记敌人
    "wolf": {
        "name": "影牙狼",
        "abbr": "狼",
        "en_name": "Shadow Fang Wolf",
        "en_id": "wolf",
        "maxhp": 45,
        "baseAtk": 10,
        "drops": [{"item": "狼牙", "qty": 1, "chance": 1.0}],
        "skills": {
            "bite": {"name": "撕咬", "dmg": [8, 14]},
            "howl": {"name": "號召嚎叫", "buff": {"critUp": 2}, "cd": 3},
            "pounce": {"name": "撲擊", "dmg": [14, 20], "cd": 3}
        },
        "body_parts": {
            "眼睛": {"damage_multiplier": 1.5, "special": "blind", "chance": 0.3},
            "腿": {"damage_multiplier": 1.2, "special": "slow", "chance": 0.4},
            "頭": {"damage_multiplier": 1.8, "special": "stun", "chance": 0.2}
        },
        "dialogues": {
            "low_hp": ["影牙狼開始畏縮，眼中露出恐懼...", "狼發出低沉的嗚咽，似乎在猶豫..."],
            "intimidated": ["在你的威嚇下，狼後退了幾步...", "狼的攻擊變得遲疑..."],
            "enraged": ["你的話語激怒了野獸！狼的眼睛變得血紅！", "狼發出憤怒的咆哮，攻擊更加兇猛！"]
        }
    },
    "wraith": {
        "name": "沙怨靈",
        "abbr": "怨靈",
        "en_name": "Sand Wraith",
        "en_id": "wraith",
        "maxhp": 60,
        "baseAtk": 8,
        "drops": [
            {"item": "神秘寶石", "qty": 1, "chance": 0.8},
            {"item": "水晶碎片", "qty": 1, "chance": 0.4}
        ],
        "skills": {
            "drain": {"name": "沙靈汲取", "dmg": [10, 14], "lifesteal": 0.5, "cd": 2},
            "veil": {"name": "流沙帷幕", "buff": {"evasion": 0.25}, "cd": 3},
            "wail": {"name": "荒嘯", "stun": 1, "cd": 4}
        },
        "body_parts": {
            "身體": {"damage_multiplier": 1.3, "special": "disperse", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["怨靈的形體開始變得透明...", "沙怨靈的嘶吼變得微弱..."],
            "intimidated": ["你的威嚇似乎對非生命體無效...", "怨靈不為所動..."],
            "enraged": ["怨靈發出刺耳的尖嘯！", "沙塵暴變得更加猛烈！"]
        }
    },
    "zombie": {
        "name": "腐屍行者",
        "abbr": "腐屍",
        "en_name": "Rotting Walker",
        "en_id": "zombie",
        "maxhp": 70,
        "baseAtk": 6,
        "drops": [
            {"item": "治療藥水", "qty": 1, "chance": 0.3},
            {"item": "解毒草", "qty": 1, "chance": 0.5}
        ],
        "skills": {
            "grab": {"name": "腐爛之握", "dmg": [5, 10]},
            "bite": {"name": "感染撕咬", "dmg": [8, 12], "debuff": {"poison": 2}},
            "surge": {"name": "不死猛衝", "dmg": [10, 15], "cd": 4}
        },
        "body_parts": {
            "頭": {"damage_multiplier": 2.0, "special": "instant_kill", "chance": 0.15},
            "腿": {"damage_multiplier": 1.4, "special": "immobilize", "chance": 0.5},
            "手臂": {"damage_multiplier": 1.2, "special": "disarm", "chance": 0.3}
        },
        "dialogues": {
            "low_hp": ["腐屍搖搖欲墜，但仍不停止前進...", "殘破的身軀發出骨骼碎裂的聲音..."],
            "intimidated": ["腐屍毫無反應，只是持續逼近...", "死物不懂畏懼..."],
            "enraged": ["腐屍發出刺耳的嘶吼，動作變得狂亂！", "不死的憤怒讓它更加危險！"]
        }
    },
    "spider": {
        "name": "毒網編織者",
        "abbr": "蜘蛛",
        "en_name": "Venom Weaver",
        "en_id": "spider",
        "maxhp": 35,
        "baseAtk": 9,
        "drops": [
            {"item": "神秘寶石", "qty": 1, "chance": 0.5},
            {"item": "麻痺毒藥", "qty": 1, "chance": 0.3}
        ],
        "skills": {
            "bite": {"name": "毒牙", "dmg": [7, 11], "debuff": {"poison": 3}},
            "web": {"name": "蛛網束縛", "debuff": {"slow": 2}, "cd": 3},
            "leap": {"name": "跳躍突襲", "dmg": [12, 18], "cd": 3}
        },
        "body_parts": {
            "腹部": {"damage_multiplier": 1.6, "special": "venom_burst", "chance": 0.3},
            "腿": {"damage_multiplier": 1.3, "special": "slow", "chance": 0.4},
            "眼睛": {"damage_multiplier": 1.5, "special": "blind", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["蜘蛛發出尖銳的嘶鳴，試圖後退...", "蛛腿顫抖著，毒液從傷口滴落..."],
            "intimidated": ["蜘蛛縮起身體，但仍警戒著...", "八隻眼睛閃爍不定..."],
            "enraged": ["蜘蛛變得狂暴，毒液四濺！", "蛛網開始瘋狂噴射！"]
        }
    },
    "scorpion": {
        "name": "沙漠毒蠍",
        "abbr": "蠍子",
        "en_name": "Desert Scorpion",
        "en_id": "scorpion",
        "maxhp": 50,
        "baseAtk": 11,
        "drops": [
            {"item": "神秘寶石", "qty": 1, "chance": 0.6},
            {"item": "解毒草", "qty": 1, "chance": 0.4}
        ],
        "skills": {
            "sting": {"name": "毒尾刺擊", "dmg": [9, 15], "debuff": {"poison": 4}},
            "clamp": {"name": "鉗擊", "dmg": [7, 12], "debuff": {"bleed": 2}, "cd": 2},
            "burrow": {"name": "潛沙突襲", "dmg": [14, 20], "cd": 4}
        },
        "body_parts": {
            "尾巴": {"damage_multiplier": 1.7, "special": "remove_poison", "chance": 0.4},
            "鉗子": {"damage_multiplier": 1.3, "special": "disarm", "chance": 0.35},
            "頭": {"damage_multiplier": 1.5, "special": "stun", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["毒蠍的動作變慢，尾巴無力地垂下...", "甲殼碎裂，發出咔嚓的聲響..."],
            "intimidated": ["毒蠍舉起尾巴，發出警告性的響聲...", "蠍子緩緩後退，但隨時準備反擊..."],
            "enraged": ["毒蠍進入狂暴狀態，尾刺瘋狂揮舞！", "沙塵暴中傳來憤怒的嘶鳴！"]
        }
    },
    "bandit": {
        "name": "沙漠劫匪",
        "abbr": "劫匪",
        "en_name": "Desert Bandit",
        "en_id": "bandit",
        "maxhp": 55,
        "baseAtk": 12,
        "drops": [
            {"item": "治療藥水", "qty": 1, "chance": 0.5},
            {"item": "舊地圖", "qty": 1, "chance": 0.2},
            {"item": "爆裂瓶", "qty": 1, "chance": 0.25}
        ],
        "skills": {
            "slash": {"name": "彎刀斬擊", "dmg": [10, 16]},
            "throw": {"name": "飛刀投擲", "dmg": [8, 14], "cd": 2},
            "ambush": {"name": "伏擊", "dmg": [15, 22], "cd": 4}
        },
        "body_parts": {
            "頭": {"damage_multiplier": 1.8, "special": "stun", "chance": 0.3},
            "手臂": {"damage_multiplier": 1.4, "special": "disarm", "chance": 0.4},
            "腿": {"damage_multiplier": 1.2, "special": "slow", "chance": 0.35}
        },
        "dialogues": {
            "low_hp": ["劫匪開始畏縮：「等等！我們可以談談！」", "劫匪試圖逃跑..."],
            "intimidated": ["「好好好，別衝動！」劫匪舉起雙手。", "劫匪的臉色變得蒼白..."],
            "enraged": ["「你會為此付出代價！」劫匪憤怒地吼叫。", "劫匪的攻擊變得不顧一切！"]
        }
    },
    "gargoyle": {
        "name": "石像鬼",
        "abbr": "石像",
        "en_name": "Stone Gargoyle",
        "en_id": "gargoyle",
        "maxhp": 65,
        "baseAtk": 13,
        "drops": [
            {"item": "神秘寶石", "qty": 2, "chance": 0.7},
            {"item": "水晶碎片", "qty": 1, "chance": 0.6},
            {"item": "守護護符", "qty": 1, "chance": 0.2}
        ],
        "skills": {
            "dive": {"name": "俯衝攻擊", "dmg": [12, 18]},
            "stone_gaze": {"name": "石化凝視", "debuff": {"stun": 1}, "cd": 3},
            "wing_slash": {"name": "翼刃斬擊", "dmg": [10, 16], "cd": 2}
        },
        "body_parts": {
            "翅膀": {"damage_multiplier": 1.6, "special": "ground", "chance": 0.4},
            "頭": {"damage_multiplier": 1.7, "special": "stun", "chance": 0.25},
            "身體": {"damage_multiplier": 1.1, "special": "crack", "chance": 0.3}
        },
        "dialogues": {
            "low_hp": ["石像鬼的身體開始龜裂，碎石剝落...", "翅膀無力地垂下，難以維持飛行..."],
            "intimidated": ["石像鬼是魔法造物，不會被言語影響...", "冰冷的石眼毫無情感..."],
            "enraged": ["石像鬼發出刺耳的石頭摩擦聲！", "魔法能量在石身中暴走！"]
        }
    },
    "undead_king": {
        "name": "不死之王",
        "abbr": "死王",
        "en_name": "Undead King",
        "en_id": "undead_king",
        "is_boss": True,
        "maxhp": 150,
        "baseAtk": 20,
        "hint": "曾經的統治者，如今的不死詛咒源頭。擁有多種致命技能，攻擊王冠可造成眩暈。",
        "drops": [
            {"item": "王室權杖", "qty": 1, "chance": 1.0},
            {"item": "強效治療藥水", "qty": 2, "chance": 0.8},
            {"item": "守護護符", "qty": 1, "chance": 0.6}
        ],
        "skills": {
            "death_strike": {"name": "死亡之擊", "dmg": [18, 26], "debuff": {"curse": 2}},
            "soul_drain": {"name": "靈魂吸取", "dmg": [15, 22], "lifesteal": 0.5, "cd": 3},
            "undead_wrath": {"name": "不死之怒", "buff": {"enrage": 3, "critUp": 3}, "cd": 4},
            "death_aura": {"name": "死亡光環", "dmg": [20, 30], "debuff": {"poison": 3}, "cd": 5}
        },
        "body_parts": {
            "王冠": {"damage_multiplier": 2.2, "special": "stun", "chance": 0.15},
            "權杖": {"damage_multiplier": 1.8, "special": "disarm", "chance": 0.25},
            "胸甲": {"damage_multiplier": 0.6, "special": None, "chance": 0.35},
            "骨骼": {"damage_multiplier": 1.3, "special": "crack", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["「永生...這就是永生的代價嗎...」不死之王痛苦地低語。", "王冠的光芒黯淡下來，骨骼發出咯吱聲..."],
            "intimidated": ["「生者的威嚇對不死者無效！」", "空洞的眼眶中燃起怒火..."],
            "enraged": ["「夠了！你們這些凡人！」不死之王發出震耳欲聾的咆哮！", "亡靈能量從身體中爆發，整個密室都在顫抖！"]
        }
    },
    "ghost_guardian": {
        "name": "幽靈守衛",
        "abbr": "守衛",
        "en_name": "Phantom Guardian",
        "en_id": "ghost",
        "maxhp": 58,
        "baseAtk": 10,
        "drops": [
            {"item": "神秘寶石", "qty": 1, "chance": 0.9},
            {"item": "水晶碎片", "qty": 1, "chance": 0.5}
        ],
        "skills": {
            "spectral_slash": {"name": "幽靈斬", "dmg": [9, 15]},
            "possession": {"name": "附身詛咒", "debuff": {"confusion": 2}, "cd": 3},
            "phase": {"name": "相位移動", "buff": {"evasion": 0.4}, "cd": 4}
        },
        "body_parts": {
            "核心": {"damage_multiplier": 2.0, "special": "banish", "chance": 0.2},
            "身體": {"damage_multiplier": 1.3, "special": "disperse", "chance": 0.3}
        },
        "dialogues": {
            "low_hp": ["幽靈的形體變得飄忽不定...", "守衛的吶喊逐漸微弱..."],
            "intimidated": ["「生者...退後...」幽靈低語道。", "守衛似乎猶豫了..."],
            "enraged": ["「侵入者必須付出代價！」幽靈憤怒地咆哮。", "靈體能量暴增，周圍溫度驟降！"]
        }
    },
    "ancient_guardian": {
        "name": "古代守護者",
        "abbr": "守護者",
        "en_name": "Ancient Guardian",
        "en_id": "ancient_guardian",
        "is_boss": True,
        "maxhp": 120,
        "baseAtk": 18,
        "hint": "守護聖所的強大存在，需要策略和準備才能戰勝。攻擊核心可造成額外傷害。",
        "drops": [
            {"item": "靈魂容器", "qty": 1, "chance": 1.0},
            {"item": "守護護符", "qty": 1, "chance": 0.8}
        ],
        "skills": {
            "crushing_blow": {"name": "粉碎打擊", "dmg": [15, 22]},
            "sand_storm": {"name": "沙塵風暴", "dmg": [18, 25], "debuff": {"bleed": 2}, "cd": 3},
            "ancient_rage": {"name": "遠古之怒", "buff": {"enrage": True, "critUp": 3}, "cd": 5}
        },
        "body_parts": {
            "核心": {
                "en_name": "core",
                "damage_multiplier": 2.0,
                "special": "crack",
                "chance": 0.2
            },
            "護甲": {
                "en_name": "armor",
                "damage_multiplier": 0.7,
                "special": None,
                "chance": 0
            }
        },
        "dialogues": {
            "low_hp": ["守護者的身軀開始崩解...", "我的使命...即將結束..."],
            "intimidated": ["石像毫無反應...", "它不知恐懼..."],
            "enraged": ["你竟敢侵犯聖所！", "感受遠古守護者的憤怒！"]
        }
    },
    "wild_dog": {
        "name": "野犬",
        "abbr": "犬",
        "en_name": "Feral Hound",
        "en_id": "dog",
        "maxhp": 40,
        "baseAtk": 11,
        "drops": [{"item": "治療藥水", "qty": 1, "chance": 0.4}],
        "skills": {
            "bite": {"name": "撕咬", "dmg": [9, 14]},
            "pounce": {"name": "撲咬", "dmg": [12, 17], "cd": 2},
            "howl": {"name": "召喚同伴", "buff": {"critUp": 3}, "cd": 4}
        },
        "body_parts": {
            "頭": {"damage_multiplier": 1.7, "special": "stun", "chance": 0.25},
            "腿": {"damage_multiplier": 1.4, "special": "slow", "chance": 0.4},
            "身體": {"damage_multiplier": 1.2, "special": None, "chance": 0}
        },
        "dialogues": {
            "low_hp": ["野犬發出痛苦的嗚咽...", "犬開始試圖逃離..."],
            "intimidated": ["野犬低下頭，耳朵貼著腦袋...", "犬後退幾步，發出低吼..."],
            "enraged": ["野犬眼睛充血，變得瘋狂！", "犬發出憤怒的咆哮，露出尖牙！"]
        }
    }
}
