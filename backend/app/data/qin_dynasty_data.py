# 寻秦记世界数据 - 高难度
from typing import Dict, Any

# ========== 新敌人 ==========
QIN_ENEMIES: Dict[str, Any] = {
    "assassin": {
        "name": "影刺客",
        "abbr": "刺客",
        "en_name": "Shadow Assassin",
        "en_id": "assassin",
        "maxhp": 75,
        "baseAtk": 15,
        "hint": "速度極快的刺客，擅長連續攻擊和施毒。攻擊其手臂可解除武裝。",
        "skills": {
            "swift_strike": {
                "name": "疾風連刺",
                "dmg": [12, 18],
                "debuff": {"bleed": 2}
            },
            "poison_blade": {
                "name": "淬毒刀刃",
                "dmg": [10, 16],
                "debuff": {"poison": 3},
                "cd": 2
            },
            "shadow_step": {
                "name": "影步",
                "buff": {"evasion": 0.4},
                "cd": 3
            }
        },
        "drops": [
            {"item": "解毒丹", "qty": 1, "chance": 0.6},
            {"item": "銀兩", "qty": 50, "chance": 1.0}
        ],
        "body_parts": {
            "手臂": {"en_name": "arm", "damage_multiplier": 1.6, "special": "disarm", "chance": 0.4},
            "頭": {"en_name": "head", "damage_multiplier": 2.0, "special": "stun", "chance": 0.2},
            "腿": {"en_name": "leg", "damage_multiplier": 1.3, "special": "slow", "chance": 0.35}
        },
        "dialogues": {
            "low_hp": ["「失手了...」刺客身形晃動。", "「不可能...我竟然...」"],
            "intimidated": ["刺客眼神閃爍，似乎在評估形勢。", "「有兩下子...」"],
            "enraged": ["「接下這招！」刺客速度暴增！", "刺客發出尖銳的嘶鳴，攻勢更加兇猛！"]
        }
    },
    
    "swordmaster": {
        "name": "劍道宗師",
        "abbr": "劍師",
        "en_name": "Sword Master",
        "en_id": "swordmaster",
        "maxhp": 90,
        "baseAtk": 18,
        "hint": "精通劍術的高手，攻擊力極高。破壞其劍可大幅降低威脅。",
        "skills": {
            "blade_dance": {
                "name": "劍舞",
                "dmg": [16, 24]
            },
            "thrust": {
                "name": "破甲突刺",
                "dmg": [20, 28],
                "cd": 3
            },
            "war_cry": {
                "name": "戰吼",
                "buff": {"critUp": 3, "atkUp": 2},
                "cd": 4
            }
        },
        "drops": [
            {"item": "秦劍殘片", "qty": 1, "chance": 0.8},
            {"item": "強效療傷藥", "qty": 1, "chance": 0.5},
            {"item": "銀兩", "qty": 80, "chance": 1.0}
        ],
        "body_parts": {
            "劍": {"en_name": "sword", "damage_multiplier": 1.8, "special": "disarm", "chance": 0.3},
            "胸甲": {"en_name": "chest", "damage_multiplier": 0.8, "special": None, "chance": 0},
            "頭": {"en_name": "head", "damage_multiplier": 2.1, "special": "stun", "chance": 0.15}
        },
        "dialogues": {
            "low_hp": ["「好劍法！」劍師喘著粗氣。", "「劍道...不過如此嗎...」"],
            "intimidated": ["「有意思...」劍師擺出架勢。", "「看來遇到對手了。」"],
            "enraged": ["「劍之道，無堅不摧！」", "劍師眼神凌厲，劍氣四射！"]
        }
    },
    
    "imperial_guard": {
        "name": "秦國禁軍",
        "abbr": "禁軍",
        "en_name": "Imperial Guard",
        "en_id": "guard",
        "maxhp": 100,
        "baseAtk": 16,
        "hint": "身著重甲的精銳士兵，防禦力高但速度較慢。",
        "skills": {
            "spear_thrust": {
                "name": "長矛突刺",
                "dmg": [14, 20]
            },
            "shield_bash": {
                "name": "盾擊",
                "dmg": [12, 18],
                "debuff": {"stun": 1},
                "cd": 4
            },
            "formation": {
                "name": "結陣",
                "buff": {"evasion": 0.2},
                "cd": 3
            }
        },
        "drops": [
            {"item": "療傷藥", "qty": 2, "chance": 0.7},
            {"item": "青銅護符", "qty": 1, "chance": 0.3}
        ],
        "body_parts": {
            "盾牌": {"en_name": "shield", "damage_multiplier": 0.6, "special": None, "chance": 0},
            "頭盔": {"en_name": "helmet", "damage_multiplier": 1.4, "special": "stun", "chance": 0.25},
            "腿": {"en_name": "leg", "damage_multiplier": 1.5, "special": "immobilize", "chance": 0.3}
        },
        "dialogues": {
            "low_hp": ["禁軍咬牙堅持，但已力不從心。", "「為了大秦...」"],
            "intimidated": ["禁軍依然堅守崗位。", "「我等誓死守衛！」"],
            "enraged": ["「犯我大秦者，雖遠必誅！」", "禁軍怒吼，攻勢更加猛烈！"]
        }
    },
    
    "imperial_commander": {
        "name": "禁軍統領",
        "abbr": "統領",
        "en_name": "Imperial Commander",
        "en_id": "commander",
        "is_boss": True,
        "maxhp": 180,
        "baseAtk": 22,
        "hint": "秦國禁軍的統帥，武藝高強且戰術靈活。攻擊其頭盔可造成眩暈，破壞戰戟可降低攻擊力。",
        "skills": {
            "halberd_sweep": {
                "name": "戰戟橫掃",
                "dmg": [18, 26]
            },
            "crushing_blow": {
                "name": "碎骨重擊",
                "dmg": [24, 34],
                "debuff": {"bleed": 2},
                "cd": 3
            },
            "commander_aura": {
                "name": "統帥之威",
                "buff": {"enrage": 2, "critUp": 3},
                "cd": 4
            },
            "tactical_strike": {
                "name": "戰術突襲",
                "dmg": [28, 38],
                "cd": 5
            }
        },
        "drops": [
            {"item": "虎符殘片", "qty": 1, "chance": 1.0},
            {"item": "強效療傷藥", "qty": 2, "chance": 0.9},
            {"item": "青銅護符", "qty": 1, "chance": 0.7},
            {"item": "銀兩", "qty": 150, "chance": 1.0}
        ],
        "body_parts": {
            "頭盔": {"en_name": "helmet", "damage_multiplier": 2.0, "special": "stun", "chance": 0.2},
            "戰戟": {"en_name": "halberd", "damage_multiplier": 1.9, "special": "disarm", "chance": 0.25},
            "胸甲": {"en_name": "armor", "damage_multiplier": 0.7, "special": "crack", "chance": 0.15},
            "腿": {"en_name": "leg", "damage_multiplier": 1.4, "special": "slow", "chance": 0.3}
        },
        "dialogues": {
            "low_hp": ["「統領之位...豈能輕易喪失...」統領氣喘吁吁。", "「不可能...我統率千軍...怎會敗於汝手...」"],
            "intimidated": ["「有膽識！但大秦威嚴不容侵犯！」", "統領冷笑：「讓你見識何為軍陣之道！」"],
            "enraged": ["「夠了！讓你見識統領真正的實力！」統領爆發全力！", "「為大秦而戰，至死方休！」氣勢如虹！"]
        }
    },
    
    "jing_ke": {
        "name": "荊軻",
        "abbr": "荊軻",
        "en_name": "Jing Ke",
        "en_id": "jing_ke",
        "is_boss": True,
        "maxhp": 220,
        "baseAtk": 25,
        "hint": "傳說中的頂尖刺客，速度、力量、技巧皆為頂尖。極度危險！攻擊其匕首可暫時解除武裝，攻擊頭部有機會眩暈。風蕭蕭兮易水寒...",
        "skills": {
            "assassin_strike": {
                "name": "圖窮匕見",
                "dmg": [22, 32],
                "debuff": {"bleed": 3}
            },
            "deadly_poison": {
                "name": "劇毒淬刃",
                "dmg": [20, 28],
                "debuff": {"poison": 4},
                "cd": 2
            },
            "phantom_step": {
                "name": "鬼魅身法",
                "buff": {"evasion": 0.5},
                "cd": 3
            },
            "fatal_blow": {
                "name": "致命一擊",
                "dmg": [30, 45],
                "lifesteal": 0.4,
                "cd": 4
            },
            "berserker_rage": {
                "name": "孤注一擲",
                "buff": {"enrage": 3, "critUp": 4},
                "cd": 5
            }
        },
        "drops": [
            {"item": "傳國玉璽", "qty": 1, "chance": 1.0},
            {"item": "荊軻匕首", "qty": 1, "chance": 1.0},
            {"item": "強效療傷藥", "qty": 3, "chance": 1.0},
            {"item": "青銅護符", "qty": 2, "chance": 0.8}
        ],
        "body_parts": {
            "頭": {"en_name": "head", "damage_multiplier": 2.3, "special": "stun", "chance": 0.15},
            "匕首": {"en_name": "dagger", "damage_multiplier": 2.0, "special": "disarm", "chance": 0.2},
            "心臟": {"en_name": "heart", "damage_multiplier": 2.5, "special": "banish", "chance": 0.1},
            "手臂": {"en_name": "arm", "damage_multiplier": 1.7, "special": "disarm", "chance": 0.25}
        },
        "dialogues": {
            "low_hp": ["「風蕭蕭兮易水寒...壯士一去兮不復還...」荊軻低語。", "「此行...終究未能完成使命...」荊軻露出苦笑。"],
            "intimidated": ["「哼，有意思的對手。」荊軻眼神凌厲。", "「讓我看看你有何本事！」"],
            "enraged": ["「為了燕國！為了太子丹！受死！」荊軻全力爆發！", "「今日不是你死，就是我亡！」殺氣沖天！"]
        }
    }
}

# ========== 新武器 ==========
QIN_WEAPONS: Dict[str, Any] = {
    "青銅劍": {
        "damage_bonus": 5,
        "desc": "戰國時期常見的青銅長劍，鋒利耐用",
        "en_name": "Bronze Sword",
        "type": "melee"
    },
    "秦劍": {
        "damage_bonus": 8,
        "desc": "秦國鍛造的精良長劍，削鐵如泥",
        "en_name": "Qin Sword",
        "type": "melee"
    },
    "長戟": {
        "damage_bonus": 10,
        "desc": "長柄戰戟，攻擊範圍廣且威力強大",
        "en_name": "Long Halberd",
        "type": "melee"
    },
    "荊軻匕首": {
        "damage_bonus": 12,
        "desc": "荊軻刺秦時使用的匕首，傳說中的神兵利器",
        "en_name": "Jing Ke's Dagger",
        "type": "melee"
    },
    "弩箭": {
        "damage_bonus": 6,
        "desc": "秦國精製的弩箭，射程遠且精準",
        "en_name": "Crossbow Bolt",
        "type": "throwable"
    },
    "飛鏢": {
        "damage_bonus": 3,
        "desc": "小巧的暗器，可快速投擲",
        "en_name": "Throwing Dart",
        "type": "throwable"
    }
}

# ========== 新道具 ==========
QIN_ITEMS: Dict[str, Any] = {
    "療傷藥": {
        "stack": True,
        "desc": "普通的草藥製劑，回復 40 生命。",
        "en_name": "healing medicine",
        "use": {
            "type": "heal",
            "value": 40,
            "consume": True,
            "trigger_enemy": False
        }
    },
    
    "強效療傷藥": {
        "stack": True,
        "desc": "名醫調配的珍貴藥劑，回復 70 生命。",
        "en_name": "greater healing medicine",
        "use": {
            "type": "heal",
            "value": 70,
            "consume": True,
            "trigger_enemy": False
        }
    },
    
    "解毒丹": {
        "stack": True,
        "desc": "解除中毒和流血狀態的靈丹妙藥。",
        "en_name": "antidote pill",
        "use": {
            "type": "cleanse",
            "cleanse": ["poison", "bleed"],
            "consume": True,
            "trigger_enemy": False,
            "message": "你服下解毒丹，體內的毒素迅速消散。"
        }
    },
    
    "青銅護符": {
        "stack": True,
        "desc": "提升 35% 閃避率，持續 3 回合。",
        "en_name": "bronze talisman",
        "use": {
            "type": "buff",
            "buff": "evasion",
            "value": 0.35,
            "duration": 3,
            "consume": True,
            "trigger_enemy": False,
            "message": "護符散發青光，你的身法變得更加輕盈。"
        }
    },
    
    "銀兩": {
        "stack": True,
        "desc": "戰國時期的貨幣，可用於交易。",
        "en_name": "silver",
        "use": None
    },
    
    "虎符": {
        "stack": False,
        "desc": "調兵遣將的信物，由虎符殘片合成。可開啟秦宮內殿。",
        "en_name": "tiger tally",
        "use": {
            "type": "context",
            "contexts": {
                "qin_palace_gate": {
                    "message": "你出示虎符，禁軍肅然起敬，讓開通往內殿的道路！",
                    "unlock_location": "qin_inner_palace",
                    "consume": False
                },
                "default": {
                    "message": "虎符是調兵信物，在此處無用。",
                    "consume": False
                }
            }
        }
    },
    
    "虎符殘片": {
        "stack": True,
        "desc": "虎符的一半，收集兩片可在吕府工坊合成完整虎符。",
        "en_name": "tiger tally fragment",
        "use": {
            "type": "context",
            "contexts": {
                "lv_workshop": {
                    "message": "你將虎符殘片交給工匠",
                    "requires": [{"item": "虎符殘片", "qty": 2}],
                    "remove_items": [{"item": "虎符殘片", "qty": 2}],
                    "give_item": "虎符",
                    "craft_message": "工匠仔細拼合兩片殘片，完整的虎符重現於世！",
                    "consume": False
                },
                "default": {
                    "message": "虎符殘片需要在工坊才能合成。",
                    "consume": False
                }
            }
        }
    },
    
    "秦劍殘片": {
        "stack": True,
        "desc": "精良秦劍的碎片，收集3片可重鑄秦劍。",
        "en_name": "qin sword fragment",
        "use": {
            "type": "context",
            "contexts": {
                "lv_workshop": {
                    "message": "你將秦劍殘片交給鑄劍師",
                    "requires": [{"item": "秦劍殘片", "qty": 3}],
                    "remove_items": [{"item": "秦劍殘片", "qty": 3}],
                    "give_item": "秦劍",
                    "one_time_give": False,
                    "craft_message": "鑄劍師重新鍛造，一把鋒利的秦劍出爐了！",
                    "consume": False
                },
                "default": {
                    "message": "需要在工坊才能重鑄秦劍。",
                    "consume": False
                }
            }
        }
    },
    
    "傳國玉璽": {
        "stack": False,
        "desc": "秦始皇的傳國玉璽，象徵著至高無上的皇權。擊敗荊軻，守護大秦的證明！",
        "en_name": "imperial seal",
        "use": None
    },
    
    "密信": {
        "stack": False,
        "desc": "一封密信，記載著刺秦計劃的細節。",
        "en_name": "secret letter",
        "use": None
    }
}

# ========== 寻秦记世界 ==========
QIN_WORLD = {
    "id": "qin_dynasty",
    "name": "尋秦記：戰國風雲",
    "en_name": "A Step Into The Past",
    "difficulty": 5,  # 1=新手, 2=簡單, 3=中等, 4=困難, 5=專家
    "cover_image": "qin_dynasty.png",
    "opening": """戰國末年，七雄爭霸的時代即將落幕。
    
秦王嬴政，這位未來將統一六國的始皇帝，此刻正面臨著生命中最大的危機——來自燕國的刺客荊軻，正策劃著驚天動地的刺秦行動。

你，一名神秘的旅者，偶然得知了這個陰謀。歷史的車輪即將轉動，而你的選擇，將決定這個時代的命運。

是守護秦王，助其完成統一大業？還是讓歷史的洪流沖刷一切？

邯鄲的街市喧囂依舊，但暗流湧動。你的冒險，從這裡開始...""",
    "description": "戰國末年，刺秦在即。潛入邯鄲、滲透咸陽、保護秦王。高難度挑戰，強敵環伺，一步錯則萬劫不復！",
    
    "initial_inventory": [
        {"name": "青銅劍", "qty": 1},
        {"name": "療傷藥", "qty": 3},
        {"name": "解毒丹", "qty": 1},
        {"name": "銀兩", "qty": 100}
    ],
    
    "locations": {
        "handan_market": {
            "name": "邯鄲街市",
            "en_name": "Handan Market",
            "exits": ["lv_manor"],
            "ambient": ["繁華的邯鄲街市人聲鼎沸，商販的叫賣聲此起彼伏。酒肆茶樓林立，空氣中瀰漫著酒香和香料的氣味。身著各國服飾的商人、遊俠、官員穿梭其間，讓這座趙國都城充滿活力。\n\n然而在繁華的表象下，你察覺到異樣——街角有幾個形跡可疑的人在竊竊私語，他們的目光不時掃向遠處的豪宅。那是權傾朝野的呂不韋府邸。\n\n可拾取：青銅劍(Bronze Sword)、弩箭(Crossbow Bolt)\n出口：呂府(Lv Manor)"],
            "spawns": ["assassin:0.4", "swordmaster:0.3"],
            "pickable_items": [
                {"name": "青銅劍", "qty": 1, "respawn": False},
                {"name": "弩箭", "qty": 5, "respawn": False}
            ],
            "clues": {
                "商販": {
                    "en_name": "merchant",
                    "search": "一個販賣兵器的商販告訴你，最近城裡來了很多江湖人士，都在打聽呂府的消息。",
                    "origin": "呂不韋是秦國的丞相，權勢滔天，為何會有人盯上他？"
                },
                "告示": {
                    "en_name": "notice",
                    "search": "城門口貼著告示：『秦王嬴政懸賞緝拿刺客，活捉者賞千金！』",
                    "method": "看來秦國已經察覺到刺殺的風聲，但為時已晚。"
                },
                "乞丐": {
                    "en_name": "beggar",
                    "search": "一個乞丐小聲說：『大人，我看到有人往呂府送了一封密信...』",
                    "give_item": ["療傷藥", "銀兩"]
                }
            }
        },
        
        "lv_manor": {
            "name": "呂府",
            "en_name": "Lv Manor",
            "exits": ["handan_market", "zhao_palace", "xianyang_gate"],
            "ambient": ["呂不韋的府邸宏偉壯觀，高牆深院，守衛森嚴。府門口站著數名持戈禁衛，神情警惕。庭院中假山流水，亭台樓閣，盡顯權貴奢華。\n\n府內有工坊，傳說能工巧匠可以鑄造神兵利器，修復破損的虎符。後院通往趙宮的密道，是呂不韋與趙國朝廷聯絡的秘密通道。呂不韋身為秦國丞相，從這裡可以直接前往咸陽。\n\n出口：邯鄲街市(Handan Market)、趙宮(Zhao Palace)、咸陽城門(Xianyang Gate)"],
            "spawns": ["assassin:0.5", "imperial_guard:0.3"],
            "context": "lv_workshop",
            "clues": {
                "工坊": {
                    "en_name": "workshop",
                    "search": "工坊中擺滿了各種兵器和工具，鑄劍師正在專心鍛造。",
                    "method": "收集虎符殘片可以在此合成完整虎符，收集秦劍殘片可以重鑄秦劍。"
                },
                "密道": {
                    "en_name": "secret passage",
                    "search": "後院假山後有一條密道，通往趙宮。呂不韋經常通過這裡與趙國勾結。",
                    "origin": "呂不韋本是商人，因奇貨可居之計扶持嬴政上位，如今位高權重，但野心依舊。"
                },
                "書房": {
                    "en_name": "study",
                    "search": "你在書房找到一封密信！內容令人震驚：『刺秦之計已定，荊軻將於咸陽行刺...』",
                    "give_item": ["密信", "強效療傷藥"]
                }
            }
        },
        
        "zhao_palace": {
            "name": "趙宮",
            "en_name": "Zhao Palace",
            "exits": ["lv_manor"],
            "ambient": ["趙國王宮金碧輝煌，但已顯頹敗之勢。秦國日益強大，趙國岌岌可危，宮中瀰漫著末世的悲涼。大殿中懸掛著『趙惠文王』的匾額，但此時的趙王已無力抵抗秦國鐵蹄。\n\n宮中隱藏著許多密謀者，他們與燕國刺客勾結，企圖刺殺秦王嬴政。你必須小心謹慎，一旦暴露身份，將面臨圍攻。\n\n出口：呂府(Lv Manor)"],
            "spawns": ["assassin:0.6", "swordmaster:0.4"],
            "clues": {
                "王座": {
                    "en_name": "throne",
                    "search": "空蕩蕩的王座訴說著趙國的衰落。秦國統一天下，已成定局。",
                    "origin": "趙國曾是七雄之一，但在長平之戰後元氣大傷，如今只能苟延殘喘。"
                },
                "密室": {
                    "en_name": "secret room",
                    "search": "你發現了一個密室，裡面存放著大量黃金和兵器，似乎是為刺客準備的。",
                    "give_item": ["虎符殘片", "青銅護符", "銀兩"]
                },
                "壁畫": {
                    "en_name": "mural",
                    "search": "壁畫描繪著趙國的輝煌歷史，但如今只剩回憶。",
                    "reason": "強秦東出，六國將亡，這是歷史的必然。"
                }
            }
        },
        
        "xianyang_gate": {
            "name": "咸陽城門",
            "en_name": "Xianyang Gate",
            "exits": ["lv_manor", "qin_outer_palace"],
            "ambient": ["巍峨的咸陽城門聳立眼前，黑色的城牆如山一般壓迫。城門上『大秦』二字鐵畫銀鉤，透露著這個新興帝國的威嚴。城門守衛森嚴，禁軍持戈而立，檢查每一個進城的人。\n\n身為秦國丞相呂不韋的『隨從』，你順利通過了檢查。遠處可見連綿的宮殿，那裡是秦王嬴政的居所，也是荊軻刺秦的目標。歷史的決戰，即將在那裡上演。\n\n可拾取：長戟(Long Halberd)\n出口：呂府(Lv Manor)、秦宮外殿(Qin Outer Palace)"],
            "spawns": ["imperial_guard:0.7", "swordmaster:0.3"],
            "pickable_items": [
                {"name": "長戟", "qty": 1, "respawn": False}
            ],
            "clues": {
                "城牆": {
                    "en_name": "wall",
                    "search": "高聳的城牆上刻著秦國的戰績：滅韓、破趙、伐楚...統一六國指日可待。",
                    "origin": "秦國自商鞅變法以來，國力日盛，如今已成天下最強。"
                },
                "禁軍": {
                    "en_name": "guard",
                    "search": "禁軍裝備精良，軍紀嚴明，是秦國統一天下的基石。",
                    "method": "想要進入秦宮，必須先擊敗守衛或出示虎符。"
                }
            }
        },
        
        "qin_outer_palace": {
            "name": "秦宮外殿",
            "en_name": "Qin Outer Palace",
            "exits": ["xianyang_gate"],
            "locked_exits": {"qin_inner_palace": "通往內殿的大門緊閉，需要虎符才能開啟"},
            "ambient": ["秦宮外殿莊嚴肅穆，黑色大理石鋪就的地面光可鑑人。殿柱上雕刻著龍鳳呈祥的圖案，展示著秦國的威嚴。殿內站著大量禁軍，他們目光如炬，警惕地注視著每一個接近內殿的人。\n\n殿中央有一扇巨大的青銅門，門上雕刻著饕餮紋飾。門後就是秦王嬴政的寢宮——內殿。守衛把守森嚴，需要虎符才能通過。\n\n空氣中彌漫著緊張的氣氛...荊軻可能已經混進來了！時間緊迫，你必須盡快阻止他！\n\n出口：咸陽城門(Xianyang Gate)"],
            "spawns": ["imperial_guard:0.5", "imperial_commander:0.8"],
            "context": "qin_palace_gate",
            "clues": {
                "青銅門": {
                    "en_name": "bronze gate",
                    "search": "巨大的青銅門緊閉，需要虎符才能開啟。門後就是秦王的寢宮。",
                    "method": "合成完整的虎符，方可開啟此門。"
                },
                "壁畫": {
                    "en_name": "mural",
                    "search": "壁畫描繪著秦國統一天下的宏圖：東滅六國，北卻匈奴，南平百越。",
                    "origin": "這是秦始皇的野心，也是歷史的必然。"
                },
                "密報": {
                    "en_name": "report",
                    "search": "你發現一份密報：『荊軻已潛入咸陽，可能化裝成使臣接近秦王！』",
                    "give_item": ["強效療傷藥", "青銅護符"]
                }
            }
        },
        
        "qin_inner_palace": {
            "name": "秦宮內殿",
            "en_name": "Qin Inner Palace",
            "exits": ["qin_outer_palace"],
            "ambient": ["秦宮內殿金碧輝煌，龍案上擺放著竹簡奏摺，牆上掛著天下輿圖。這裡是秦王嬴政處理政務的地方，也是荊軻刺秦的現場。\n\n突然，一個黑衣人從暗處躍出——正是荊軻！他手持匕首，目光如電，殺氣凜然。你必須在他刺殺秦王之前阻止他！\n\n「風蕭蕭兮易水寒，壯士一去兮不復還！」荊軻悲壯地吟唱著，向秦王沖去...\n\n最終決戰，一觸即發！\n\n出口：秦宮外殿(Qin Outer Palace)"],
            "spawns": ["jing_ke:1.0"],
            "clues": {
                "龍案": {
                    "en_name": "dragon desk",
                    "search": "龍案上堆滿奏摺，都是關於統一六國的計劃。秦王嬴政的野心，躍然紙上。",
                    "origin": "一統天下，千古一帝，這是秦始皇的宏願。"
                },
                "輿圖": {
                    "en_name": "map",
                    "search": "牆上的輿圖標註著六國位置，許多地方已被塗成黑色——那是秦國的版圖。",
                    "method": "統一天下已成定局，只差最後一步。"
                },
                "寶座": {
                    "en_name": "throne",
                    "search": "秦王的寶座空蕩蕩的，秦王嬴政此刻不知身在何處...你必須保護他！",
                    "give_item": ["強效療傷藥"]
                }
            }
        }
    },
    
    "quests": [
        {
            "id": "q_protect_qin",
            "title": "守護秦王",
            "desc": "刺秦計劃已經開始，荊軻潛入咸陽。你必須阻止這場刺殺，守護秦王嬴政，讓歷史按照軌跡前進。",
            "state": "NOT_STARTED",
            "start": {"trigger": "onEnter", "location": "handan_market"},
            "objectives": [
                {"type": "REACH_LOCATION", "location": "lv_manor", "desc": "前往呂府調查"},
                {"type": "OBSERVE", "target": "書房", "desc": "在呂府書房尋找線索"},
                {"type": "COLLECT_ITEM", "item": "密信", "qty": 1, "desc": "獲得刺秦密信"},
                {"type": "REACH_LOCATION", "location": "zhao_palace", "desc": "潛入趙宮"},
                {"type": "OBSERVE", "target": "密室", "desc": "調查趙宮密室"},
                {"type": "COLLECT_ITEM", "item": "虎符殘片", "qty": 2, "desc": "收集2個虎符殘片"},
                {"type": "USE_ITEM", "item": "虎符殘片", "context": "lv_workshop", "desc": "在呂府工坊合成虎符"},
                {"type": "COLLECT_ITEM", "item": "虎符", "qty": 1, "desc": "獲得完整虎符"},
                {"type": "REACH_LOCATION", "location": "xianyang_gate", "desc": "前往咸陽城門"},
                {"type": "USE_ITEM", "item": "虎符", "context": "qin_palace_gate", "desc": "用虎符開啟秦宮內殿"},
                {"type": "REACH_LOCATION", "location": "qin_inner_palace", "desc": "進入秦宮內殿"},
                {"type": "DEFEAT_ENEMY", "enemy": "jing_ke", "qty": 1, "desc": "擊敗荊軻！"},
                {"type": "COLLECT_ITEM", "item": "傳國玉璽", "qty": 1, "desc": "保護傳國玉璽"}
            ],
            "rewards": [
                {"type": "giveItem", "name": "強效療傷藥", "qty": 5},
                {"type": "giveItem", "name": "青銅護符", "qty": 3},
                {"type": "giveItem", "name": "銀兩", "qty": 500}
            ]
        },
        
        {
            "id": "q_forge_qin_sword",
            "title": "重鑄秦劍",
            "desc": "收集秦劍殘片，在呂府工坊重鑄傳說中的秦劍。這把神兵利器將大幅提升你的戰鬥力。",
            "state": "NOT_STARTED",
            "start": {"trigger": "onEnter", "location": "lv_manor"},
            "objectives": [
                {"type": "OBSERVE", "target": "工坊", "desc": "與鑄劍師對話"},
                {"type": "COLLECT_ITEM", "item": "秦劍殘片", "qty": 3, "desc": "收集3個秦劍殘片（擊敗劍道宗師獲得）"},
                {"type": "USE_ITEM", "item": "秦劍殘片", "context": "lv_workshop", "desc": "在工坊重鑄秦劍"},
                {"type": "COLLECT_ITEM", "item": "秦劍", "qty": 1, "desc": "獲得秦劍"}
            ],
            "rewards": [
                {"type": "giveItem", "name": "強效療傷藥", "qty": 2},
                {"type": "giveItem", "name": "青銅護符", "qty": 1}
            ]
        }
    ]
}
