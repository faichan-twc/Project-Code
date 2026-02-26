# Worlds/Scenarios Data
from typing import List, Dict, Any
from .tutorial_data import TUTORIAL_WORLD
from .advanced_tutorial_data import ADVANCED_TUTORIAL_WORLD
from .qin_dynasty_data import QIN_WORLD

# 難度分級：1=新手, 2=簡單, 3=中等, 4=困難, 5=專家
# WORLDS 按難度排序（由簡單至困難）
WORLDS: List[Dict[str, Any]] = [
    TUTORIAL_WORLD,  # 難度 1 - 新手教學
    ADVANCED_TUTORIAL_WORLD,  # 難度 2 - 進階教學
    {
        "id": "forest",
        "name": "迷霧森林",
        "en_name": "Misty Forest",
        "difficulty": 3,  # 中等難度
        "cover_image": "forest.png",
        "opening": "濃霧如幕布般籠罩著整片森林，古樹的枝椏在白霧中扭曲成詭異的爪形。空氣冰冷刺骨，每一步都踩在濕滑的落葉上。村民們口耳相傳著一個警告：森林深處的古井封印著黑暗的力量，凡是接近者都會迷失在霧中。但作為冒險者，你知道——有些真相，只有勇者才能揭開。",
        "description": "薄霧籠罩的古老森林，樹影間隱藏著千年秘密。傳說中的古井封印著強大的黑暗力量，只有最勇敢的冒險者才能揭開真相。",
        "initial_inventory": [
            {"name": "火把", "qty": 1},
            {"name": "舊地圖", "qty": 1},
            {"name": "治療藥水", "qty": 2}
        ],
        "locations": {
            "grove": {
                "name": "林徑",
                "en_name": "Grove",
                "exits": ["fallen_log"],
                "ambient": ["濃密的白霧籠罩著森林入口，古老的樹木在霧中扭曲成詭異的形狀。地面覆蓋著厚厚的落葉，泥濘中交錯著人類和野獸的腳印。樹皮上的發光青苔在黑暗中散發著微弱綠光，遠處傳來野獸的低吼和不明的聲響。空氣中瀰漫著不自然的魔法氣息，前方的小徑通往森林更深處。\n\n可拾取：樹枝(Branch)、碎石(Rock)\n出口：倒木(Fallen Log)"],
                "spawns": ["wolf:0.5", "wild_dog:0.3", "spider:0.2"],
                "pickable_items": [
                    {"name": "樹枝", "qty": 2, "respawn": False},
                    {"name": "碎石", "qty": 3, "respawn": False}
                ],
                "clues": {
                    "樹": {
                        "en_name": "tree",
                        "search": "樹皮上有新鮮的抓痕，還沾著一些黑色的液體。這些痕跡似乎是某種大型生物留下的。",
                        "origin": "這些古樹已經生長了數百年，它們見證了森林中所有的秘密。"
                    },
                    "地面": {
                        "en_name": "ground",
                        "search": "地面上有多組腳印，有人類的也有野獸的。腳印向森林深處延伸，似乎有人在追蹤什麼。",
                        "method": "跟隨這些腳印，或許能找到失蹤的探險者。"
                    },
                    "霧": {
                        "en_name": "fog",
                        "search": "濃霧並非自然形成，它帶著一股冰冷的魔法氣息。霧氣似乎從森林深處湧出。",
                        "reason": "村民說，自從古井的封印減弱後，霧氣就開始籠罩整片森林。"
                    }
                }
            },
            "fallen_log": {
                "name": "倒木",
                "en_name": "Fallen Log",
                "exits": ["grove", "forest_depth"],
                "ambient": ["一棵數百年的巨樹橫倒在小徑上，樹幹上有深深的爪痕和焦黑痕跡。樹洞中散落著破碎的武器和乾涸的血跡，這裡曾發生過激烈戰鬥。倒木後的濃霧更加深沉，小徑延伸向森林最黑暗的深處，傳來冰冷的風和腐朽氣息。霧氣中時不時傳來樹枝斷裂聲和生物踩踏落葉的沙沙聲。\n\n可拾取：粗壯木棒(Wooden Club)、破損的劍(Broken Sword)\n出口：林徑(Grove)、森林深處(Forest Depth)"],
                "spawns": ["wolf:0.4", "spider:0.3"],
                "pickable_items": [
                    {"name": "粗壯木棒", "qty": 1, "respawn": False},
                    {"name": "破損的劍", "qty": 1, "respawn": False}
                ],
                "clues": {
                    "倒木": {
                        "en_name": "log",
                        "search": "樹幹被某種巨大的力量擊倒，斷口處還殘留著魔法的痕跡。樹洞中散落著破碎的武器。",
                        "origin": "這場戰鬥發生在不久前，參戰者似乎在尋找通往森林深處的路。"
                    },
                    "武器": {
                        "en_name": "weapon",
                        "search": "破碎的劍刃上刻著符文，屬於某個探險隊。旁邊還有一張濕透的地圖碎片。",
                        "method": "地圖上標記著『古井』的位置——在森林最深處。"
                    }
                }
            },
            "forest_depth": {
                "name": "森林深處",
                "en_name": "Forest Depth",
                "exits": ["fallen_log", "old_well", "temple_outer"],
                "ambient": ["這是森林最黑暗的區域，樹冠完全遮蔽天空，即使白天也昏暗如黃昏。枯死的樹木爬滿黑色藤蔓，空氣中瀰漫著腐朽和潮濕的氣味。遠處傳來規律的滴水聲指向古井方向，另一側隱約可見石造神殿的輪廓。地上有一條被頻繁使用的小徑，路旁破碎石碑上刻著模糊的警告文字。\n\n可拾取：骨頭(Bone)\n出口：倒木(Fallen Log)、古井(Old Well)、神殿外廊(Temple Outer Hall)"],
                "spawns": ["wraith:0.5", "zombie:0.3", "spider:0.2"],
                "pickable_items": [
                    {"name": "骨頭", "qty": 2, "respawn": False}
                ],
                "clues": {
                    "地面": {
                        "en_name": "ground",
                        "search": "地面覆蓋著厚厚的落葉，但你注意到有一條被頻繁使用的小徑通往古井。",
                        "origin": "這條路似乎是探險者們開闢的，他們都在尋找井中的秘密。"
                    },
                    "石碑": {
                        "en_name": "monument",
                        "search": "一塊破碎的石碑上刻著警告：『井中封印不可破，擾之則災厄降臨。』",
                        "reason": "古代村民在此立碑，警告後人不要打開古井的封印。",
                        "give_item": ["治療藥水"]
                    },
                    "樹": {
                        "en_name": "tree",
                        "search": "這裡的樹木都已枯死，樹幹上爬滿了發黑的藤蔓。這種腐化從古井方向蔓延而來。",
                        "method": "必須找到淨化森林的方法，或許古井中有答案。"
                    }
                }
            },
            "old_well": {
                "name": "古井",
                "en_name": "Old Well",
                "exits": ["forest_depth"],
                "ambient": ["小空地中央矗立著一口古老石井，井口由刻滿符文的巨大石板部分覆蓋，但已經鬆動。井壁覆蓋著發光的青苔，往下望去一片漆黑深不見底，井底傳來詭異的低語和呼吸聲。井口周圍散落著生鏽鐵鍊和儀式用具殘留，強大的黑暗力量從井中緩慢溢出擴散。這就是森林詛咒的源頭，符文石板的鬆動意味著封印正在減弱。\n\n出口：森林深處(Forest Depth)"],
                "spawns": [],
                "context": "ancient_well",
                "clues": {
                    "井": {
                        "en_name": "well",
                        "search": "井口的符文石板已經鬆動，封印正在減弱。井內一片漆黑，你需要光源才能看清井底。",
                        "origin": "這口井建於千年前，古代祭司用它封印了森林中的黑暗力量。",
                        "method": "使用火把照亮井底，或許能發現什麼。"
                    },
                    "符文": {
                        "en_name": "rune",
                        "search": "井口的符文記載著封印的方法：『以光驅暗，以水晶淨化，以森林精華重生。』",
                        "method": "你需要收集水晶碎片，在神殿聖壇合成完整水晶，才能徹底淨化古井。"
                    },
                    "水": {
                        "en_name": "water",
                        "search": "井水漆黑如墨，表面漂浮著黑色的霧氣。這不是普通的水，而是被詛咒污染的魔法之源。",
                        "reason": "封印減弱後，井中的黑暗力量開始擴散，污染了整片森林。"
                    }
                }
            },
            "temple_outer": {
                "name": "神殿外廊",
                "en_name": "Temple Outer Hall",
                "exits": ["forest_depth"],
                "locked_exits": {"temple_sanctum": "需要森林古鑰才能進入神殿聖所"},
                "ambient": ["森林最深處矗立著一座半毀的古代神殿，巨大石塊建造的外廊穹頂已部分坍塌。石柱上刻滿精美花紋和古代文字，爬滿藤蔓和苔蘚。神殿大門緊閉，門上雕刻著藍色發光符文，中央有精緻鑰匙孔，需要特殊鑰匙才能開啟。牆壁上的褪色壁畫描繪著祭司們手持水晶對抗黑暗的淨化儀式場景。空氣中有奇特的安寧感，這裡曾是封印古井的儀式中心。\n\n出口：森林深處(Forest Depth)"],
                "spawns": ["zombie:0.4", "wraith:0.3"],
                "context": "temple_entrance",
                "clues": {
                    "石柱": {
                        "en_name": "pillar",
                        "search": "石柱上刻著古老的儀式記錄：祭司們曾用水晶之力淨化森林，並將黑暗封印在古井中。",
                        "origin": "這座神殿是封印儀式的核心，聖壇上可以合成淨化水晶。"
                    },
                    "門": {
                        "en_name": "door",
                        "search": "神殿大門由古老的魔法鎖保護，需要『森林古鑰』才能開啟。",
                        "method": "古鑰應該就在古井附近，與井互動可能獲得線索。"
                    }
                }
            },
            "temple_sanctum": {
                "name": "神殿聖所",
                "en_name": "Temple Sanctum",
                "exits": ["temple_outer"],
                "ambient": ["圓形聖所的穹頂高聳，保持得相對完好。大廳中央的白色大理石聖壇上雕刻著太陽月亮星辰圖案，三個凹槽排列成三角形散發著微弱藍光。聖壇周圍漂浮著無數光點，空氣中瀰漫著純淨的魔法氣息。牆壁上色彩鮮艷的壁畫描繪著祭司們在聖壇合成淨化水晶、前往古井封印黑暗的完整儀式過程。大廳後方矗立著手持水晶杖的祭司石像，眼睛發著光——這是被賦予魔法生命的守護者，正靜靜評估著你。\n\n出口：神殿外廊(Temple Outer Hall)"],
                "spawns": ["ghost_guardian:0.8"],
                "context": "sacred_altar",
                "clues": {
                    "聖壇": {
                        "en_name": "altar",
                        "search": "聖壇上有三個凹槽，排列成三角形。凹槽邊緣刻著文字：『三片碎片，合而為一，光輝重現，森林重生。』",
                        "method": "收集三個水晶碎片放入凹槽，它們會自動融合成完整水晶。然後將完整水晶帶到古井，淨化封印。"
                    },
                    "壁畫": {
                        "en_name": "mural",
                        "search": "壁畫描繪了完整的儀式：祭司在聖壇合成淨化水晶，然後在古井使用水晶驅散黑暗。",
                        "origin": "這套儀式已經失傳千年，只有通過這些壁畫才能重現。"
                    }
                }
            }
        },
        "quests": [
            {
                "id": "q_misty_forest",
                "title": "迷霧森林的詛咒",
                "desc": "森林被濃霧籠罩，村民說詛咒源自森林深處的古井。你必須找到古井，揭開封印的秘密。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "grove"},
                "objectives": [
                    {"type": "REACH_LOCATION", "location": "old_well", "desc": "找到古井"},
                    {"type": "OBSERVE", "target": "井", "desc": "調查古井"},
                    {"type": "USE_ITEM", "item": "火把", "context": "ancient_well", "desc": "用火把照亮古井"},
                    {"type": "COLLECT_ITEM", "item": "森林古鑰", "qty": 1, "desc": "從古井獲得森林古鑰"},
                    {"type": "REACH_LOCATION", "location": "temple_outer", "desc": "前往神殿外廊"},
                    {"type": "USE_ITEM", "item": "森林古鑰", "context": "temple_entrance", "desc": "用古鑰開啟神殿大門"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "治療藥水", "qty": 2},
                    {"type": "giveItem", "name": "守護護符", "qty": 1}
                ]
            },
            {
                "id": "q_crystal_purification",
                "title": "淨化水晶",
                "desc": "收集三塊水晶碎片，在神殿聖壇合成完整的淨化水晶，然後用它淨化古井的封印。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "temple_sanctum"},
                "objectives": [
                    {"type": "COLLECT_ITEM", "item": "水晶碎片", "qty": 3, "desc": "收集3個水晶碎片（擊敗怨靈和守衛獲得）"},
                    {"type": "USE_ITEM", "item": "水晶碎片", "context": "sacred_altar", "desc": "將水晶碎片放在聖壇上"},
                    {"type": "COLLECT_ITEM", "item": "完整水晶", "qty": 1, "desc": "獲得完整的淨化水晶"},
                    {"type": "REACH_LOCATION", "location": "old_well", "desc": "返回古井"},
                    {"type": "USE_ITEM", "item": "完整水晶", "context": "ancient_well", "desc": "在古井使用淨化水晶，驅散詛咒"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "強效治療藥水", "qty": 3},
                    {"type": "giveItem", "name": "守護護符", "qty": 1}
                ]
            }
        ]
    },
    {
        "id": "desert",
        "name": "低語之沙",
        "en_name": "Whispering Sands",
        "difficulty": 4,  # 困難
        "cover_image": "desert.png",
        "opening": "烈日炙烤著金色的沙海，熱浪扭曲了地平線上的景象。遠處，海市蜃樓中浮現出古老神殿的輪廓，隨即又消失在風沙之中。沙漠的風似乎在低語，訴說著被時間遺忘的詛咒。商隊失蹤，探險者有去無回——但埋藏在黃沙下的秘密，正在召喚著新的挑戰者。",
        "description": "無盡沙海中迴盪著古老的低語。半埋的神殿、失蹤的商隊、被詛咒的怨靈——沙漠深處隱藏著危險與寶藏。",
        "initial_inventory": [
            {"name": "治療藥水", "qty": 2},
            {"name": "舊地圖", "qty": 1},
            {"name": "解毒草", "qty": 1}
        ],
        "locations": {
            "dune": {
                "name": "沙丘",
                "en_name": "Sand Dune",
                "exits": ["torn_tent", "stone_circle"],
                "ambient": ["金色沙丘連綿起伏，烈日炙烤下散發著扭曲的熱浪。腳下細沙隨風流動發出低沉沙沙聲，遠方地平線在熱氣中搖擺扭曲。風沙拍打著臉頰帶來灼熱，遠處有一頂破舊帳篷在風中搖曳，另一側則矗立著幾根奇特的石柱。\n\n可拾取：尖銳碎石(Sharp Rock)\n出口：破帳篷(Torn Tent)、石柱圈(Stone Circle)"],
                "spawns": ["scorpion:0.4", "wild_dog:0.3", "bandit:0.2"],
                "pickable_items": [
                    {"name": "尖銳碎石", "qty": 3, "respawn": False}
                ],
                "clues": {
                    "帳篷": {
                        "en_name": "tent",
                        "search": "遠處的破舊帳篷在風中搖晃，似乎是商隊遺留下來的。",
                        "origin": "許多商隊和探險者曾在此紮營，但大部分都失蹤了。"
                    },
                    "石柱": {
                        "en_name": "pillars",
                        "search": "遠方矗立的黑色石柱散發著不祥的氣息，它們排列成奇特的圓形。",
                        "reason": "傳說這些石柱是古代文明留下的遺跡，隱藏著強大的魔法力量。"
                    }
                }
            },
            "torn_tent": {
                "name": "破帳篷",
                "en_name": "Torn Tent",
                "exits": ["dune"],
                "ambient": ["廢棄的商隊帳篷布料褪色破洞，在風中無力拍打。帳篷內陰暗悶熱，地面散落著生鏽刀劍、空水袋和破碎木箱，都蓋著厚厚沙塵。帳篷一角被撕裂，露出外面刺眼陽光和起伏沙丘。這裡曾發生過什麼？商隊的人去了哪裡？\n\n可拾取：生鏽匕首(Rusty Dagger)\n出口：沙丘(Sand Dune)"],
                "spawns": ["bandit:0.4", "wild_dog:0.3"],
                "pickable_items": [
                    {"name": "生鏽匕首", "qty": 1, "respawn": False}
                ],
                "clues": {
                    "遺物": {
                        "en_name": "remains",
                        "search": "你在商隊遺物中找到探險家的日記和一些補給品！",
                        "give_item": ["破損的日記", "麻痺毒藥", "治療藥水"]
                    }
                }
            },
            "stone_circle": {
                "name": "石柱圈",
                "en_name": "Stone Circle",
                "exits": ["dune", "buried_temple"],
                "ambient": ["七根高聳黑色石柱圍成完美圓圈，柱身刻滿古老符文在陽光下閃爍微光。站在中央能感受到異樣能量流動，風吹過石柱發出遠古低語般的嗚咽聲。地面有燒焦痕跡和奇特圖案，暗示這裡曾舉行過神秘儀式。透過石柱縫隙可見遠處沙丘和半埋的神殿輪廓。\n\n出口：沙丘(Sand Dune)、埋沙神殿(Buried Temple)"],
                "spawns": ["wraith:0.5", "scorpion:0.2"],
                "context": "stone_circle",
                "clues": {
                    "符文": {
                        "en_name": "runes",
                        "search": "符文講述著一個關於沙漠怨靈和封印之力的古老傳說。",
                        "method": "或許古老的符文石能與這裡產生共鳴。"
                    }
                }
            },
            "buried_temple": {
                "name": "埋沙神殿",
                "en_name": "Buried Temple",
                "exits": ["stone_circle", "temple_inner"],
                "ambient": ["巨大石造神殿半埋沙海中，風化石牆上刻著精美浮雕描繪古代文明輝煌。高大拱門入口的黑暗門洞中吹出陣陣冷風，帶著腐朽和魔法氣息，與沙漠熱浪形成詭異對比。入口周圍沙地散落著破碎雕像殘骸和古老骨骸，神殿陰影在沙地上投下漆黑輪廓。深處傳來模糊聲音——是風聲，還是別的什麼？\n\n出口：石柱圈(Stone Circle)、神殿內部(Temple Inner)"],
                "spawns": ["zombie:0.4", "wraith:0.4"],
                "clues": {
                    "浮雕": {
                        "en_name": "relief",
                        "search": "牆上的浮雕描繪著古代法師舉行儀式的場景，他們似乎在封印某種強大的邪惡力量。",
                        "origin": "這座神殿是古代文明的遺跡，曾是封印怨靈的聖地。"
                    },
                    "骨骸": {
                        "en_name": "bones",
                        "search": "散落的骨骸有些已經風化，有些看起來還很新鮮。這裡曾有許多探險者葬身於此。",
                        "reason": "神殿被不死生物守護著，擅闖者很少能活著離開。"
                    }
                }
            },
            "temple_inner": {
                "name": "神殿內部",
                "en_name": "Temple Inner",
                "exits": ["buried_temple"],
                "locked_exits": {"sanctum": "需要沙漠神殿鑰匙才能進入聖所"},
                "ambient": ["神殿內部陰冷潮濕，幾乎沒有光線，只有入口微弱陽光照亮附近區域。高聳石柱支撐穹頂，牆壁上褪色壁畫描繪著古代法師進行神秘儀式的場景，空氣中瀰漫厚重塵埃和魔法氣息。深處矗立著刻滿封印符文的巨大石門，散發微弱藍光，中央有精緻鑰匙孔。角落堆放著古老木箱和破碎器皿，陰影中似乎還隱藏著什麼。\n\n出口：埋沙神殿(Buried Temple)"],
                "spawns": ["ghost_guardian:0.6", "wraith:0.4", "zombie:0.3"],
                "context": "temple_inner",
                "clues": {
                    "壁畫": {
                        "en_name": "mural",
                        "search": "壁畫描繪著古代法師使用靈魂容器封印怨靈的場景。",
                        "method": "靈魂容器或許能用來對付沙漠中的怨靈。你需要在更深處的聖所進行封印儀式。"
                    },
                    "寶箱": {
                        "en_name": "chest",
                        "search": "你在角落發現一個古老的寶箱！",
                        "give_item": ["古老符文石"]
                    },
                    "石門": {
                        "en_name": "stone door",
                        "search": "厚重的石門上刻著封印符文，門上有一個鑰匙孔。",
                        "method": "沙漠神殿鑰匙應該能打開這扇門。"
                    }
                }
            },
            "sanctum": {
                "name": "神殿聖所",
                "en_name": "Temple Sanctum",
                "exits": ["temple_inner"],
                "ambient": ["神殿最深處的圓形聖所穹頂高聳，牆壁鑲嵌著發光水晶提供幽暗藍光。空氣中瀰漫著濃厚魔法波動，強大到幾乎能看見魔力扭曲流動。大廳中央的黑色大理石祭壇刻滿複雜封印陣，散發脈動的暗紅色光芒，周圍地面畫著巨大魔法陣。祭壇前矗立著三米高的古代守護者石像，手持巨劍身披戰甲，眼睛閃爍不祥紅光，正注視著你。整個聖所充滿壓迫感，封印著強大而古老的力量。\n\n出口：神殿內部(Temple Inner)"],
                "spawns": ["ancient_guardian:0.9"],
                "context": "sanctum_altar",
                "clues": {
                    "祭壇": {
                        "en_name": "altar",
                        "search": "古老的祭壇上刻著封印陣，這裡曾是封印怨靈的地方。",
                        "method": "擊敗守護者後，使用靈魂容器在此處完成封印儀式。"
                    },
                    "石像": {
                        "en_name": "statue",
                        "search": "守護者石像高達三米，手持巨劍。它的眼睛閃爍著紅光——它還活著！",
                        "origin": "這是古代法師創造的守護者，用來保護聖所不被入侵。"
                    }
                }
            }
        },
        "quests": [
            {
                "id": "q_desert_mystery",
                "title": "沙漠的秘密",
                "desc": "探索沙漠遺跡，找到古老符文石，解開石柱圈的秘密。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "dune"},
                "objectives": [
                    {"type": "REACH_LOCATION", "location": "torn_tent", "desc": "探索破帳篷"},
                    {"type": "COLLECT_ITEM", "item": "破損的日記", "qty": 1, "desc": "從遺物中找到日記"},
                    {"type": "OBSERVE", "target": "符文", "desc": "前往石柱圈並調查石柱上的符文"},
                    {"type": "REACH_LOCATION", "location": "buried_temple", "desc": "找到埋沙神殿"},
                    {"type": "REACH_LOCATION", "location": "temple_inner", "desc": "進入神殿內部"},
                    {"type": "COLLECT_ITEM", "item": "古老符文石", "qty": 1, "desc": "從寶箱獲得符文石"},
                    {"type": "USE_ITEM", "item": "古老符文石", "context": "stone_circle", "desc": "返回石柱圈使用符文石"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "治療藥水", "qty": 2},
                    {"type": "giveItem", "name": "解毒草", "qty": 1}
                ]
            },
            {
                "id": "q_seal_wraith",
                "title": "封印怨靈",
                "desc": "使用沙漠神殿鑰匙進入聖所，擊敗古代守護者，完成封印儀式。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "stone_circle"},
                "objectives": [
                    {"type": "COLLECT_ITEM", "item": "沙漠神殿鑰匙", "qty": 1, "desc": "獲得沙漠神殿鑰匙"},
                    {"type": "USE_ITEM", "item": "沙漠神殿鑰匙", "context": "buried_temple", "desc": "使用鑰匙開啟神殿深處"},
                    {"type": "REACH_LOCATION", "location": "sanctum", "desc": "進入神殿聖所"},
                    {"type": "DEFEAT_ENEMY", "enemy": "ancient_guardian", "qty": 1, "desc": "擊敗古代守護者"},
                    {"type": "COLLECT_ITEM", "item": "靈魂容器", "qty": 1, "desc": "從守護者處獲得靈魂容器"},
                    {"type": "USE_ITEM", "item": "靈魂容器", "context": "sanctum_altar", "desc": "在聖所祭壇完成封印儀式"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "強效治療藥水", "qty": 2},
                    {"type": "giveItem", "name": "守護護符", "qty": 1},
                    {"type": "giveItem", "name": "淨化的靈魂水晶", "qty": 1}
                ]
            }
        ]
    },
    {
        "id": "ruins",
        "name": "遺忘之城",
        "en_name": "Forgotten Ruins",
        "difficulty": 4,  # 困难
        "cover_image": "ruins.png",
        "opening": "破碎的拱門在陰影中矗立，見證著曾經的輝煌。石柱傾倒，雕像殘缺，野草從裂縫中生長——這座城市曾是文明的巔峰，如今卻只剩死寂。牆上的浮雕訴說著一場災難，一個失敗的魔法實驗毀滅了整個王朝。寶藏還在，但守護它們的不僅是時間，還有那些永不安息的亡靈。",
        "description": "曾經輝煌的王國化為廢墟，斷壁殘垣間遊蕩著不死的守衛。失落的寶藏、禁忌的魔法、王室的秘密——等待著勇者發掘。",
        "initial_inventory": [
            {"name": "治療藥水", "qty": 1},
            {"name": "火把", "qty": 1},
            {"name": "舊地圖", "qty": 1}
        ],
        "locations": {
            "courtyard": {
                "name": "外庭",
                "en_name": "Courtyard",
                "exits": ["relief_corridor", "bell_tower"],
                "ambient": ["遺忘之城的外庭一片荒涼，斷裂石板路被野草覆蓋，中央乾涸噴泉的雕像殘缺不全。四周建築牆壁傾頹倒塌，倒塌石柱橫七豎八，藤蔓爬滿牆面。空氣中瀰漫死寂氣息，沒有鳥鳴蟲叫，只有風吹過殘破建築的呼嘯聲和遠處鐘塔的低沉嗡鳴。一條通道通往浮雕走廊，另一條通向鐘塔底部。\n\n可拾取：碎石(Rock)、骨頭(Bone)\n出口：浮雕廊(Relief Corridor)、鐘塔底(Bell Tower Base)"],
                "spawns": ["zombie:0.4", "spider:0.3", "wild_dog:0.2"],
                "pickable_items": [
                    {"name": "碎石", "qty": 3, "respawn": False},
                    {"name": "骨頭", "qty": 2, "respawn": False}
                ],
                "clues": {
                    "雕像": {
                        "en_name": "statue",
                        "search": "殘破的雕像描繪著一位威嚴的國王，手持權杖，眼神卻透著悲傷。",
                        "origin": "這是王國最後一位君主的雕像，他為了永生進行了禁忌的魔法實驗。"
                    }
                }
            },
            "relief_corridor": {
                "name": "浮雕廊",
                "en_name": "Relief Corridor",
                "exits": ["courtyard", "throne_hall"],
                "locked_exits": {"secret_vault": "浮雕中似乎隱藏著機關，需要找到開啟的方法"},
                "ambient": ["連接外庭和王座廳的長廊保留著昔日華美，兩側高牆刻滿精緻浮雕。浮雕描繪著城市輝煌歷史——建城奠基、加冕典禮、戰爭勝利、繁榮集市，國王和王后的形象反復出現。然而走廊盡頭畫風驟變，開始描繪王后病逝、國王悲痛、禁忌魔法儀式，最後是城市陷入死亡詛咒。陽光從破損屋頂射入投下斑駁光影。某些浮雕似乎可以移動，牆面有微小縫隙，暗示著隱藏的密室入口。\n\n出口：外庭(Courtyard)、王座廳(Throne Hall)"],
                "spawns": ["zombie:0.4", "wraith:0.3"],
                "context": "relief_corridor",
                "clues": {
                    "浮雕": {
                        "en_name": "relief",
                        "search": "浮雕描繪著國王加冕的場景，其中隱藏著精巧的機關。",
                        "method": "破損的日記中可能記載著開啟機關的秘密。",
                        "origin": "這些浮雕是王室工匠的傑作，用來保護密室的財寶。"
                    }
                }
            },
            "bell_tower": {
                "name": "鐘塔底",
                "en_name": "Bell Tower Base",
                "exits": ["courtyard"],
                "ambient": ["半毀的鐘塔外牆布滿巨大裂縫，向上可見破損螺旋樓梯懸掛半空中。塔頂懸掛著覆滿銅鏽和蛛網的巨大銅鐘，風吹過就微微搖晃，發出低沉悠長的嗡鳴聲在廢墟中迴盪。塔底散落著石塊和木頭碎片，地面深色裂縫中爬出蜘蛛，牆角堆積厚厚塵埃蛛網。鐘面刻著古老銘文，這座鐘曾為整座城市報時，見證王國興衰。\n\n出口：外庭(Courtyard)"],
                "spawns": ["spider:0.5", "scorpion:0.3"],
                "clues": {
                    "巨鐘": {
                        "en_name": "bell",
                        "search": "巨鐘上刻著銘文：「當三聲鐘響，王者將甦醒。」"
                    },
                    "碎石": {
                        "en_name": "rubble",
                        "search": "在倒塌的塔底旁，你發現一本滿是灰塵的日記，似乎是探險家遺落的。",
                        "give_item": ["破損的日記"]
                    }
                }
            },
            "throne_hall": {
                "name": "王座廳",
                "en_name": "Throne Hall",
                "exits": ["relief_corridor"],
                "locked_exits": {"underground_chamber": "需要王室印章才能開啟通往地下的密道"},
                "ambient": ["王座廳宏偉而空蕩，穹頂高達數十米，生鏽鐵鍊在風中搖擺發出吱呀聲。大廳盡頭高台上矗立著黑色大理石雕刻的王座，鑲嵌失去光澤的寶石，已經破裂，厚厚灰塵覆蓋一切。兩側牆壁掛著褪色掛毯，地面鋪著破損紅色地毯延伸到王座前，空氣中迴盪詭異回聲。牆上壁畫描繪王室最後的日子——國王絕望、王后逝去、禁忌魔法符號。王座後方牆壁有可疑痕跡，似乎隱藏秘密通道。\n\n出口：浮雕廊(Relief Corridor)"],
                "spawns": ["wraith:0.6", "zombie:0.3"],
                "context": "throne_room",
                "clues": {
                    "王座": {
                        "en_name": "throne",
                        "search": "破碎的王座後方有一道隱蔽的門，門上有印章的凹槽。",
                        "method": "王室印章應該能開啟這道門。"
                    },
                    "壁畫": {
                        "en_name": "mural",
                        "search": "壁畫記載著王室最後的日子：國王為了永生進行了禁忌的魔法實驗，卻將整座城市變成了死亡之地。",
                        "reason": "國王無法接受愛妻的逝去，不惜一切代價想要復活她，最終釀成大禍。"
                    }
                }
            },
            "secret_vault": {
                "name": "密室",
                "en_name": "Secret Vault",
                "exits": ["relief_corridor"],
                "ambient": ["隱藏的密室是王室最核心的秘密寶庫，雖然不大但堆滿珍貴物品。昏暗光線中成堆金幣寶石散落地上，沿牆檀木書架上整齊放著古老書籍和卷軸——記載失傳知識和禁忌魔法的秘密文獻。角落有上鎖寶箱雕刻精美王室紋章，牆上掛著法杖、權杖等儀式器物，空氣瀰漫羊皮紙氣味和魔法波動。天花板蹲伏著巨大石像鬼，眼睛閃爍邪惡紅光，這是王室設置的魔法守衛，正注視著你。\n\n出口：浮雕廊(Relief Corridor)"],
                "spawns": ["gargoyle:0.9", "wraith:0.2"],
                "clues": {
                    "寶箱": {
                        "en_name": "treasure",
                        "search": "你打開寶箱，發現了珍貴的王室遺物！",
                        "give_item": ["王室印章", "守護護符", "爆裂瓶"]
                    },
                    "文獻": {
                        "en_name": "documents",
                        "search": "古老的文獻記載著魔法實驗的真相：國王為了復活逝去的王后，使用了亡靈魔法，但儀式失控，詛咒了整座城市。",
                        "method": "文獻中提到，只有淨化聖水才能解除不死詛咒。",
                        "give_item": ["淨化聖水"]
                    }
                }
            },
            "underground_chamber": {
                "name": "地下密室",
                "en_name": "Underground Chamber",
                "exits": ["throne_hall"],
                "ambient": ["地底深處的圓形密室沒有自然光線，只有牆壁符文散發詭異紅光。從地面到穹頂刻滿密密麻麻的亡靈符文不斷閃爍，地面畫著由鮮血和黑色物質繪成的巨大魔法陣，散發強大邪惡魔力。大廳中央矗立著黑曜石雕刻的巨大石棺，鑲嵌暗紅色寶石，蓋子微微開啟溢出黑色霧氣。從石棺內傳來低沉的呼吸聲——沉重、緩慢，但充滿力量。空氣冰冷刺骨，瀰漫死亡腐朽氣息，四周擺放著儀式蠟燭、祭品殘骸和魔法器具。這裡就是國王進行永生儀式的地方，詛咒的源頭。石棺內的東西正在甦醒……\n\n出口：王座廳(Throne Hall)"],
                "spawns": ["undead_king:0.9"],
                "context": "underground_ritual",
                "clues": {
                    "石棺": {
                        "en_name": "sarcophagus",
                        "search": "石棺中躺著不死之王——曾經的統治者，如今的詛咒源頭。",
                        "origin": "國王在此進行了永生儀式，但代價是失去人性，成為不死生物。"
                    },
                    "符文": {
                        "en_name": "runes",
                        "search": "亡靈符文記載著儀式的過程，以及解除詛咒的方法。",
                        "method": "擊敗不死之王後，使用淨化聖水在此處完成淨化儀式。"
                    }
                }
            }
        },
        "quests": [
            {
                "id": "q_lost_kingdom",
                "title": "失落的王國",
                "desc": "探索遺忘之城的廢墟，找到開啟密室的方法，尋找王室的遺產。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "courtyard"},
                "objectives": [
                    {"type": "COLLECT_ITEM", "item": "破損的日記", "qty": 1, "desc": "找到探險家的日記"},
                    {"type": "REACH_LOCATION", "location": "relief_corridor", "desc": "前往浮雕廊"},
                    {"type": "OBSERVE", "target": "浮雕", "desc": "調查浮雕"},
                    {"type": "USE_ITEM", "item": "破損的日記", "context": "relief_corridor", "desc": "在浮雕廊使用日記開啟機關"},
                    {"type": "REACH_LOCATION", "location": "secret_vault", "desc": "進入密室"},
                    {"type": "COLLECT_ITEM", "item": "王室印章", "qty": 1, "desc": "從寶箱取得王室印章"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "強效治療藥水", "qty": 1},
                    {"type": "giveItem", "name": "解毒草", "qty": 1}
                ]
            },
            {
                "id": "q_undead_curse",
                "title": "不死的詛咒",
                "desc": "深入地下密室，面對不死之王，解除籠罩城市的詛咒。",
                "state": "NOT_STARTED",
                "start": {"trigger": "onEnter", "location": "secret_vault"},
                "objectives": [
                    {"type": "COLLECT_ITEM", "item": "淨化聖水", "qty": 1, "desc": "從文獻中找到淨化聖水"},
                    {"type": "REACH_LOCATION", "location": "throne_hall", "desc": "前往王座廳"},
                    {"type": "OBSERVE", "target": "王座", "desc": "調查王座後方的密道"},
                    {"type": "USE_ITEM", "item": "王室印章", "context": "throne_room", "desc": "使用王室印章開啟地下密道"},
                    {"type": "REACH_LOCATION", "location": "underground_chamber", "desc": "進入地下密室"},
                    {"type": "DEFEAT_ENEMY", "enemy": "undead_king", "qty": 1, "desc": "擊敗不死之王"},
                    {"type": "COLLECT_ITEM", "item": "王室權杖", "qty": 1, "desc": "從不死之王處獲得王室權杖"},
                    {"type": "USE_ITEM", "item": "淨化聖水", "context": "underground_ritual", "desc": "使用淨化聖水完成淨化儀式"}
                ],
                "rewards": [
                    {"type": "giveItem", "name": "強效治療藥水", "qty": 3},
                    {"type": "giveItem", "name": "守護護符", "qty": 1},
                    {"type": "giveItem", "name": "淨化的王冠", "qty": 1}
                ]
            }
        ]
    },
    QIN_WORLD  # 尋秦記：戰國風雲（專家級）
]
