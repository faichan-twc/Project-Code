# 游戏数据结构参考文档

本文档详细说明 FABLE 游戏的数据结构规范，用于创建新的游戏内容（道具、武器、敌人、世界场景）。

⚠️ **重要更新说明**：
- 任务目标按**顺序执行**，必须完成前置目标才能触发后续目标
- 任务启动时会检查玩家库存，已有的 COLLECT_ITEM 会计入进度
- 敌人技能仅支持5种类型（见敌人章节）
- 武器分为 `melee`（近战）和 `throwable`（投掷消耗型）
- 世界场景有**难度分级系统**（1-5级）

---

## 目录
1. [难度分级系统](#难度分级系统)
2. [武器（Weapons）](#武器weapons)
3. [道具（Items）](#道具items)
4. [敌人（Enemies）](#敌人enemies)
5. [世界场景（Worlds）](#世界场景worlds)

---

## 难度分级系统

### 难度等级定义

游戏中的世界场景按难度分为 5 个等级：

| 难度值 | 难度名称 | 图标 | 说明 | 敌人HP范围 | 推荐玩家 |
|-------|---------|------|------|-----------|---------|
| **1** | 新手 | ⭐ | 简单的教学关卡，敌人弱小 | 20-40 | 首次游玩 |
| **2** | 简单 | ⭐⭐ | 轻松的冒险，适合熟悉系统 | 30-60 | 了解基础 |
| **3** | 中等 | ⭐⭐⭐ | 标准难度，需要一定策略 | 45-80 | 熟练玩家 |
| **4** | 困难 | ⭐⭐⭐⭐ | 挑战性强，需要合理规划 | 60-120 | 高级玩家 |
| **5** | 专家 | ⭐⭐⭐⭐⭐ | 极限挑战，强力BOSS战 | 75-220 | 精通玩家 |

### 难度评估标准

创建新世界时，根据以下因素综合评估难度：

1. **敌人强度**：
   - 普通敌人 HP 和攻击力
   - BOSS 数量和强度
   - 特殊技能复杂度

2. **任务复杂度**：
   - 任务步骤数量
   - 解谜难度
   - 多重目标

3. **资源管理**：
   - 初始道具数量
   - 治疗道具获取难度
   - 经济系统

4. **战术要求**：
   - 是否需要攻击身体部位
   - 是否有无法逃跑的战斗
   - 是否需要特定道具组合

### 现有世界难度

- **迷霧森林 (Misty Forest)** - 难度 3 (中等)
  - 中等强度敌人（45-80 HP）
  - 标准任务链（7步）
  - 适合熟练玩家

- **低語之沙 (Whispering Sands)** - 难度 4 (困难)
  - 较强敌人和复杂任务
  - 多个困难战斗
  - 需要策略规划

- **尋秦記：戰國風雲 (A Step Into The Past)** - 难度 5 (专家)
  - 高强度BOSS战（180-220 HP）
  - 复杂13步任务链
  - 无法逃跑的决战
  - 需要高级战术

### 在世界数据中使用

```python
{
    "id": "world_id",
    "name": "世界名称",
    "en_name": "World Name",
    "difficulty": 3,  # 1=新手, 2=简单, 3=中等, 4=困难, 5=专家
    "cover_image": "image.png",
    # ... 其他字段
}
```

**注意事项**：
- `difficulty` 字段为必需，范围 1-5
- 游戏选单将按难度从低到高排序显示
- 难度会影响玩家期望和游戏体验

---

## 武器（Weapons）

### 基础结构
```python
"武器名称": {
    "damage_bonus": int,        # 攻击力加成（必需）
    "desc": str,         # 描述文本（必需）
    "en_name": str,            # 英文名称（必需）
    "type": str                # 武器类型："melee" 或 "throwable"（可选，默认 melee）
}
```

### 武器类型

#### 1. `type: "melee"` - 近战武器（默认）
- 不会被消耗，可重复使用
- 适合：剑、斧、锤、法杖等

**示例**：
```python
"粗壯木棒": {
    "damage_bonus": 3,
    "desc": "結實的木棒，適合揮擊",
    "en_name": "Wooden Club",
    "type": "melee"
}
```

#### 2. `type: "throwable"` - 投掷武器
- 使用后从背包中消耗1个
- 适合：石头、飞刀、弓箭等

**示例**：
```python
"碎石": {
    "damage_bonus": 1,
    "desc": "粗糙的石頭，可以用來投擲或近戰",
    "en_name": "Rock",
    "type": "throwable"
}
```

### 完整武器示例

```python
# 可拾取的简易武器
"樹枝": {
    "damage_bonus": 1,
    "desc": "乾枯的樹枝，脆弱但能用來防身",
    "en_name": "Branch",
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
}
```

---

## 道具（Items）

### 基础结构
```python
"道具名称": {
    "stack": bool,              # 是否可堆叠（必需）
    "desc": str,                # 描述文本（必需）
    "en_name": str,             # 英文名称（必需）
    "use": dict | None          # 使用效果配置（可选）
}
```

### Use 类型详解

#### 1. `type: "heal"` - 治疗类
```python
"use": {
    "type": "heal",
    "value": int,              # 治疗量
    "consume": bool,           # 是否消耗
    "trigger_enemy": bool      # 是否触发敌人遭遇
}
```
**示例**：
```python
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
}
```

#### 2. `type: "buff"` - 增益类
```python
"use": {
    "type": "buff",
    "buff": str,               # 增益类型：atkUp, critUp, evasion
    "value": int | float,      # 增益数值
    "duration": int,           # 持续回合数
    "consume": bool,
    "trigger_enemy": bool,
    "message": str             # 使用时显示的消息（可选）
}
```
**示例**：
```python
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
}
```

#### 3. `type: "combat"` - 战斗类
```python
"use": {
    "type": "combat",
    "damage": [int, int],      # 伤害范围 [最小, 最大]（可选）
    "special": str,            # 特殊效果（可选）
    "consume": bool,
    "trigger_enemy": bool,
    "combat_only": bool,       # 是否仅战斗中可用
    "message": str
}
```
**特殊效果**：
- `"capture_wraith"` - 捕获怨灵

**示例**：
```python
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
}
```

#### 4. `type: "weapon_buff"` - 武器增益类
```python
"use": {
    "type": "weapon_buff",
    "debuff": dict,            # 武器附加的减益效果
    "duration": int,           # 持续攻击次数
    "consume": bool,
    "trigger_enemy": bool,
    "message": str
}
```
**Debuff 类型**：
- `"poison"`: int - 中毒回合数
- `"slow"`: int - 减速回合数
- `"bleed"`: int - 流血回合数
- `"confusion"`: int - 混乱回合数

**示例**：
```python
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
}
```

#### 5. `type: "cleanse"` - 净化类
```python
"use": {
    "type": "cleanse",
    "cleanse": list[str],      # 要清除的减益类型列表
    "consume": bool,
    "trigger_enemy": bool,
    "message": str
}
```
**示例**：
```python
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
}
```

#### 6. `type: "context"` - 场景交互类
```python
"use": {
    "type": "context",
    "contexts": {
        "context_name": {
            "message": str,                    # 使用时的消息
            "consume": bool,                   # 是否消耗
            "give_item": str,                  # 给予的道具（可选）
            "one_time_give": bool,             # 是否只给一次（默认True）
            "unlock_location": str,            # 解锁的地点（可选）
            "requires": list[dict],            # 需要的道具（可选）
            "remove_items": list[dict],        # 移除的道具（可选）
            "craft_message": str               # 合成消息（可选）
        },
        "default": {
            "message": str,
            "consume": bool
        }
    }
}
```

**Requires/Remove_items 格式**：
```python
"requires": [{"item": "道具名", "qty": 数量}]
"remove_items": [{"item": "道具名", "qty": 数量}]
```

**示例1 - 钥匙开门**：
```python
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
}
```

**示例2 - 合成配方**：
```python
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
}
```

**示例3 - 获得道具**：
```python
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
}
```

---

## 敌人（Enemies）

### 基础结构
```python
"enemy_id": {
    "name": str,                    # 中文名称（必需）
    "en_id": str,                   # 英文ID（必需）
    "maxhp": int,                   # 最大生命值（必需）
    "baseAtk": int,                 # 基础攻击力（必需）
    "is_boss": bool,                # 是否为BOSS（可选，默认False）
    "hint": str,                    # 提示文本（可选）
    "skills": dict,                 # 技能列表（必需）
    "drops": list[dict],            # 掉落物品（可选）
    "body_parts": dict,             # 身体部位（可选）
    "dialogues": dict               # 对话（可选）
}
```

**BOSS 特性**：
- 设置 `"is_boss": True` 的敌人无法逃跑
- BOSS通常拥有更高的生命值、更强的技能和更好的掉落物品
- 建议BOSS拥有 `hint` 字段提供战斗提示

### Skills 结构详解

**⚠️ 重要：游戏引擎仅支持以下5种技能类型**

#### ✅ 1. 基础攻击技能（带可选减益/吸血）
```python
"skill_key": {
    "name": str,                    # 技能名称
    "dmg": [int, int],             # 伤害范围 [最小, 最大]
    "cd": int,                      # 冷却回合数（可选，默认0）
    "lifesteal": float,            # 生命偷取比例（可选，0.0-1.0）
    "debuff": dict                 # 附加减益（可选）
}
```

**Debuff 类型**（可附加在攻击技能上）：
- `"poison"`: int - 中毒回合数
- `"slow"`: int - 减速回合数
- `"bleed"`: int - 流血回合数
- `"confusion"`: int - 混乱回合数
- `"curse"`: int - 诅咒回合数

**示例**：
```python
"death_strike": {
    "name": "死亡之擊",
    "dmg": [18, 26],
    "debuff": {"curse": 2}
}
```

#### ✅ 2. 吸血攻击技能
```python
"soul_drain": {
    "name": "靈魂吸取",
    "dmg": [15, 22],
    "lifesteal": 0.5,              # 吸取50%伤害作为生命值
    "cd": 3
}
```

#### ✅ 3. 增益技能（Buff）
```python
"skill_key": {
    "name": str,
    "buff": dict,                   # 增益效果
    "cd": int
}
```

**支持的 Buff 类型**：
- `"critUp"`: int - 暴击增加回合数
- `"evasion"`: float - 闪避率提升（0.0-1.0）
- `"enrage"`: int - 狂暴状态回合数
- `"atkUp"`: int - 攻击力提升回合数

**示例**：
```python
"undead_wrath": {
    "name": "不死之怒",
    "buff": {"enrage": 3, "critUp": 3},
    "cd": 4
}
```

#### ✅ 4. 眩晕技能（Stun）
```python
"skill_key": {
    "name": str,
    "stun": int,                    # 眩晕回合数
    "cd": int
}
```

**眩晕机制说明**：
- 玩家被眩晕时无法执行任何动作（攻击、防御、使用道具、逃跑）
- 眩晕计数在玩家尝试行动时减少1
- 当剩余回合数为0时，下一回合恢复正常
- 示例：眩晕1回合 = 跳过1次玩家回合

**示例**：
```python
"stone_gaze": {
    "name": "石化凝視",
    "stun": 1,                      # 玩家跳过1次行动
    "cd": 3
}

"荒嘯": {
    "name": "荒嘯",
    "stun": 2,                      # 玩家跳过2次行动
    "cd": 5
}
```

#### ✅ 5. 复合攻击技能（伤害+减益）
```python
"sand_storm": {
    "name": "沙塵風暴",
    "dmg": [18, 25],
    "debuff": {"bleed": 2},
    "cd": 3
}
```

---

### ❌ 不支持的技能类型

以下技能类型**不被游戏引擎支持**，请勿使用：

- ❌ `summon` - 召唤生物
- ❌ `heal` - 敌人自我治疗
- ❌ `shield` - 护盾效果
- ❌ `teleport` - 传送
- ❌ `transform` - 变身

### 完整敌人示例

**简单敌人（基础攻击+增益）**：
```python
"wolf": {
    "name": "影牙狼",
    "en_id": "wolf",
    "maxhp": 45,
    "baseAtk": 10,
    "hint": "狼群通常成群活動，小心被包圍。",
    "skills": {
        "bite": {
            "name": "撕咬",
            "dmg": [8, 14]              # ✅ 基础攻击
        },
        "howl": {
            "name": "號召嚎叫",
            "buff": {"critUp": 2},       # ✅ 增益技能
            "cd": 3
        },
        "pounce": {
            "name": "撲擊",
            "dmg": [14, 20],             # ✅ 高伤害攻击
            "cd": 3
        }
    },
    "drops": [
        {"item": "狼牙", "qty": 1, "chance": 1.0}
    ]
}
```

**Boss敌人（多种技能类型）**：
```python
"undead_king": {
    "name": "不死之王",
    "en_id": "undead_king",
    "is_boss": True,                 # ✅ BOSS标记（无法逃跑）
    "maxhp": 150,
    "baseAtk": 20,
    "hint": "強大的不死生物，擁有多種致命技能。",
    "skills": {
        "death_strike": {
            "name": "死亡之擊",
            "dmg": [18, 26],
            "debuff": {"curse": 2}       # ✅ 攻击+减益
        },
        "soul_drain": {
            "name": "靈魂吸取",
            "dmg": [15, 22],
            "lifesteal": 0.5,            # ✅ 吸血攻击
            "cd": 3
        },
        "undead_wrath": {
            "name": "不死之怒",
            "buff": {"enrage": 3, "critUp": 3},  # ✅ 多重增益
            "cd": 4
        },
        "death_aura": {
            "name": "死亡光環",
            "dmg": [20, 30],
            "debuff": {"poison": 3},     # ✅ 高伤害+中毒
            "cd": 5
        }
    },
    "drops": [
        {"item": "王室權杖", "qty": 1, "chance": 1.0},
        {"item": "強效治療藥水", "qty": 2, "chance": 0.8}
    ],
    "body_parts": {
        "王冠": {
            "en_name": "crown",
            "damage_multiplier": 2.2,
            "chance": 0.15,
            "special": "stun"
        },
        "權杖": {
            "en_name": "scepter",
            "damage_multiplier": 1.8,
            "chance": 0.25,
            "special": "disarm"
        }
    },
    "dialogues": {
        "low_hp": [
            "「永生...這就是永生的代價嗎...」"
        ],
        "enraged": [
            "「夠了！你們這些凡人！」"
        ]
    }
}
```

**带眩晕的敌人**：
```python
"gargoyle": {
    "name": "石像鬼",
    "en_id": "gargoyle",
    "maxhp": 65,
    "baseAtk": 13,
    "skills": {
        "dive": {
            "name": "俯衝攻擊",
            "dmg": [12, 18]              # ✅ 基础攻击
        },
        "stone_gaze": {
            "name": "石化凝視",
            "stun": 1,                   # ✅ 眩晕技能
            "cd": 3
        },
        "wing_slash": {
            "name": "翼刃斬擊",
            "dmg": [10, 16],
            "cd": 2
        }
    }
}
```

### Body Parts 结构
```python
"部位名称": {
    "en_name": str,                # 英文名称
    "damage_multiplier": float,    # 伤害倍数
    "chance": float,               # 触发特殊效果概率（0.0-1.0）
    "special": str                 # 特殊效果
}
```

**特殊效果列表**：
- `"blind"` - 降低闪避
- `"stun"` - 眩晕1回合
- `"slow"` - 减速
- `"instant_kill"` - 即死
- `"immobilize"` - 眩晕2回合
- `"disarm"` - 降低攻击力50%
- `"venom_burst"` - 玩家中毒
- `"remove_poison"` - 清除玩家中毒
- `"disperse"` - 清除闪避
- `"ground"` - 大幅降低闪避
- `"crack"` - 降低防御
- `"banish"` - 生命降至30%

### Drops 结构
```python
{"item": str, "qty": int, "chance": float}
```
- `item`: 道具名称
- `qty`: 数量
- `chance`: 掉落概率（0.0-1.0）

---

## 世界场景（Worlds）

### 基础结构
```python
{
    "id": str,                      # 场景ID（必需）
    "name": str,                    # 中文名称（必需）
    "en_name": str,                 # 英文名称（必需）
    "difficulty": int,              # 难度等级 1-5（必需）
    "cover_image": str,             # 封面图片（可选）
    "opening": str,                 # 开场白（必需）
    "description": str,             # 描述（必需）
    "initial_inventory": list[dict], # 初始物品（必需）
    "locations": dict,              # 地点列表（必需）
    "quests": list[dict]            # 任务列表（必需）
}
```

**难度等级说明**：
- `difficulty`: 1=新手, 2=简单, 3=中等, 4=困难, 5=专家
- 此字段影响游戏选单中的排序和显示
- 详细标准请参考[难度分级系统](#难度分级系统)

### Initial Inventory 结构
```python
"initial_inventory": [
    {"name": "道具名", "qty": 数量},
    {"name": "道具名", "qty": 数量}
]
```

**示例**：
```python
"initial_inventory": [
    {"name": "火把", "qty": 1},
    {"name": "舊地圖", "qty": 1},
    {"name": "治療藥水", "qty": 2}
]
```

### Locations 结构
python
"location_id": {
    "name": str,                    # 中文名称（必需）
    "en_name": str,                 # 英文名称（必需）
    "exits": list[str],             # 出口列表（必需）
    "locked_exits": dict,           # 锁定的出口（可选）
    "ambient": list[str],           # 环境描述（必需）
    "spawns": list[str],            # 敌人生成（可选）
    "context": str,                 # 场景上下文（可选）
    "clues": dict                   # 线索/可调查对象（可选）
}
```

#### Locked Exits 结构
```python
"locked_exits": {
    "location_id": "提示消息"
}
```

**示例**：
```python
"locked_exits": {"temple_sanctum": "需要森林古鑰才能進入神殿聖所"}
```

#### Spawns 结构
```python
"spawns": ["enemy_id:概率", "enemy_id:概率"]
```
- 概率为0.0-1.0之间的浮点数
- 多个敌人的概率会累加

**示例**：
```python
"spawns": ["wolf:0.5", "wild_dog:0.3", "spider:0.2"]
```

#### Pickable Items 结构
```python
"pickable_items": [
    {"name": str, "qty": int, "respawn": bool}
]
```
- `name`: 道具或武器名称（必须在items.py或weapons.py中定义）
- `qty`: 数量
- `respawn`: 是否重生（通常为False，一次性拾取）

**示例**：
```python
"pickable_items": [
    {"name": "樹枝", "qty": 2, "respawn": False},
    {"name": "碎石", "qty": 3, "respawn": False},
    {"name": "治療藥水", "qty": 1, "respawn": False}
]
```

#### Clues 结构
```python
"clues": {
    "对象名称": {
        "en_name": str,            # 英文名称（必需）
        "search": str,             # OBSERVE时显示（必需）
        "origin": str,             # QUESTION origin时显示（可选）
        "reason": str,             # QUESTION reason时显示（可选）
        "method": str,             # QUESTION method时显示（可选）
        "give_item": list[str]     # 给予的道具（可选）
    }
}
```

**示例**：
```python
"clues": {
    "樹": {
        "en_name": "tree",
        "search": "樹皮上有新鮮的抓痕，還沾著一些黑色的液體。這些痕跡似乎是某種大型生物留下的。",
        "origin": "這些古樹已經生長了數百年，它們見證了森林中所有的秘密。"
    },
    "石碑": {
        "en_name": "monument",
        "search": "一塊破碎的石碑上刻著警告：『井中封印不可破，擾之則災厄降臨。』",
        "reason": "古代村民在此立碑，警告後人不要打開古井的封印。",
        "give_item": ["治療藥水"]
    }
}
```

### 完整Location示例

```python
"grove": {
    "name": "林徑",
    "en_name": "Grove",
    "exits": ["fallen_log"],
    "ambient": ["你踏入迷霧森林的入口，濃霧讓視線只能看到幾步之外。古老的樹木在霧中若隱若現，樹皮上纏繞著發光的青苔。\n遠處傳來野獸的低吼，還有樹葉被踩碎的聲音。地面上的腳印指向更深處。\n\n出口：倒木"],
    "spawns": ["wolf:0.5", "wild_dog:0.3", "spider:0.2"],
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
        }
    },
    "pickable_items": [
        {"name": "樹枝", "qty": 2, "respawn": False},
        {"name": "碎石", "qty": 3, "respawn": False},
        {"name": "治療藥水", "qty": 1, "respawn": False}
    ]
}
```

### Quests 结构

⚠️ **任务系统重要特性**：
1. **顺序执行**：目标必须按顺序完成，后续目标在前置目标未完成前不会触发
2. **库存初始化**：任务启动时会检查玩家背包，已有的 COLLECT_ITEM 物品会计入进度
3. **示例**：如果任务需要收集3个水晶碎片，玩家背包已有2个，任务启动后显示 2/3

```python
{
    "id": str,                      # 任务ID（必需）
    "title": str,                   # 任务标题（必需）
    "desc": str,                    # 任务描述（必需）
    "state": str,                   # 初始状态（必需，通常为"NOT_STARTED"）
    "start": dict,                  # 触发条件（必需）
    "objectives": list[dict],       # 目标列表（必需，按顺序执行）
    "rewards": list[dict]           # 奖励列表（必需）
}
```

#### Start 结构
```python
"start": {
    "trigger": str,                 # 触发类型："onEnter"
    "location": str                 # 触发地点ID
}
```

#### Objectives 类型

**1. REACH_LOCATION - 到达地点**
```python
{
    "type": "REACH_LOCATION",
    "location": str,                # 地点ID
    "desc": str                     # 描述
}
```

**2. DEFEAT_ENEMY - 击败敌人**
```python
{
    "type": "DEFEAT_ENEMY",
    "enemy": str,                   # 敌人ID（可选，不填则任意敌人）
    "qty": int,                     # 数量（可选，默认1）
    "desc": str
}
```

**3. COLLECT_ITEM - 收集道具**
```python
{
    "type": "COLLECT_ITEM",
    "item": str,                    # 道具名称
    "qty": int,                     # 数量
    "desc": str
}
```

**4. USE_ITEM - 使用道具**
```python
{
    "type": "USE_ITEM",
    "item": str,                    # 道具名称
    "context": str,                 # 需要的场景上下文（可选）
    "desc": str
}
```

**5. OBSERVE - 观察对象**
```python
{
    "type": "OBSERVE",
    "target": str,                  # 目标对象名称
    "desc": str
}
```

#### Rewards 结构
```python
{
    "type": "giveItem",
    "name": str,                    # 道具名称
    "qty": int                      # 数量
}
```

### 完整Quest示例

**示例：顺序执行的任务**
```python
{
    "id": "q_misty_forest",
    "title": "迷霧森林的詛咒",
    "desc": "森林被濃霧籠罩，村民說詛咒源自森林深處的古井。你必須找到古井，揭開封印的秘密。",
    "state": "NOT_STARTED",
    "start": {"trigger": "onEnter", "location": "grove"},
    "objectives": [
        # 目标0: 必须先完成
        {"type": "REACH_LOCATION", "location": "old_well", "desc": "找到古井"},
        # 目标1: 必须等目标0完成后才能触发
        {"type": "OBSERVE", "target": "井", "desc": "調查古井"},
        # 目标2: 必须等目标0和1都完成
        {"type": "USE_ITEM", "item": "火把", "context": "ancient_well", "desc": "用火把照亮古井"},
        # 目标3: 必须等目标0-2都完成（COLLECT_ITEM会从背包初始化进度）
        {"type": "COLLECT_ITEM", "item": "森林古鑰", "qty": 1, "desc": "從古井獲得森林古鑰"},
        # 目标4: 必须等前面所有目标完成
        {"type": "REACH_LOCATION", "location": "temple_outer", "desc": "前往神殿外廊"},
        # 目标5: 最后一个目标
        {"type": "USE_ITEM", "item": "森林古鑰", "context": "temple_entrance", "desc": "用古鑰開啟神殿大門"}
    ],
    "rewards": [
        {"type": "giveItem", "name": "治療藥水", "qty": 2},
        {"type": "giveItem", "name": "守護護符", "qty": 1}
    ]
}
```

**示例：COLLECT_ITEM 库存初始化**
```python
{
    "id": "q_crystal_purification",
    "title": "淨化水晶",
    "desc": "收集三塊水晶碎片，在神殿聖壇合成完整的淨化水晶。",
    "state": "NOT_STARTED",
    "start": {"trigger": "onEnter", "location": "temple_sanctum"},
    "objectives": [
        # 如果玩家背包已有2个水晶碎片，任务启动时会显示 2/3
        {"type": "COLLECT_ITEM", "item": "水晶碎片", "qty": 3, "desc": "收集3個水晶碎片"},
        {"type": "USE_ITEM", "item": "水晶碎片", "context": "sacred_altar", "desc": "將水晶碎片放在聖壇上"},
        {"type": "COLLECT_ITEM", "item": "完整水晶", "qty": 1, "desc": "獲得完整的淨化水晶"},
        {"type": "REACH_LOCATION", "location": "old_well", "desc": "返回古井"},
        {"type": "USE_ITEM", "item": "完整水晶", "context": "ancient_well", "desc": "在古井使用淨化水晶"}
    ],
    "rewards": [
        {"type": "giveItem", "name": "強效治療藥水", "qty": 3}
    ]
}
```

---

## 完整World示例

```python
{
    "id": "forest",
    "name": "迷霧森林",
    "en_name": "Misty Forest",
    "difficulty": 3,  # 中等难度
    "cover_image": "forest.png",
    "opening": "濃霧籠罩著森林，樹影在霧中扭曲成詭異的形狀。村民說，森林深處的古井封印著某種力量，只有勇敢的冒險者才能揭開真相。",
    "description": "薄霧瀰漫的古老森林，隱藏著被遺忘的秘密。傳說森林深處有一口古井，井底封印著森林的核心力量。",
    "initial_inventory": [
        {"name": "火把", "qty": 1},
        {"name": "舊地圖", "qty": 1},
        {"name": "治療藥水", "qty": 2}
    ],
    "locations": {
        # ... (见上文Location示例)
    },
    "quests": [
        # ... (见上文Quest示例)
    ]
}
```

---

## 注意事项

### 1. 命名规范
- 中文名称使用繁体中文
- 英文名称使用小写，多个单词用空格分隔
- ID使用snake_case格式

### 2. Context 一致性
- 道具的context必须与location的context匹配
- 任务目标中的context必须与道具use配置中的context一致

**示例**：
```python
# Location
"old_well": {
    "context": "ancient_well"
}

# Item
"火把": {
    "use": {
        "contexts": {
            "ancient_well": {...}  # 匹配
        }
    }
}

# Quest
{"type": "USE_ITEM", "item": "火把", "context": "ancient_well"}  # 匹配
```

### 3. 引用完整性
- 所有道具名称、敌人ID、地点ID必须在对应数据文件中定义
- Quest objectives中引用的item必须在items.py中存在
- Location的exits必须是有效的location_id
- Spawns中的敌人ID必须在enemies.py中存在

### 4. 数值平衡
- 玩家初始生命值：100
- 敌人生命值建议：30-80（普通）、80-150（精英）
- 治疗道具：15-60 HP
- 敌人伤害：6-18（普通攻击）、15-25（技能）

### 5. 概率设定
- 掉落概率：0.3-0.8（常见物品）、0.1-0.3（稀有物品）
- 敌人生成概率：总和不超过1.0
- 身体部位特殊效果概率：0.1-0.5

---

## 数据验证清单

创建新内容时，请确保：

- [ ] 所有必需字段都已填写
- [ ] 中英文名称都已提供
- [ ] Context名称在道具、地点、任务间保持一致
- [ ] 所有引用的ID都已定义
- [ ] 技能冷却时间合理（2-5回合）
- [ ] 伤害数值平衡
- [ ] 任务目标顺序逻辑正确
- [ ] 地点出口双向连通
- [ ] 初始物品数量适中（3-5个）

---

## 常见错误

### ❌ 错误示例1：Context不匹配
```python
# Location
"context": "temple_entrance"

# Item (错误)
"contexts": {
    "temple_sanctum": {...}  # 不匹配！
}
```

### ❌ 错误示例2：引用不存在的道具
```python
# Quest (错误)
{"type": "COLLECT_ITEM", "item": "魔法寶石", ...}  # items.py中不存在
```

### ❌ 错误示例3：出口不存在
```python
# Location (错误)
"exits": ["nonexistent_location"]  # 该location_id不存在
```

### ✅ 正确示例
```python
# 1. Context匹配
"context": "ancient_well"  # Location
"contexts": {"ancient_well": {...}}  # Item

# 2. 道具存在
items.py中定义："森林古鑰": {...}
任务中引用："item": "森林古鑰"

# 3. 出口存在
locations中定义："fallen_log": {...}
其他location的exits: ["fallen_log"]
```

---

## 附录：系统支持的所有参数

### Buff/Debuff类型
- `critUp` (int) - 暴击提升
- `evasion` (float) - 闪避率
- `enrage` (bool) - 狂暴
- `poison` (int) - 中毒
- `slow` (int) - 减速
- `bleed` (int) - 流血
- `confusion` (int) - 混乱

### 特殊效果类型
- 身体部位特殊效果（见Body Parts部分）
- 道具特殊效果：`capture_wraith`

### 任务目标类型
- `REACH_LOCATION`
- `DEFEAT_ENEMY`
- `COLLECT_ITEM`
- `USE_ITEM`
- `OBSERVE`

### 道具使用类型
- `heal`
- `buff`
- `combat`
- `weapon_buff`
- `cleanse`
- `context`

---

**版本**: 2.1  
**最后更新**: 2026-01-21  
**兼容版本**: FABLE v1.0+

**主要更新**：
- **v2.1 (2026-01-21)**: 添加难度分级系统（1-5级），世界按难度排序
- **v2.0 (2026-01-21)**: 添加武器系统说明（melee/throwable类型）
- **v2.0**: 更新任务系统（顺序执行、库存初始化）
- **v2.0**: 明确敌人技能仅支持5种类型
- **v2.0**: 更新所有示例为当前游戏数据
