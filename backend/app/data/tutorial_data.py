# 新手教学世界 - 冒险者训练营
from typing import Dict, Any

# ========== 新手教学敌人 ==========
TUTORIAL_ENEMIES: Dict[str, Any] = {
    "training_dummy": {
        "name": "训练假人",
        "abbr": "假人",
        "en_name": "Training Dummy",
        "en_id": "dummy",
        "maxhp": 30,
        "baseAtk": 5,
        "hint": "用于练习攻击的训练假人，不会还击。试试攻击它吧！",
        "skills": {
            "idle": {
                "name": "静止不动",
                "dmg": [0, 0]
            }
        },
        "drops": [
            {"item": "木劍", "qty": 1, "chance": 1.0}
        ],
        "body_parts": {
            "頭": {"en_name": "head", "damage_multiplier": 1.5, "special": None, "chance": 0},
            "身體": {"en_name": "body", "damage_multiplier": 1.0, "special": None, "chance": 0}
        },
        "dialogues": {
            "low_hp": ["假人搖搖晃晃..."],
            "intimidated": [""],
            "enraged": [""]
        }
    },
    
    "weak_slime": {
        "name": "弱小史萊姆",
        "abbr": "史萊姆",
        "en_name": "Weak Slime",
        "en_id": "slime",
        "maxhp": 25,
        "baseAtk": 4,
        "hint": "軟綿綿的小史萊姆，攻擊力很弱。適合新手練習。",
        "skills": {
            "bounce": {
                "name": "彈跳撞擊",
                "dmg": [3, 6]
            }
        },
        "drops": [
            {"item": "小型治療藥水", "qty": 1, "chance": 0.8}
        ],
        "body_parts": {
            "核心": {"en_name": "core", "damage_multiplier": 1.3, "special": None, "chance": 0}
        },
        "dialogues": {
            "low_hp": ["史萊姆軟趴趴地縮小了..."],
            "intimidated": ["「啵嚕啵嚕...」"],
            "enraged": ["史萊姆用力彈跳！"]
        }
    }
}

# ========== 新手教学武器 ==========
TUTORIAL_WEAPONS: Dict[str, Any] = {
    "木劍": {
        "damage_bonus": 3,
        "description": "訓練用的木劍，雖然不鋒利但足以對付弱小敵人",
        "en_name": "Wooden Sword",
        "type": "melee"
    }
}

# ========== 新手教学道具 ==========
TUTORIAL_ITEMS: Dict[str, Any] = {
    "小型治療藥水": {
        "stack": True,
        "desc": "回復 30 生命值的基礎藥水。",
        "en_name": "small healing potion",
        "use": {
            "type": "heal",
            "value": 30,
            "consume": True,
            "trigger_enemy": False
        }
    },
    
    "訓練指南": {
        "stack": False,
        "desc": "一本教導冒險者基礎知識的指南書。",
        "en_name": "training guide",
        "use": None
    }
}

# ========== 新手教学世界 ==========
TUTORIAL_WORLD = {
    "id": "tutorial",
    "name": "冒險者訓練營",
    "en_name": "Adventurer Training Camp",
    "difficulty": 1,  # 新手難度
    "cover_image": "tutorial.png",
    "opening": """歡迎來到冒險者訓練營！

這裡是所有偉大冒險的起點。在這個安全的訓練場地，你將學會成為一名合格冒險者所需的基本技能。

訓練教官站在營地入口，手持木劍，等待著新學員的到來。

「歡迎，新人！」教官微笑著說，「在這裡，你將學會如何移動、戰鬥、休息和使用道具。準備好開始你的冒險之旅了嗎？」

你的訓練，從現在開始！""",
    "description": "新手友好的教學關卡，引導玩家學習基本操作。無難度，輕鬆上手！",
    
    "initial_inventory": [
        {"name": "訓練指南", "qty": 1},
        {"name": "小型治療藥水", "qty": 3}
    ],
    
    "locations": {
        "training_ground": {
            "name": "訓練場",
            "en_name": "Training Ground",
            "exits": ["equipment_room"],
            "ambient": ["寬敞的訓練場地上豎立著幾個訓練假人。教官站在一旁，手中拿著木劍。陽光灑在泥土地面上，空氣中充滿著新學員的緊張與期待。\n\n教官說：「來吧，試著拾取木劍然後攻擊那個訓練假人！輸入『使用木劍攻擊假人』或『use sword to attack dummy』。」\n\n可拾取：木劍(Wooden Sword)\n出口：裝備室(Equipment Room)"],
            "spawns": ["training_dummy:1.0"],
            "pickable_items": [
                {"name": "木劍", "qty": 1, "respawn": False}
            ],
            "clues": {
                "教官": {
                    "en_name": "instructor",
                    "search": "教官是一位經驗豐富的冒險者。他說：「記住這些基本指令：\n• 攻擊：attack [敵人]\n• 使用武器攻擊：use [武器] to attack [敵人]\n• 防禦：defend\n• 觀察：look [目標]\n• 前往：go to [地點]\n• 拾取：pick [物品]\n• 使用道具：use [物品]\n• 休息：rest」",
                    "method": "熟練這些指令，你就能應對大部分情況了！先拾取木劍，然後用它攻擊訓練假人吧！"
                },
                "訓練假人": {
                    "en_name": "dummy",
                    "search": "一個用稻草和木頭製成的訓練假人，專門用於練習攻擊。它不會還手，是新手練習的最佳對象。",
                    "method": "先拾取木劍（pick sword），然後輸入『use sword to attack dummy』或『用木劍攻擊假人』來使用武器攻擊！你也可以試試攻擊特定部位，如『use sword to attack dummy's head』！"
                }
            }
        },
        
        "equipment_room": {
            "name": "裝備室",
            "en_name": "Equipment Room",
            "exits": ["training_ground", "rest_area"],
            "ambient": ["裝備室內整齊地擺放著各種訓練用具：木劍、皮甲、盾牌。牆上貼著一張告示，說明如何使用道具。\n\n貨架上還有一些治療藥水供學員使用。\n\n出口：訓練場(Training Ground)、休息區(Rest Area)"],
            "spawns": [],
            "pickable_items": [
                {"name": "小型治療藥水", "qty": 2, "respawn": False}
            ],
            "clues": {
                "告示": {
                    "en_name": "notice",
                    "search": "告示寫道：\n『如何使用道具』\n1. 輸入『use [物品名稱]』來使用道具\n2. 例如：use potion 或 使用藥水\n3. 有些道具可以在戰鬥中使用，有些則需要在戰鬥外使用\n4. 善用道具可以大大提升你的生存能力！",
                    "method": "試試現在使用一瓶治療藥水吧！即使你沒受傷，也能看到效果。"
                },
                "貨架": {
                    "en_name": "shelf",
                    "search": "貨架上整齊地擺放著補給品。你可以拾取一些治療藥水備用。",
                    "method": "輸入『pick potion』或『拾取藥水』來拾取物品。"
                }
            }
        },
        
        "rest_area": {
            "name": "休息區",
            "en_name": "Rest Area",
            "exits": ["equipment_room"],
            "ambient": ["舒適的休息區有幾張長椅和一個營火。這裡是冒險者恢復體力的地方。牆上掛著一塊木牌，寫著休息的重要性。\n\n角落裡站著一隻看起來很弱小的史萊姆，似乎是訓練用的活體靶子。\n\n出口：裝備室(Equipment Room)"],
            "spawns": ["weak_slime:0.8"],
            "clues": {
                "木牌": {
                    "en_name": "sign",
                    "search": "木牌寫道：\n『休息的重要性』\n• 輸入『rest』或『休息』可以恢復 20 生命值\n• 休息需要消耗一個回合\n• 在安全的地方休息，不要在敵人面前休息！\n• 如果敵人在場，休息會給敵人攻擊機會",
                    "method": "試著在擊敗史萊姆後休息，恢復你的生命值。"
                },
                "營火": {
                    "en_name": "campfire",
                    "search": "溫暖的營火散發著舒適的光芒。在營火旁休息能讓人感到特別安心。",
                    "origin": "自古以來，營火就是冒險者的避風港。"
                },
                "史萊姆": {
                    "en_name": "slime",
                    "search": "一隻軟綿綿的小史萊姆，看起來人畜無害。教官說這是用來訓練防禦技巧的。",
                    "method": "試著在戰鬥中使用『defend』或『防禦』來減少傷害！防禦姿態能減少 50% 的傷害。"
                }
            }
        }
    },
    
    "quests": [
        {
            "id": "q_tutorial_basic",
            "title": "冒險者基礎訓練",
            "desc": "完成教官安排的基礎訓練，學習成為冒險者所需的各項技能。",
            "state": "NOT_STARTED",
            "start": {"trigger": "onEnter", "location": "training_ground"},
            "objectives": [
                {"type": "OBSERVE", "target": "教官", "desc": "與教官對話，了解基本指令（輸入：look instructor）"},
                {"type": "COLLECT_ITEM", "item": "木劍", "qty": 1, "desc": "拾取木劍（輸入：pick sword）"},
                {"type": "DEFEAT_ENEMY", "enemy": "training_dummy", "qty": 1, "desc": "擊敗訓練假人（輸入：attack dummy）"},
                {"type": "REACH_LOCATION", "location": "equipment_room", "desc": "前往裝備室（輸入：go to equipment room）"},
                {"type": "OBSERVE", "target": "告示", "desc": "閱讀裝備室的告示（輸入：look notice）"},
                {"type": "REACH_LOCATION", "location": "rest_area", "desc": "前往休息區（輸入：go to rest area）"},
                {"type": "OBSERVE", "target": "木牌", "desc": "閱讀休息區的木牌（輸入：look sign）"},
                {"type": "DEFEAT_ENEMY", "enemy": "weak_slime", "qty": 1, "desc": "擊敗史萊姆，練習防禦技巧（輸入：attack slime）"}
            ],
            "rewards": [
                {"type": "giveItem", "name": "小型治療藥水", "qty": 5},
                {"type": "giveItem", "name": "木劍", "qty": 1}
            ]
        }
    ]
}
