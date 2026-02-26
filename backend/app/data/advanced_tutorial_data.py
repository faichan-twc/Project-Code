# 进阶教学世界 - 探险者试炼
from typing import Dict, Any

# ========== 进阶教学敌人 ==========
ADVANCED_ENEMIES: Dict[str, Any] = {
    "stone_golem": {
        "name": "石魔像",
        "abbr": "魔像",
        "en_name": "Stone Golem",
        "en_id": "golem",
        "maxhp": 50,
        "baseAtk": 8,
        "hint": "石魔像全身由堅硬的石頭構成，但頭部的魔法核心是它的弱點。攻擊核心可造成額外傷害！使用重型武器效果更佳。",
        "skills": {
            "stone_punch": {
                "name": "岩石重拳",
                "dmg": [6, 10]
            },
            "harden": {
                "name": "石化",
                "buff": {"evasion": 0.2},
                "cd": 3
            }
        },
        "drops": [
            {"item": "石頭碎片", "qty": 1, "chance": 1.0},
            {"item": "初級治療藥水", "qty": 1, "chance": 0.7}
        ],
        "body_parts": {
            "頭部核心": {"en_name": "head core", "damage_multiplier": 2.0, "special": "stun", "chance": 0.25},
            "身體": {"en_name": "body", "damage_multiplier": 0.8, "special": None, "chance": 0},
            "手臂": {"en_name": "arm", "damage_multiplier": 1.2, "special": "disarm", "chance": 0.15}
        },
        "dialogues": {
            "low_hp": ["石魔像的身體開始崩解..."],
            "intimidated": ["魔像發出低沉的轟鳴聲。"],
            "enraged": ["石魔像憤怒地捶打胸膛！"]
        }
    },
    
    "guardian_statue": {
        "name": "守護石像",
        "abbr": "石像",
        "en_name": "Guardian Statue",
        "en_id": "statue",
        "maxhp": 60,
        "baseAtk": 10,
        "hint": "古老的守護者，持有石劍。破壞它的石劍可以大幅降低攻擊力，攻擊腿部可以減慢它的速度。",
        "skills": {
            "stone_slash": {
                "name": "石劍斬擊",
                "dmg": [8, 12]
            },
            "shield_block": {
                "name": "石盾格擋",
                "buff": {"evasion": 0.3},
                "cd": 4
            }
        },
        "drops": [
            {"item": "神殿鑰匙", "qty": 1, "chance": 1.0},
            {"item": "初級治療藥水", "qty": 2, "chance": 0.8}
        ],
        "body_parts": {
            "石劍": {"en_name": "sword", "damage_multiplier": 1.8, "special": "disarm", "chance": 0.3},
            "頭": {"en_name": "head", "damage_multiplier": 1.5, "special": "stun", "chance": 0.2},
            "腿": {"en_name": "leg", "damage_multiplier": 1.3, "special": "slow", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["守護石像開始龜裂..."],
            "intimidated": ["石像緩緩轉動頭部。"],
            "enraged": ["守護者的眼睛發出紅光！"]
        }
    }
}

# ========== 进阶教学武器 ==========
ADVANCED_WEAPONS: Dict[str, Any] = {
    "鐵劍": {
        "damage_bonus": 6,
        "desc": "標準的鐵製長劍，平衡而可靠",
        "en_name": "Iron Sword",
        "type": "melee"
    },
    
    "重錘": {
        "damage_bonus": 8,
        "desc": "沉重的戰錘，對石質敵人特別有效",
        "en_name": "Heavy Hammer",
        "type": "melee"
    }
}

# ========== 进阶教学道具 ==========
ADVANCED_ITEMS: Dict[str, Any] = {
    "初級治療藥水": {
        "stack": True,
        "desc": "回復 40 生命值的藥水。",
        "en_name": "basic healing potion",
        "use": {
            "type": "heal",
            "value": 40,
            "consume": True,
            "trigger_enemy": False
        }
    },
    
    "探險者地圖": {
        "stack": False,
        "desc": "一張詳細的遺跡地圖，標註了所有房間和通道。使用後可以查看完整地圖。",
        "en_name": "explorer map",
        "use": {
            "type": "call_ai",
            "parameter": "generate_map",
            "message": "你展開地圖，遺跡的整體結構一目了然！",
            "consume": False
        }
    },
    
    "神殿鑰匙": {
        "stack": False,
        "desc": "開啟神殿密室的古老鑰匙。",
        "en_name": "temple key",
        "use": {
            "type": "context",
            "contexts": {
                "temple_lock": {
                    "message": "你將神殿鑰匙插入鎖孔，沉重的石門緩緩打開...",
                    "unlock_location": "secret_chamber",
                    "consume": True
                },
                "default": {
                    "message": "這把鑰匙在這裡沒有用處。",
                    "consume": False
                }
            }
        }
    },
    
    "石頭碎片": {
        "stack": True,
        "desc": "魔像身上掉落的石頭碎片，似乎沒什麼用。",
        "en_name": "stone fragment",
        "use": None
    },
    
    "探險者筆記": {
        "stack": False,
        "desc": "記載著進階戰鬥技巧的筆記本。",
        "en_name": "explorer notes",
        "use": None
    },
    
    "傳送卷軸": {
        "stack": False,
        "desc": "可以傳送回訓練營的魔法卷軸。使用後會立即傳送回冒險者訓練營。",
        "en_name": "teleport scroll",
        "use": {
            "type": "context",
            "contexts": {
                "secret_chamber_location": {
                    "message": "你展開卷軸，魔法陣法在腳下展開，白光閃過...你回到了訓練營！",
                    "unlock_location": "training_ground_return",
                    "consume": True
                },
                "default": {
                    "message": "傳送卷軸在這裡無法使用。",
                    "consume": False
                }
            }
        }
    }
}

# ========== 进阶教学世界 ==========
ADVANCED_TUTORIAL_WORLD = {
    "id": "advanced_tutorial",
    "name": "探險者試煉",
    "en_name": "Explorer's Trial",
    "difficulty": 2,  # 簡單難度
    "cover_image": "advanced_tutorial.png",
    "opening": """你已經掌握了基本的冒險技巧，現在是時候學習更進階的技術了。

在遙遠的荒野中，有一座古老的遺跡——探險者試煉場。這是探險者公會用來培訓精英探險者的訓練設施。

遺跡內有真實的石魔像守衛，以及需要解開的謎題和機關。只有掌握進階技巧的探險者，才能通過這些試煉。

你站在遺跡入口，手中握著一把鐵劍和一張探險者地圖。

「記住，」教官的聲音在你腦海中迴響，「觀察敵人的弱點、活用地圖、善用環境線索、精準打擊要害——這些都是精英探險者必備的技能。」

試煉，開始了！""",
    "description": "進階教學關卡，教導部位攻擊、環境互動、道具解謎等技巧。適合完成新手教學的玩家。",
    
    "initial_inventory": [
        {"name": "探險者筆記", "qty": 1},
        {"name": "探險者地圖", "qty": 1},
        {"name": "鐵劍", "qty": 1},
        {"name": "初級治療藥水", "qty": 3}
    ],
    
    "locations": {
        "entrance_hall": {
            "name": "入口大廳",
            "en_name": "Entrance Hall",
            "exits": ["pillar_hall"],
            "ambient": ["寬敞的入口大廳，陽光從高處的窗戶灑落。石牆上刻著古老的文字，地面鋪著精美的石磚。大廳中央立著一座教學石碑。\n\n這裡是試煉的起點，你需要在這裡學習進階技巧。\n\n可拾取：重錘(Heavy Hammer)\n出口：石柱廳堂(Pillar Hall)"],
            "spawns": [],
            "pickable_items": [
                {"name": "重錘", "qty": 1, "respawn": False}
            ],
            "clues": {
                "教學石碑": {
                    "en_name": "teaching stone",
                    "search": "石碑上刻著進階戰鬥技巧：\n\n【技巧一：全力攻擊弱點】\n使用武器攻擊敵人的特定部位可造成額外傷害！\n\n英文指令格式：\n• use [weapon] to attack [enemy]'s [part]\n• 例如：use sword to attack golem's head\n\n中文指令格式：\n• 用[武器]攻擊[敵人]的[部位]\n• 例如：用劍攻擊魔像的頭部核心\n\n簡化格式：\n• hit [enemy] [part]\n• 例如：hit golem head\n\n不同部位有不同效果：\n• 頭部(head) - 高傷害，可能眩暈\n• 武器(sword/weapon) - 解除武裝\n• 腿部(leg) - 減速\n\n【技巧二：環境線索互動】\n與環境中的事物深入互動可以獲取更多情報：\n• what is [對象] - 基本描述\n• how to [對象] - 方法提示\n• origin [對象] - 來源歷史\n• reason [對象] - 原因目的\n\n💡 試試對旁邊的「古老文字」使用這些問法！",
                    "method": "試著用『observe golem』或『觀察魔像』來查看敵人的弱點和提示。記住，攻擊部位時使用英文單詞（如head、body、arm）更容易被識別！",
                    "origin": "這座石碑是探險者公會立下的，用於訓練後輩。"
                },
                "古老文字": {
                    "en_name": "ancient text",
                    "search": "牆上的文字記載著這座遺跡的歷史。\n\n💡 進階技巧：你可以用不同的問法來獲取更多線索：\n• what is [對象] - 基本描述（例如：what is text）\n• how to [對象] - 方法/解法提示（例如：how to text）\n• where [對象] - 來源/歷史（例如：where text）\n• why [對象] - 原因/目的（例如：why text）\n\n試試看不同的問法吧！",
                    "origin": "這座遺跡建於千年前，原本是守護神殿的要塞。",
                    "reason": "遺跡被廢棄後，探險者公會將其改造為訓練場所。",
                    "method": "環境線索互動是進階探險者的必備技能！除了基本的 observe/look 之外，還可以用 what is、how to、where、why 等問法，從不同角度獲取線索。每個問題都可能揭示不同的信息！"
                },
                "地圖使用說明": {
                    "en_name": "map guide",
                    "search": "一塊小木牌，說明如何使用探險者地圖。",
                    "method": "輸入『use map』或『使用地圖』可以查看遺跡的完整佈局，了解各個區域的連接關係。地圖會顯示哪些區域需要特殊道具才能進入。"
                }
            }
        },
        
        "pillar_hall": {
            "name": "石柱廳堂",
            "en_name": "Pillar Hall",
            "exits": ["entrance_hall", "ancient_temple"],
            "locked_exits": {"secret_chamber": "密室的石門緊閉，上面有一個鑰匙孔。需要神殿鑰匙才能開啟。"},
            "ambient": ["高聳的石柱支撐著穹頂，每根柱子上都雕刻著守護者的圖案。大廳中央站著一尊石魔像，這是你的第一個真正的挑戰。\n\n廳堂一側有一扇緊閉的石門，看起來需要特殊的鑰匙才能打開。\n\n出口：入口大廳(Entrance Hall)、古老神殿(Ancient Temple)"],
            "spawns": ["stone_golem:1.0"],
            "context": "temple_lock",
            "clues": {
                "石柱": {
                    "en_name": "pillar",
                    "search": "石柱上雕刻著守護者的形象，雕工精美。",
                    "origin": "這些石柱是用魔法石打造的，具有加固建築的作用。",
                    "method": "石柱的雕刻記錄了守護者的弱點——頭部的魔法核心。"
                },
                "石門": {
                    "en_name": "stone door",
                    "search": "密室的石門上有一個鑰匙孔，門縫中隱約可見寶物的光芒。",
                    "reason": "密室封印是為了保護重要的聖物不被盜取。",
                    "method": "擊敗古老神殿中的守護石像，它會掉落神殿鑰匙。獲得鑰匙後，在這裡使用鑰匙即可開啟密室。"
                },
                "魔像": {
                    "en_name": "golem",
                    "search": "石魔像是用魔法賦予生命的守衛。它全身堅硬，但頭部的魔法核心閃爍著微弱的光芒。",
                    "method": "使用『observe golem』或『觀察魔像』查看它的弱點。攻擊頭部(head)效果最佳！\n\n指令範例：\n• use sword to attack golem's head\n• 用劍攻擊魔像的頭部核心\n• hit golem head\n\n使用重錘對石質敵人更有效。"
                }
            }
        },
        
        "ancient_temple": {
            "name": "古老神殿",
            "en_name": "Ancient Temple",
            "exits": ["pillar_hall"],
            "ambient": ["莊嚴的神殿內供奉著古老的神像。祭壇上放置著神秘的符文，空氣中瀰漫著神聖的氣息。\n\n一尊守護石像守在祭壇前，手持石劍，警惕地注視著入侵者。這是你的最終挑戰。\n\n出口：石柱廳堂(Pillar Hall)"],
            "spawns": ["guardian_statue:1.0"],
            "clues": {
                "神像": {
                    "en_name": "deity statue",
                    "search": "神像雕刻著一位手持權杖的神祇，表情慈祥而威嚴。",
                    "origin": "這是古代文明崇拜的守護之神。",
                    "reason": "人們建造這座神殿，祈求神明的保護和祝福。"
                },
                "祭壇": {
                    "en_name": "altar",
                    "search": "祭壇上的符文發出微弱的光芒，似乎在回應著什麼。",
                    "method": "祭壇的魔力維持著守護石像的運作。擊敗石像後，你將獲得神殿鑰匙。"
                },
                "守護者": {
                    "en_name": "guardian",
                    "search": "守護石像是神殿最後的防線。它手持石劍，身披石甲。",
                    "method": "用『observe statue』查看弱點！它的石劍是武器，破壞它可以降低攻擊力。攻擊腿部可以減速。記得使用武器進行精準打擊！"
                }
            }
        },
        
        "secret_chamber": {
            "name": "密室",
            "en_name": "Secret Chamber",
            "exits": ["pillar_hall"],
            "locked_exits": {"training_ground_return": "使用傳送卷軸可以返回訓練營。"},
            "context": "secret_chamber_location",
            "ambient": ["隱秘的密室中堆滿了古老的寶藏。金幣、寶石、魔法卷軸散落各處，這是歷代守護者收集的財富。\n\n房間中央有一個寶箱，裡面放著試煉的最終獲勵。\n\n💡 使用傳送卷軸(use scroll)可以返回訓練營。"],
            "spawns": [],
            "pickable_items": [],
            "clues": {
                "寶箱": {
                    "en_name": "treasure chest",
                    "search": "一個精美的寶箱，裡面裝滿了珍貴的物品和藥水。",
                    "method": "你已經通過了試煉！這些是你的獎勵。",
                    "give_item": ["傳送卷軸", "初級治療藥水", "初級治療藥水", "初級治療藥水"]
                },
                "寶藏": {
                    "en_name": "treasure",
                    "search": "閃閃發光的金幣和寶石，價值連城。",
                    "origin": "這些是千年來守護者從盜墓者手中奪回的財寶。",
                    "reason": "財寶被保存在此，等待真正有資格的探險者取走。"
                }
            }
        },
        
        "training_ground_return": {
            "name": "冒險者訓練營",
            "en_name": "Training Ground",
            "exits": [],
            "ambient": ["你回到了熟悉的訓練營。陽光灑在泥土地面上，訓練假人依然豎立在原地。\n\n教官站在訓練場中央，看到你歸來，臉上露出欣慰的笑容。\n\n『歡迎回來，年輕的冒險者！』』"],
            "spawns": [],
            "clues": {
                "教官": {
                    "en_name": "instructor",
                    "search": "教官是一位經驗豐富的冒險者，他正等待著為你舉行畢業儀式。"
                },
                "訓練場": {
                    "en_name": "training ground",
                    "search": "熟悉的訓練場地，這裡是你冒險旅程開始的地方。",
                    "origin": "這座訓練營培養了無數優秀的冒險者。",
                    "reason": "每一位偉大的冒險者，都是從這裡踏出第一步。"
                }
            }
        }
    },
    
    "quests": [
        {
            "id": "q_advanced_trial",
            "title": "探險者試煉",
            "desc": "學習進階戰鬥技巧，包括部位攻擊、環境互動、使用地圖和道具解謎。",
            "state": "NOT_STARTED",
            "start": {"trigger": "onEnter", "location": "entrance_hall"},
            "objectives": [
                {"type": "OBSERVE", "target": "教學石碑", "desc": "閱讀教學石碑，學習部位攻擊"},
                {"type": "OBSERVE", "target": "古老文字", "desc": "學習如何與環境線索互動（search/origin/reason/method）"},
                {"type": "OBSERVE", "target": "地圖使用說明", "desc": "學習如何使用地圖"},
                {"type": "REACH_LOCATION", "location": "pillar_hall", "desc": "前往石柱廳堂"},
                {"type": "OBSERVE", "target": "魔像", "desc": "觀察石魔像，了解敵人弱點"},
                {"type": "DEFEAT_ENEMY", "enemy": "stone_golem", "qty": 1, "desc": "擊敗石魔像（試試攻擊頭部核心！）"},
                {"type": "REACH_LOCATION", "location": "ancient_temple", "desc": "前往古老神殿"},
                {"type": "OBSERVE", "target": "守護石像", "desc": "觀察守護石像的弱點"},
                {"type": "DEFEAT_ENEMY", "enemy": "guardian_statue", "qty": 1, "desc": "擊敗守護石像（試試破壞它的石劍！）"},
                {"type": "COLLECT_ITEM", "item": "神殿鑰匙", "qty": 1, "desc": "獲得神殿鑰匙"},
                {"type": "REACH_LOCATION", "location": "pillar_hall", "desc": "返回石柱廳堂"},
                {"type": "USE_ITEM", "item": "神殿鑰匙", "context": "temple_lock", "desc": "使用神殿鑰匙開啟密室"},
                {"type": "REACH_LOCATION", "location": "secret_chamber", "desc": "進入密室，獲得獎勵"}
            ],
            "rewards": [
                {"type": "giveItem", "name": "初級治療藥水", "qty": 5},
                {"type": "giveItem", "name": "重錘", "qty": 1}
            ]
        },
        
        {
            "id": "q_graduation",
            "title": "正式畢業",
            "desc": "使用傳送卷軸回到冒險者訓練營，與教官完成最後的畢業儀式。",
            "state": "NOT_STARTED",
            "start": {"trigger": "onEnter", "location": "secret_chamber"},
            "objectives": [
                {"type": "OBSERVE", "target": "寶箱", "desc": "觀察寶箱，了解獎勵內容"},
                {"type": "COLLECT_ITEM", "item": "傳送卷軸", "qty": 1, "desc": "獲得傳送卷軸"},
                {"type": "USE_ITEM", "item": "傳送卷軸", "context": "secret_chamber_location", "desc": "使用傳送卷軸回到訓練營（輸入：use scroll）"},
                {"type": "REACH_LOCATION", "location": "training_ground_return", "desc": "回到訓練營"},
                {"type": "OBSERVE", "target": "教官", "desc": "與教官對話，完成畢業儀式"}
            ],
            "rewards": [
                {"type": "giveItem", "name": "初級治療藥水", "qty": 3}
            ]
        }
    ]
}
