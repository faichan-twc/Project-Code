# Items Data
from typing import Dict, Any
from .tutorial_data import TUTORIAL_ITEMS
from .advanced_tutorial_data import ADVANCED_ITEMS
from .qin_dynasty_data import QIN_ITEMS

ITEMS: Dict[str, Any] = {
    **TUTORIAL_ITEMS,  # 新手教学道具
    **ADVANCED_ITEMS,  # 进阶教学道具
    **QIN_ITEMS,  # 寻秦记道具
    "火把": {
        "stack": False, 
        "desc": "照亮黑暗的舊火把。", 
        "en_name": "torch", 
        "use": {
            "type": "context",
            "contexts": {
                "ancient_well": {
                    "message": "你舉起火把照向漆黑的井底，火光驅散了黑暗。在井壁的裂縫中，你發現了一把古老的鑰匙！",
                    "give_item": "森林古鑰",
                    "consume": False
                },
                "default": {
                    "message": "火把發出溫暖的光芒，但這裡似乎不需要照明。",
                    "consume": False
                }
            }
        }
    },
    "舊地圖": {
        "stack": False, 
        "desc": "殘破的地圖，標示著某個位置。", 
        "en_name": "old map", 
        "use": {
            "type": "call_ai",
            "parameter": "generate_map",
            "message": "你仔細研究這張古老的地圖...",
            "consume": False
        }
    },
    "治療藥水": {
        "stack": True, 
        "heal": 30, 
        "desc": "回復 30 生命。", 
        "en_name": "healing potion",
        "use": {
            "type": "heal",
            "value": 30,
            "consume": True,
            "trigger_enemy": False
        }
    },
    "神秘寶石": {
        "stack": True, 
        "desc": "散發微光的寶石，似乎有反應。", 
        "en_name": "mystic gem", 
        "use": None
    },
    "狼牙": {
        "stack": True, 
        "desc": "影牙狼的尖利獰牙。", 
        "en_name": "wolf fang", 
        "use": None
    },
    "森林古鑰": {
        "stack": False,
        "desc": "刻滿符文的古老鑰匙，散發著森林的氣息。可以開啟神殿大門。",
        "en_name": "ancient forest key",
        "use": {
            "type": "context",
            "contexts": {
                "temple_entrance": {
                    "message": "你將森林古鑰插入門鎖，符文開始發光。古老的神殿大門轟然開啟，通往聖所的道路出現了！",
                    "unlock_location": "temple_sanctum",
                    "consume": False
                },
                "default": {
                    "message": "這裡沒有可以使用這把鑰匙的地方。",
                    "consume": False
                }
            }
        }
    },
    
    # === 戰鬥道具 ===
    "爆裂瓶": {
        "stack": True,
        "desc": "投擲後爆炸的煉金藥劑，造成 40-50 傷害。",
        "en_name": "explosive flask",
        "use": {
            "type": "combat",
            "damage": [40, 50],
            "consume": True,
            "trigger_enemy": False,
            "combat_only": True,
            "message": "你投擲爆裂瓶，火焰吞噬了敵人！"
        }
    },
    "麻痺毒藥": {
        "stack": True,
        "desc": "塗抹在武器上，使敵人緩速 3 回合。",
        "en_name": "paralyzing poison",
        "use": {
            "type": "weapon_buff",
            "debuff": {"slow": 3},
            "duration": 1,
            "consume": True,
            "trigger_enemy": False,
            "message": "你將毒藥塗抹在武器上，刀鋒泛著詭異的綠光。"
        }
    },
    "強效治療藥水": {
        "stack": True,
        "desc": "回復 60 生命。",
        "en_name": "greater healing potion",
        "use": {
            "type": "heal",
            "value": 60,
            "consume": True,
            "trigger_enemy": False
        }
    },
    "狂暴藥劑": {
        "stack": True,
        "desc": "提升 20 攻擊力，持續 3 回合。",
        "en_name": "berserk potion",
        "use": {
            "type": "buff",
            "buff": "atkUp",
            "value": 20,
            "duration": 3,
            "consume": True,
            "trigger_enemy": False,
            "message": "你喝下狂暴藥劑，感覺力量湧入全身！"
        }
    },
    "守護護符": {
        "stack": True,
        "desc": "提升 30% 閃避率，持續 3 回合。",
        "en_name": "guardian amulet",
        "use": {
            "type": "buff",
            "buff": "evasion",
            "value": 0.3,
            "duration": 3,
            "consume": True,
            "trigger_enemy": False,
            "message": "護符發出柔和的光芒，你感到身體變得輕盈。"
        }
    },
    "解毒草": {
        "stack": True,
        "desc": "清除所有毒素和流血效果。",
        "en_name": "antidote herb",
        "use": {
            "type": "cleanse",
            "cleanse": ["poison", "bleed"],
            "consume": True,
            "trigger_enemy": False,
            "message": "你咀嚼解毒草，苦澀的汁液驅散了體內的毒素。"
        }
    },
    
    # === 場景互動道具 ===
    "古老符文石": {
        "stack": False,
        "desc": "刻有神秘符文的石板，在特定地點會發光。",
        "en_name": "ancient runestone",
        "use": {
            "type": "context",
            "contexts": {
                "stone_circle": {
                    "message": "你將符文石放在石柱圈中央，古老的符文開始發光！石柱之間浮現出能量脈絡，空氣中迴盪著遠古的低語。符文石與石柱產生共鳴，解開了沙漠深處埋藏千年的秘密！作為見證者，你獲得了神殿的鑰匙。",
                    "give_item": "沙漠神殿鑰匙",
                    "consume": False
                },
                "default": {
                    "message": "符文石微微發光，但似乎需要在特殊地點才能啟動。",
                    "consume": False
                }
            }
        }
    },
    "沙漠神殿鑰匙": {
        "stack": False,
        "desc": "打開埋沙神殿深處的鑰匙。",
        "en_name": "desert temple key",
        "use": {
            "type": "context",
            "contexts": {
                "temple_inner": {
                    "message": "鑰匙完美契合，古老的門扉緩緩開啟，釋放出陣陣陰風...",
                    "consume": False,
                    "unlock_location": "sanctum"
                },
                "default": {
                    "message": "這裡沒有可以使用鑰匙的地方。",
                    "consume": False
                }
            }
        }
    },
    "破損的日記": {
        "stack": False,
        "desc": "探險家的日記，記載著關於遺忘之城的秘密。",
        "en_name": "torn journal",
        "use": {
            "type": "context",
            "contexts": {
                "relief_corridor": {
                    "message": "對照日記上的記載，你發現浮雕中隱藏的機關！一塊石板移開，露出密室...",
                    "consume": False,
                    "unlock_location": "secret_vault"
                },
                "default": {
                    "message": "你翻閱日記，裡面記載著遺忘之城的歷史和寶藏的線索。",
                    "consume": False
                }
            }
        }
    },
    "王室印章": {
        "stack": False,
        "desc": "刻有王室徽記的金色印章，可以開啟王座後方的密道。",
        "en_name": "royal seal",
        "use": {
            "type": "context",
            "contexts": {
                "throne_room": {
                    "message": "你將印章嵌入王座後方的凹槽，隱藏之門緩緩開啟，通往地下密室的道路出現了！",
                    "consume": False,
                    "unlock_location": "underground_chamber"
                },
                "default": {
                    "message": "這枚印章代表王室的權威，似乎可以開啟某個特定的地方。",
                    "consume": False
                }
            }
        }
    },
    "王室權杖": {
        "stack": False,
        "desc": "不死之王的權杖，仍然散發著強大的魔法力量。",
        "en_name": "royal scepter",
        "use": {
            "type": "buff",
            "effect": "attack",
            "value": 12,
            "duration": 999,
            "message": "你握緊權杖，感受到魔法力量流入你的身體，攻擊力大幅提升！",
            "consume": False
        }
    },
    "淨化聖水": {
        "stack": False,
        "desc": "古老的淨化聖水，可以解除不死詛咒。",
        "en_name": "holy water",
        "use": {
            "type": "context",
            "contexts": {
                "underground_ritual": {
                    "message": "你將聖水灘在儀式台上，地下密室中的亡靈符文逐漸消散，詛咒被解除了！你發現了一頂淨化後的王冠。",
                    "give_item": "淨化的王冠",
                    "consume": True
                },
                "default": {
                    "message": "聖水應該在儀式地點使用才會發揮作用。",
                    "consume": False
                }
            }
        }
    },
    "淨化的王冠": {
        "stack": False,
        "desc": "被淨化後的王冠，不再有亡靈的氣息，散發著神聖的光芒——證明你解除了王國的詛咒。",
        "en_name": "purified crown",
        "use": None
    },
    
    # === 任務道具 ===
    "水晶碎片": {
        "stack": True,
        "desc": "閃爍的魔法水晶碎片，收集3個可合成完整水晶。",
        "en_name": "crystal shard",
        "use": {
            "type": "context",
            "contexts": {
                "sacred_altar": {
                    "message": "你將水晶碎片放在聖壇上",
                    "requires": [{"item": "水晶碎片", "qty": 3}],
                    "remove_items": [{"item": "水晶碎片", "qty": 3}],
                    "give_item": "完整水晶",
                    "one_time_give": False,
                    "craft_message": "三塊碎片在聖壇的魔力下融合在一起，形成了一顆完整的淨化水晶！",
                    "consume": False
                },
                "default": {
                    "message": "水晶碎片需要在神殿聖壇上才能合成完整水晶。",
                    "consume": False
                }
            }
        }
    },
    "完整水晶": {
        "stack": False,
        "desc": "完整的魔法水晶，蘊含強大的能量。",
        "en_name": "complete crystal",
        "use": {
            "type": "context",
            "contexts": {
                "ancient_well": {
                    "message": "你將淨化水晶投入古井，耀眼的光芒從井底爆發！黑暗的霧氣被光芒驅散，古井的封印恢復了平衡。迷霧森林的詛咒被徹底解除了！",
                    "consume": True
                },
                "sacred_altar": {
                    "message": "水晶在聖壇上發出柔和的光芒，但這裡不是使用它的地方。你需要將它帶到古井。",
                    "consume": False
                },
                "default": {
                    "message": "水晶發出耀眼的光芒，但需要在正確的地方才能發揮作用。",
                    "consume": False
                }
            }
        }
    },
    "靈魂容器": {
        "stack": False,
        "desc": "用於封印怨靈的古老容器。可在戰鬥中捕獲怨靈，或在聖所完成封印儀式。",
        "en_name": "soul vessel",
        "use": {
            "type": "context",
            "contexts": {
                "sanctum_altar": {
                    "message": "你將靈魂容器放在祭壇上，封印陣開始發光！容器中的怨靈被永久封印，沙漠的詛咒終於解除了...",
                    "consume": True,
                    "give_item": "淨化的靈魂水晶"
                },
                "default": {
                    "message": "靈魂容器微微震動，但需要在聖所的祭壇上才能完成封印。",
                    "consume": False
                }
            }
        }
    },
    "淨化的靈魂水晶": {
        "stack": False,
        "desc": "封印了怨靈力量的水晶，散發著聖潔的光芒。",
        "en_name": "purified soul crystal",
        "use": None
    }
}
