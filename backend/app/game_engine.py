# Game Engine - Combat, Inventory, Quest Management
import random
import os
from typing import Optional, Dict, List
from app.models import GameState, Enemy, Item, Quest, QuestState, Buff
from app.game_data import GameData
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AzureOpenAI = None

class GameEngine:
    def __init__(self):
        self.data = GameData()
        self.sessions: Dict[str, GameState] = {}
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE:
            token = os.getenv("OPENAI_API_KEY")
            endpoint = os.getenv("OPENAI_API_BASE_URL")
            if token and endpoint:
                self.openai_client = OpenAI(
                    base_url=endpoint,
                    api_key=token,
                )
    
    def generate_text_map(self, state: GameState) -> str:
        """Generate ASCII text map using AI based on current location and world structure"""
        if not self.openai_client:
            return "⚠️ 地圖功能暫時無法使用（未配置 API 金鑰或 OpenAI 套件未安裝）。"
        
        world = self.get_current_world(state)
        locations = world.get("locations", {})
        current_location = state.location_id
        
        # Build location information
        location_info = []
        for loc_id, loc_data in locations.items():
            exits = loc_data.get("exits", [])
            locked_exits = loc_data.get("locked_exits", {})
            is_current = "【當前位置】" if loc_id == current_location else ""
            
            # Convert exit IDs to readable names
            exit_names = []
            for exit_id in exits:
                exit_data = locations.get(exit_id, {})
                if exit_data:
                    exit_names.append(f"{exit_data['name']} ")
                else:
                    exit_names.append(exit_id)
            
            location_info.append(f"- {loc_data['name']} {is_current}")
            location_info.append(f"  可通往: {', '.join(exit_names) if exit_names else '無'}")
            
        
        location_text = "\n".join(location_info)
        
        # Create prompt for AI
        prompt = f"""你是一個文字冒險遊戲的地圖繪製師。請根據以下地點信息，繪製一個簡潔美觀的 ASCII 文字地圖。

場景名稱：{world['name']}
當前位置：{state.location}

地點清單：
{location_text}

繪製要求：
1. 使用簡單線條連接各地點
2. 地圖寬度50字符內
3. 只顯示地圖圖形
4. 清晰展示連接關係

請繪製："""

        try:
            model_name = os.getenv("OPENAI_MODEL_NAME")
            
            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "你是遊戲地圖繪製助手。使用文字符號繪製簡潔的地圖。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Check if response is valid
            if not response or not response.choices:
                return "⚠️ AI 返回了空回應，請稍後再試。"
            
            choice = response.choices[0]
            message_content = choice.message.content
            finish_reason = choice.finish_reason
            
            # Debug: Print response details
            print(f"📊 AI 回應詳情:")
            print(f"  - Finish Reason: {finish_reason}")
            print(f"  - Content Length: {len(message_content) if message_content else 0}")
            print(f"  - Content is None: {message_content is None}")
            
            # Check for content filtering
            if finish_reason == "content_filter":
                return "⚠️ 內容被安全過濾器攔截。"
            
            if not message_content:
                return f"⚠️ AI 未能生成地圖內容 (finish_reason: {finish_reason})。請稍後再試。"
            
            # Remove markdown code block markers if present
            map_text = message_content


            return {"text": f"\n{map_text}\n\n當前位置：【{state.location}】\n\n💡 此地圖由 AI 生成，位置可能不準確，只供參考。", "type": "ascii_map"}
            
        except Exception as e:
            error_msg = f"⚠️ 生成地圖時發生錯誤：{str(e)}\n\n"

            return error_msg
    
    def get_bilingual_name(self, cn_name: str, entity_type: str) -> str:
        """Get bilingual display name (Chinese + English)"""
        if entity_type == "enemy":
            # Find enemy by Chinese name
            for enemy_id, enemy_data in self.data.enemies.items():
                if enemy_data["name"] == cn_name:
                    return f"{cn_name}({enemy_data.get('en_id', enemy_id)})"
        elif entity_type == "item":
            # Find item by Chinese name (check both items and weapons)
            for item_name, item_data in self.data.items.items():
                if item_name == cn_name:
                    return f"{cn_name}({item_data.get('en_name', item_name)})"
            # Check weapons if not found in items
            for weapon_name, weapon_data in self.data.weapons.items():
                if weapon_name == cn_name:
                    return f"{cn_name}({weapon_data.get('en_name', weapon_name)})"
        elif entity_type == "location":
            # Find location by Chinese name - check all worlds
            for world in self.data.worlds:
                for loc_id, loc_data in world["locations"].items():
                    if loc_data["name"] == cn_name:
                        return f"{cn_name}({loc_data.get('en_name', loc_id)})"
        
        return cn_name  # Fallback to Chinese name only
    
    def get_current_world(self, state: GameState) -> dict:
        """Get the world data for the current scenario"""
        world = self.data.get_world_by_id(state.scenario)
        return world if world else self.data.world
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> GameState:
        """Get existing session or create new one"""
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        
        state = GameState()
        self.sessions[state.session_id] = state
        return state
    
    def start_game(self, state: GameState, scenario: str) -> List[str]:
        """Initialize a new game with selected scenario"""
        messages = []
        state.scenario = scenario
        
        # Load scenario-specific data
        self.data.load_scenario_data(scenario)
        
        # Get the world for this scenario
        world = self.data.get_world_by_id(scenario)
        if not world:
            return ["錯誤：找不到該場景"]
        
        # Set initial location based on scenario
        initial_location_id = list(world["locations"].keys())[0]  # First location in the world
        state.location_id = initial_location_id
        state.location = world["locations"][initial_location_id]["name"]
        
        # Add opening message
        messages.append(world["opening"])
        
        # Add initial location description
        initial_loc = world["locations"][initial_location_id]
        location_display = self.get_bilingual_name(initial_loc["name"], "location")
        messages.append(f"你身處「{location_display}」。")
        if initial_loc.get("ambient"):
            messages.append(initial_loc["ambient"][0])
        
        # 顯示可互動的對象（線索提示）
        clues = initial_loc.get("clues", {})
        if clues:
            interactive_objects = [f"{cn}({clue.get('en_name', cn)})" for cn, clue in clues.items()]
            messages.append(f"💡 你可以互動的事物：{', '.join(interactive_objects)}")
        
        # Update exits
        self._update_exits(state)
        
        # Initialize player inventory from world data
        initial_inventory = world.get("initial_inventory", [
            {"name": "火把", "qty": 1},
            {"name": "舊地圖", "qty": 1},
            {"name": "治療藥水", "qty": 1}
        ])
        
        state.player.inventory = [
            Item(
                name=item["name"],
                qty=item["qty"],
                display_name=self.get_bilingual_name(item["name"], "item")
            )
            for item in initial_inventory
        ]
        
        # Initialize quests
        for quest_data in world["quests"]:
            quest = Quest(**quest_data)
            state.quests[quest.id] = quest
        
        # Trigger initial quest
        self._trigger_quest_events(state, "onEnter", location=initial_location_id)
        
        return messages
    
    def clamp(self, value: int, min_val: int, max_val: int) -> int:
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))
    
    def rng(self, min_val: int, max_val: int) -> int:
        """Random number generator"""
        return random.randint(min_val, max_val)
    
    # Combat System
    def ensure_enemy(self, state: GameState) -> List[str]:
        """Spawn enemy if conditions are met (based on current location)"""
        messages = []
        if state.enemy or random.random() >= 0.30:
            return messages
        
        # Use current location's spawn data
        world = self.get_current_world(state)
        location = world["locations"].get(state.location_id, {})
        spawns = location.get("spawns", [])
        
        if not spawns:
            return messages
        

        # Pick random enemy from location's spawn list
        spawn = random.choice(spawns)
        enemy_id = spawn.split(':')[0]
        messages.extend(self.spawn_enemy(state, enemy_id))
        
        return messages
    
    def spawn_enemy(self, state: GameState, enemy_id: str) -> List[str]:
        """Spawn a new enemy"""
        messages = []
        enemy_data = self.data.enemies.get(enemy_id)
        if not enemy_data:
            return messages
        
        state.enemy = Enemy(
            id=enemy_id,
            name=enemy_data["name"],
            hp=enemy_data["maxhp"],
            maxhp=enemy_data["maxhp"],
            baseAtk=enemy_data.get("baseAtk", 10),
            buffs=Buff(),
            display_name=self.get_bilingual_name(enemy_data["name"], "enemy")
        )
        
        enemy_display = self.get_bilingual_name(enemy_data["name"], "enemy")
        messages.append("陰影中浮現了某種氣息……")
        
        # 返回帶有特殊類型標記的消息字典
        messages.append({"text": f"⚔️ 出現了【{enemy_display}】！", "type": "enemy_appear"})
        
        # 顯示敵人提示（如果有）
        if "hint" in enemy_data:
            messages.append(f"💡 {enemy_data['hint']}")
        
        return messages
    
    def player_attack(self, state: GameState, intent: Optional[object] = None) -> List[str]:
        """Execute player attack with advanced NLP features"""
        messages = []
        
        if not state.enemy:
            messages.append("周圍沒有敵人。")
            return messages
        
        # Check stun
        if state.player.buffs.stun > 0:
            state.player.buffs.stun -= 1
            if state.player.buffs.stun > 0:
                messages.append(f"你處於暈眩狀態，無法行動！（剩餘 {state.player.buffs.stun} 回合）")
            else:
                messages.append("你處於暈眩狀態，無法行動！（眩暈即將結束）")
            messages.extend(self.enemy_turn(state))
            return messages
        
        enemy = state.enemy
        
        # Check if attack hits
        base_evasion = enemy.buffs.evasion or 0
        
        # 功能3：攻擊方式影響命中率
        hit_modifier = 1.0
        if intent and hasattr(intent, 'attack_style'):
            if intent.attack_style == "quick":
                hit_modifier = 1.15  # 快速攻擊提高命中
            elif intent.attack_style == "heavy":
                hit_modifier = 0.85  # 重擊降低命中
            elif intent.attack_style == "precise":
                hit_modifier = 1.5  # 精準攻擊大幅提高命中
        
        hit = random.random() > (base_evasion * (2 - hit_modifier))
        if not hit:
            messages.append("你的攻擊被敵人閃過！")
            messages.extend(self.enemy_turn(state))
            return messages
        
        # Calculate base damage
        base_dmg = self.rng(10, 18)
        crit_mul = 1 + 0.25 * (state.player.buffs.critUp or 0)
        
        # 功能1：武器加成
        weapon_bonus = 0
        weapon_name = None
        is_throwable = False
        if intent and hasattr(intent, 'weapon') and intent.weapon:
            weapon_name = intent.weapon
            # Check if player has the weapon
            if not self.has_item(state, weapon_name):
                messages.append(f"你沒有 {weapon_name}。")
                messages.extend(self.enemy_turn(state))
                return messages
            
            weapon_data = self.data.weapons.get(weapon_name, {})
            weapon_bonus = weapon_data.get("damage_bonus", 0)
            is_throwable = weapon_data.get("type") == "throwable"
            
            if is_throwable:
                messages.append(f"你投擲【{weapon_name}】進行攻擊！")
            else:
                messages.append(f"你使用【{weapon_name}】進行攻擊！")
        
        # 功能3：攻擊方式影響傷害
        style_multiplier = 1.0
        style_desc = ""
        if intent and hasattr(intent, 'attack_style'):
            if intent.attack_style == "quick":
                style_multiplier = 0.8
                style_desc = "快速攻擊"
            elif intent.attack_style == "heavy":
                style_multiplier = 1.5
                style_desc = "全力重擊"
            elif intent.attack_style == "precise":
                style_multiplier = 1.2
                style_desc = "精準打擊"
            elif intent.attack_style == "defensive":
                style_multiplier = 0.9
                style_desc = "謹慎攻擊"
                state.player.buffs.evasion = 0.15  # 防守反擊增加閃避
        
        # 功能1：部位攻擊加成
        part_multiplier = 1.0
        special_effect = None
        if intent and hasattr(intent, 'body_part') and intent.body_part:
            enemy_data = self.data.enemies.get(enemy.id, {})
            body_parts = enemy_data.get("body_parts", {})
            if intent.body_part in body_parts:
                part_data = body_parts[intent.body_part]
                part_multiplier = part_data.get("damage_multiplier", 1.0)
                if random.random() < part_data.get("chance", 0):
                    special_effect = part_data.get("special")
                messages.append(f"你瞄準了【{intent.body_part}】！")
        
        # 功能3：動作修飾詞加成
        modifier_bonus = 0
        if intent and hasattr(intent, 'modifiers') and intent.modifiers:
            if "側面" in intent.modifiers or "繞到" in intent.modifiers:
                modifier_bonus += 3
                messages.append("你繞到了敵人側面！")
            if "跳躍" in intent.modifiers:
                modifier_bonus += 2
                messages.append("你跳躍攻擊！")
        
        # Calculate final damage
        base_final_dmg = (base_dmg + weapon_bonus + modifier_bonus) * crit_mul * style_multiplier * part_multiplier
        
        # Apply debuff effects
        if state.player.buffs.slow > 0:
            base_final_dmg *= 0.7  # Slow reduces damage by 30%
        
        total_dmg = round(base_final_dmg)
        
        # Apply confusion (miss chance)
        if state.player.buffs.confusion > 0:
            if random.random() < 0.3:  # 30% miss chance when confused
                messages.append(f"😵 你因混亂而攻擊失誤！")
                return messages
        
        enemy.hp = self.clamp(enemy.hp - total_dmg, 0, enemy.maxhp)
        
        # Consume throwable weapon
        if weapon_name and is_throwable:
            self.remove_item(state, weapon_name, 1)
            messages.append(f"({weapon_name} -1)")
        
        # Apply weapon debuff if active
        if state.player.weapon_debuff and state.player.weapon_debuff_duration > 0:
            for debuff_type, debuff_turns in state.player.weapon_debuff.items():
                if hasattr(enemy.buffs, debuff_type):
                    current_val = getattr(enemy.buffs, debuff_type, 0)
                    setattr(enemy.buffs, debuff_type, max(current_val, debuff_turns))
                    messages.append(f"💉 武器上的毒藥生效！敵人被施加了 {debuff_type} 效果！")
            
            state.player.weapon_debuff_duration -= 1
            if state.player.weapon_debuff_duration <= 0:
                state.player.weapon_debuff = None
        
        # Display attack result
        enemy_display = self.get_bilingual_name(enemy.name, "enemy")
        if style_desc:
            messages.append(f"你的【{style_desc}】對【{enemy_display}】造成了 {total_dmg} 傷害！")
        else:
            messages.append(f"你對【{enemy_display}】造成了 {total_dmg} 傷害。")
        
        # 功能1：特殊效果
        if special_effect:
            if special_effect == "blind":
                enemy.buffs.evasion = max(0, enemy.buffs.evasion - 0.3)
                messages.append("💥 敵人的眼睛被擊中，閃避降低！")
            elif special_effect == "stun":
                enemy.buffs.stun = 1
                messages.append("💥 暴擊！敵人被擊暈了！")
            elif special_effect == "slow":
                messages.append("💥 敵人的腿受傷，行動變慢！")
            elif special_effect == "instant_kill":
                enemy.hp = 0
                messages.append("💀 致命一擊！你擊碎了敵人的頭顱！")
            elif special_effect == "immobilize":
                enemy.buffs.stun = 2
                messages.append("🦿 敵人的腿被打斷，無法移動！")
            elif special_effect == "disarm":
                enemy.baseAtk = max(1, int(enemy.baseAtk * 0.5))
                messages.append("🗡️ 敵人的武器被擊落，攻擊力大幅降低！")
            elif special_effect == "venom_burst":
                state.player.buffs.poison = max(state.player.buffs.poison, 5)
                messages.append("☠️ 毒液爆發！你被濺到劇毒！")
            elif special_effect == "remove_poison":
                if state.player.buffs.poison > 0:
                    state.player.buffs.poison = 0
                    messages.append("✨ 你破壞了毒腺，毒素被清除！")
                else:
                    messages.append("✨ 你破壞了毒腺！")
            elif special_effect == "disperse":
                enemy.buffs.evasion = 0
                messages.append("👻 靈體被擊散，形體變得虛弱！")
            elif special_effect == "ground":
                enemy.buffs.evasion = max(0, enemy.buffs.evasion - 0.5)
                messages.append("🪽 翅膀受損，敵人無法飛行，閃避大幅降低！")
            elif special_effect == "crack":
                messages.append("🪨 石身出現裂痕，防禦力下降！")
            elif special_effect == "banish":
                enemy.hp = max(0, int(enemy.hp * 0.3))
                messages.append("✨ 核心被擊中，靈體即將消散！")
        
        # Check if enemy defeated
        if enemy.hp <= 0:
            messages.append(f"你擊敗了【{enemy_display}】！戰鬥結束。")
            messages.extend(self._handle_enemy_defeat(state, enemy.id))
            state.enemy = None
            return messages
        
        # 功能2：根據敵人狀態產生動態對話
        messages.extend(self._enemy_dynamic_dialogue(state, enemy))
        
        messages.extend(self.enemy_turn(state))
        return messages
    
    def _enemy_dynamic_dialogue(self, state: GameState, enemy: Enemy) -> List[str]:
        """功能2：生成動態敵人對話"""
        messages = []
        enemy_data = self.data.enemies.get(enemy.id, {})
        dialogues = enemy_data.get("dialogues", {})
        
        # 低生命值對話
        if enemy.hp < enemy.maxhp * 0.3 and dialogues.get("low_hp"):
            if random.random() < 0.5:
                messages.append(f"💬 {random.choice(dialogues['low_hp'])}")
        
        return messages
    
    def handle_intimidation(self, state: GameState, sentiment) -> List[str]:
        """功能2：處理威嚇/對話情感"""
        messages = []
        
        if not state.enemy:
            return messages
        
        enemy = state.enemy
        enemy_data = self.data.enemies.get(enemy.id, {})
        dialogues = enemy_data.get("dialogues", {})
        
        if sentiment == "intimidating":
            # 檢查是否生命值低於50%
            if enemy.hp < enemy.maxhp * 0.5:
                # 30%機率撤退
                if random.random() < 0.3:
                    enemy_display = self.get_bilingual_name(enemy.name, "enemy")
                    messages.append(f"✨ 在你的威嚇下，【{enemy_display}】畏懼地逃走了！")
                    messages.extend(self._handle_enemy_defeat(state, enemy.id, fled=True))
                    state.enemy = None
                    return messages
                else:
                    # 70%機率憤怒
                    enemy.buffs.enrage = True
                    enemy.buffs.critUp = (enemy.buffs.critUp or 0) + 3
                    if dialogues.get("enraged"):
                        messages.append(f"💢 {random.choice(dialogues['enraged'])}")
                    messages.append(f"敵人的攻擊力上升！")
            else:
                if dialogues.get("intimidated"):
                    messages.append(f"💬 {random.choice(dialogues['intimidated'])}")
        
        elif sentiment == "friendly":
            messages.append("你試圖友善地交流，但野獸不為所動...")
        
        return messages
    
    def _process_player_debuffs(self, state: GameState) -> List[str]:
        """Process player debuff effects (poison, bleed, slow, confusion)"""
        messages = []
        debuff_dmg = 0
        
        if state.player.buffs.poison > 0:
            dmg = 3
            debuff_dmg += dmg
            state.player.buffs.poison -= 1
            messages.append(f"🧪 中毒效果：你受到 {dmg} 傷害（剩餘 {state.player.buffs.poison} 回合）")
        
        if state.player.buffs.bleed > 0:
            dmg = 2
            debuff_dmg += dmg
            state.player.buffs.bleed -= 1
            messages.append(f"🩸 流血效果：你受到 {dmg} 傷害（剩餘 {state.player.buffs.bleed} 回合）")
        
        if state.player.buffs.slow > 0:
            state.player.buffs.slow -= 1
            messages.append(f"🐌 減速效果：攻擊力降低（剩餘 {state.player.buffs.slow} 回合）")
        
        if state.player.buffs.confusion > 0:
            state.player.buffs.confusion -= 1
            messages.append(f"😵 混亂效果：命中率降低（剩餘 {state.player.buffs.confusion} 回合）")
        
        if debuff_dmg > 0:
            state.player.hp = self.clamp(state.player.hp - debuff_dmg, 0, state.player.maxhp)
        
        return messages
    
    def player_defend(self, state: GameState) -> List[str]:
        """Player enters defensive stance"""
        messages = []
        
        # Check stun
        if state.player.buffs.stun > 0:
            state.player.buffs.stun -= 1
            if state.player.buffs.stun > 0:
                messages.append(f"你處於暈眩狀態，無法行動！（剩餘 {state.player.buffs.stun} 回合）")
            else:
                messages.append("你處於暈眩狀態，無法行動！（眩暈即將結束）")
            messages.extend(self.enemy_turn(state))
            return messages
        
        state.player.defending = True
        messages.append("你擺出防禦姿態，將減少下一次受到的傷害。")
        messages.extend(self.enemy_turn(state))
        return messages
    
    def enemy_turn(self, state: GameState) -> List[str]:
        """Execute enemy turn"""
        messages = []
        
        if not state.enemy:
            return messages
        
        enemy = state.enemy
        
        # Check stun
        enemy_display = self.get_bilingual_name(enemy.name, "enemy")
        if enemy.buffs.stun > 0:
            messages.append(f"【{enemy_display}】（暈眩中，無法行動）")
            enemy.buffs.stun -= 1
            return messages
        
        # AI picks action
        action = self._enemy_ai(state, enemy)
        
        if action["type"] == "buff":
            if "apply" in action:
                for key, value in action["apply"].items():
                    setattr(enemy.buffs, key, value)
            messages.append(f"【{enemy_display}】使用了【{action['name']}】，獲得增益。")
        
        elif action["type"] == "stun":
            state.player.buffs.stun = (state.player.buffs.stun or 0) + action["stun"]
            messages.append(f"【{enemy_display}】使用了【{action['name']}】，你被暈眩 {action['stun']} 回合！")
        
        elif action["type"] == "attack":
            dmg = self.rng(action["dmg"][0], action["dmg"][1])
            e_crit_mul = 1 + 0.25 * (enemy.buffs.critUp or 0)
            dmg = round(dmg * e_crit_mul)
            dmg += enemy.buffs.atkUp or 0
            
            if state.player.defending:
                dmg = round(dmg * 0.5)
            
            state.player.hp = self.clamp(state.player.hp - dmg, 0, state.player.maxhp)
            messages.append(f"【{enemy_display}】使出【{action['name']}】，對你造成 {dmg} 傷害！")
            
            if action.get("lifesteal"):
                heal = round(dmg * action["lifesteal"])
                enemy.hp = self.clamp(enemy.hp + heal, 0, enemy.maxhp)
                messages.append(f"它吸收了 {heal} 生命！")
            
            # Apply debuffs
            if action.get("debuff"):
                for debuff_type, duration in action["debuff"].items():
                    setattr(state.player.buffs, debuff_type, duration)
                    debuff_names = {
                        "poison": "中毒",
                        "slow": "減速",
                        "bleed": "流血",
                        "confusion": "混亂"
                    }
                    debuff_name = debuff_names.get(debuff_type, debuff_type)
                    messages.append(f"你被施加了【{debuff_name}】狀態（{duration} 回合）！")
        
        # Update cooldowns
        for skill in enemy.cd:
            enemy.cd[skill] = max(0, enemy.cd[skill] - 1)
        
        if action.get("cd"):
            enemy.cd[action["key"]] = action["cd"]
        
        state.player.defending = False
        
        # Note: stun countdown is handled in player action checks, not here
        # to avoid double decrement
        
        # Process player debuff effects
        messages.extend(self._process_player_debuffs(state))
        
        if state.player.hp <= 0:
            state.game_over = True
            messages.append("💀 你倒下了……冒險到此為止。")
            messages.append("\n=== 遊戲結束 ===")
            messages.append("你可以重新開始遊戲或選擇其他場景。")
        
        return messages
    
    def _enemy_ai(self, state: GameState, enemy: Enemy) -> dict:
        """Generic enemy AI decision making based on skills and HP threshold"""
        enemy_data = self.data.enemies.get(enemy.id, {})
        skills = enemy_data.get("skills", {})
        
        if not skills:
            # Fallback if no skills defined
            return {"type": "attack", "key": "basic", "name": "攻擊", "dmg": [6, 10]}
        
        # === Phase 1: Low HP behaviors (< 30%) ===
        if enemy.hp <= enemy.maxhp * 0.3:
            # Check for enrage-type buffs (only trigger once)
            if not enemy.buffs.enrage:
                for skill_key, skill_data in skills.items():
                    if skill_data.get("buff") and "critUp" in skill_data["buff"]:
                        enemy.buffs.enrage = True
                        enemy.buffs.critUp = (enemy.buffs.critUp or 0) + skill_data["buff"]["critUp"]
                        return {
                            "type": "buff",
                            "key": skill_key,
                            "name": skill_data["name"],
                            "apply": skill_data["buff"],
                            "cd": skill_data.get("cd", 0)
                        }
        
        # === Phase 2: Priority skills (off cooldown) ===
        # Sort skills by priority: stun > buff > high damage > lifesteal > basic
        skill_priority = []
        
        for skill_key, skill_data in skills.items():
            if enemy.cd.get(skill_key, 0) > 0:
                continue  # Skill on cooldown
            
            priority = 0
            skill_type = "attack"
            
            # Determine skill type and priority
            if "stun" in skill_data:
                skill_type = "stun"
                priority = 100  # Highest priority
            elif "buff" in skill_data:
                skill_type = "buff"
                # Check if buff is already active
                buff_keys = skill_data["buff"].keys()
                already_active = all(getattr(enemy.buffs, key, None) for key in buff_keys)
                if not already_active:
                    priority = 80
                else:
                    continue  # Skip if buff already active
            elif "dmg" in skill_data:
                skill_type = "attack"
                avg_dmg = sum(skill_data["dmg"]) / 2
                priority = avg_dmg
                # Bonus priority for special effects
                if "lifesteal" in skill_data:
                    priority += 20
                if "debuff" in skill_data:
                    priority += 15
            
            skill_priority.append({
                "key": skill_key,
                "type": skill_type,
                "priority": priority,
                "data": skill_data
            })
        
        # === Phase 3: Execute highest priority skill ===
        if skill_priority:
            # Sort by priority (descending)
            skill_priority.sort(key=lambda x: x["priority"], reverse=True)
            chosen = skill_priority[0]
            
            skill_key = chosen["key"]
            skill_data = chosen["data"]
            skill_type = chosen["type"]
            
            if skill_type == "stun":
                return {
                    "type": "stun",
                    "key": skill_key,
                    "name": skill_data["name"],
                    "stun": skill_data.get("stun", 1),
                    "cd": skill_data.get("cd", 0)
                }
            elif skill_type == "buff":
                return {
                    "type": "buff",
                    "key": skill_key,
                    "name": skill_data["name"],
                    "apply": skill_data["buff"],
                    "cd": skill_data.get("cd", 0)
                }
            else:  # attack
                action = {
                    "type": "attack",
                    "key": skill_key,
                    "name": skill_data["name"],
                    "dmg": skill_data["dmg"],
                    "cd": skill_data.get("cd", 0)
                }
                # Add optional effects
                if "lifesteal" in skill_data:
                    action["lifesteal"] = skill_data["lifesteal"]
                if "debuff" in skill_data:
                    action["debuff"] = skill_data["debuff"]
                return action
        
        # === Phase 4: Fallback to first available skill ===
        first_skill = next(iter(skills.items()))
        skill_key, skill_data = first_skill
        return {
            "type": "attack",
            "key": skill_key,
            "name": skill_data["name"],
            "dmg": skill_data.get("dmg", [6, 10])
        }
    
    def _handle_enemy_defeat(self, state: GameState, enemy_id: str, fled: bool = False) -> List[str]:
        """Handle enemy defeat rewards and quest updates"""
        messages = []
        
        # 如果是逃跑則不給獎勵
        if not fled:
            # Drop items based on enemy data
            enemy_data = self.data.enemies.get(enemy_id, {})
            drops = enemy_data.get("drops", [])
            for drop in drops:
                chance = drop.get("chance", 1.0)
                if random.random() <= chance:
                    messages.extend(self.add_item(state, drop["item"], drop.get("qty", 1)))
        
        # Update stats
        if "defeated" not in state.stats:
            state.stats["defeated"] = {}
        state.stats["defeated"][enemy_id] = state.stats["defeated"].get(enemy_id, 0) + 1
        
        # Trigger quest events
        self._trigger_quest_events(state, "onDefeat", enemy=enemy_id)
        
        return messages
    
    # ========== 功能4：環境互動問答系統 ==========
    def handle_environment_question(self, state: GameState, intent: object) -> List[str]:
        """處理環境相關問題"""
        messages = []
        
        location_id = state.location_id
        target = intent.object if hasattr(intent, 'object') and intent.object else "四周"
        question_type = intent.question_type if hasattr(intent, 'question_type') else "general"
        
        # 從當前 world 的 location 中獲取線索數據
        world = self.get_current_world(state)
        location_data = world["locations"].get(location_id, {})
        location_clues = location_data.get("clues", {})
        
        # 獲取目標的線索，如果沒有則使用默認回覆
        target_clues = location_clues.get(target, {})
        
        # 先觸發任務事件（觀察線索），在給物品之前
        # 這樣可以確保順序任務正確更新
        self._trigger_quest_events(state, "onObserve", target=target)
        
        # 如果找到線索
        if target_clues:
            # 給予道具（如果有）
            if "give_item" in target_clues:
                items_to_give = target_clues["give_item"]
                if isinstance(items_to_give, str):
                    items_to_give = [items_to_give]
                
                for item_name in items_to_give:
                    messages.extend(self.add_item(state, item_name, 1))
                
                # 移除 give_item 防止重複獲取
                del location_clues[target]["give_item"]
            
            # QUESTION 只顯示答案（origin/reason/method），不顯示描述
            # 根據問題類型顯示對應答案
            if question_type in target_clues and question_type not in ["search", "give_item", "en_name"]:
                messages.append(f"💡 {target_clues[question_type]}")
            elif "origin" in target_clues:
                messages.append(f"💡 來源：{target_clues['origin']}")
            elif "reason" in target_clues:
                messages.append(f"💡 原因：{target_clues['reason']}")
            elif "method" in target_clues:
                messages.append(f"💡 方法：{target_clues['method']}")
            else:
                # 如果沒有答案字段，回退顯示描述
                if "search" in target_clues:
                    messages.append(f"🔍 {target_clues['search']}")
        else:
            messages.append(f"🔍 這裡沒有{target}可以調查。")
        
        # 記錄發現的線索到環境狀態
        if location_id not in state.environment_state:
            state.environment_state[location_id] = {}
        state.environment_state[location_id][target] = state.environment_state[location_id].get(target, 0) + 1
        
        return messages
    
    # Inventory System
    def add_item(self, state: GameState, name: str, qty: int = 1) -> List[str]:
        """Add item to inventory"""
        messages = []
        item_data = self.data.items.get(name, {})
        
        existing = next((item for item in state.player.inventory if item.name == name), None)
        
        if existing and item_data.get("stack", True):
            existing.qty += qty
        else:
            display_name = self.get_bilingual_name(name, "item")
            state.player.inventory.append(Item(name=name, qty=qty, display_name=display_name))
        
        item_display = self.get_bilingual_name(name, "item")
        messages.append(f"獲得物品：{item_display} × {qty}")
        
        # Trigger quest event
        self._trigger_quest_events(state, "onPick", item=name, qty=qty)
        
        return messages
    
    def pick_from_location(self, state: GameState, item_name: Optional[str] = None) -> List[str]:
        """Pick up items from current location"""
        messages = []
        
        # Get current location data
        world = self.get_current_world(state)
        location = world["locations"].get(state.location_id, {})
        pickable_items = location.get("pickable_items", [])
        
        # Initialize picked_items in location state if not exists
        if "picked_items" not in state.location_states.get(state.location_id, {}):
            if state.location_id not in state.location_states:
                state.location_states[state.location_id] = {}
            state.location_states[state.location_id]["picked_items"] = []
        
        picked_items = state.location_states[state.location_id]["picked_items"]
        
        # If no item specified, show available items
        if not item_name or item_name == "未知物品":
            available = [item for item in pickable_items if item["name"] not in picked_items]
            if not available:
                messages.append("這裡沒有可以拾取的物品。")
            else:
                # Get bilingual names for all available items
                bilingual_names = []
                for item in available:
                    cn_name = item["name"]
                    # Get English name from items or weapons
                    en_name = None
                    if cn_name in self.data.items:
                        en_name = self.data.items[cn_name].get("en_name")
                    elif cn_name in self.data.weapons:
                        en_name = self.data.weapons[cn_name].get("en_name")
                    
                    if en_name:
                        bilingual_names.append(f"{cn_name}({en_name})")
                    else:
                        bilingual_names.append(cn_name)
                
                items_list = "、".join(bilingual_names)
                messages.append(f"你可以拾取：{items_list}")
            return messages
        
        # Try to find the item in pickable_items
        target_item = None
        for item in pickable_items:
            if item["name"] == item_name:
                target_item = item
                break
        
        if not target_item:
            item_display = self.get_bilingual_name(item_name, "item")
            messages.append(f"這裡沒有 {item_display}。")
            return messages
        
        # Check if already picked
        if item_name in picked_items:
            item_display = self.get_bilingual_name(item_name, "item")
            messages.append(f"{item_display} 已經被拾取了。")
            return messages
        
        # Pick up the item
        qty = target_item.get("qty", 1)
        messages.extend(self.add_item(state, item_name, qty))
        
        # Mark as picked if not respawnable
        if not target_item.get("respawn", False):
            picked_items.append(item_name)
        
        return messages
    
    def remove_item(self, state: GameState, name: str, qty: int = 1) -> bool:
        """Remove item from inventory"""
        item = next((i for i in state.player.inventory if i.name == name), None)
        if not item:
            return False
        
        item_data = self.data.items.get(name, {})
        if item_data.get("stack", True):
            item.qty -= qty
            if item.qty <= 0:
                state.player.inventory.remove(item)
        else:
            state.player.inventory.remove(item)
        
        return True
    
    def has_item(self, state: GameState, name: str) -> bool:
        """Check if player has item"""
        return any(item.name == name and item.qty > 0 for item in state.player.inventory)
    
    def use_item(self, state: GameState, name: str, context: Optional[str] = None) -> List[str]:
        """Use an item"""
        messages = []
        item_display = self.get_bilingual_name(name, "item")
        
        if not self.has_item(state, name):
            messages.append(f"你沒有 {item_display}。")
            return messages
        
        item_data = self.data.items.get(name, {})
        use_config = item_data.get("use")
        
        # Check if item has use effect
        if not use_config:
            messages.append(f"{item_display} 暫無特殊用法。")
            return messages
        
        # Check stun - cannot use any items while stunned
        if state.player.buffs.stun > 0:
            state.player.buffs.stun -= 1
            if state.player.buffs.stun > 0:
                messages.append(f"你處於暈眩狀態，無法使用物品！（剩餘 {state.player.buffs.stun} 回合）")
            else:
                messages.append("你處於暈眩狀態，無法使用物品！（眩暈即將結束）")
            if state.enemy:
                messages.extend(self.enemy_turn(state))
            return messages
        
        effect_type = use_config.get("type")
        
        # Auto-detect context from current location if not provided
        if context is None:
            world = self.get_current_world(state)
            location = world["locations"].get(state.location_id, {})
            context = location.get("context")
        
        # Apply item effect based on type
        consumed = False
        
        # Check combat_only restriction
        if use_config.get("combat_only", False) and not state.enemy:
            messages.append(f"{item_display} 只能在戰鬥中使用。")
            return messages
        
        if effect_type == "heal":
            before = state.player.hp
            heal_amount = use_config.get("value", 0)
            state.player.hp = self.clamp(state.player.hp + heal_amount, 0, state.player.maxhp)
            actual_heal = state.player.hp - before
            messages.append(f"你使用了{item_display}（+{actual_heal} HP）。")
            consumed = use_config.get("consume", False)
        
        elif effect_type == "buff":
            buff_name = use_config.get("buff")
            buff_value = use_config.get("value", 0)
            duration = use_config.get("duration", 1)
            if hasattr(state.player.buffs, buff_name):
                setattr(state.player.buffs, buff_name, buff_value)
            effect_message = use_config.get("message", f"你使用了{item_display}，獲得增益！")
            messages.append(effect_message)
            consumed = use_config.get("consume", False)
        
        elif effect_type == "combat":
            # Combat items (explosives, etc.)
            if not state.enemy:
                messages.append(f"{item_display} 需要在戰鬥中使用。")
                return messages
            
            effect_message = use_config.get("message", f"你使用了{item_display}！")
            messages.append(effect_message)
            
            # Deal damage
            if "damage" in use_config:
                dmg_range = use_config["damage"]
                damage = random.randint(dmg_range[0], dmg_range[1])
                state.enemy.hp -= damage
                messages.append(f"造成 {damage} 點傷害！")
                
                if state.enemy.hp <= 0:
                    messages.extend(self._handle_enemy_death(state))
            
            # Apply special effects (e.g., capture wraith)
            if "special" in use_config:
                special = use_config["special"]
                if special == "capture_wraith" and state.enemy and "wraith" in state.enemy.name.lower():
                    state.enemy.hp = 0
                    messages.append(f"{state.enemy.name} 被封印進容器中！")
                    messages.extend(self._handle_enemy_death(state))
            
            consumed = use_config.get("consume", False)
        
        elif effect_type == "weapon_buff":
            # Apply debuff to weapon (will be applied on next attack)
            effect_message = use_config.get("message", f"你使用了{item_display}。")
            messages.append(effect_message)
            
            # Store weapon buff in player state
            if "debuff" in use_config:
                state.player.weapon_debuff = use_config["debuff"]
                state.player.weapon_debuff_duration = use_config.get("duration", 1)
            
            consumed = use_config.get("consume", False)
        
        elif effect_type == "cleanse":
            # Remove debuffs
            cleanse_list = use_config.get("cleanse", [])
            effect_message = use_config.get("message", f"你使用了{item_display}。")
            messages.append(effect_message)
            
            for debuff_type in cleanse_list:
                if hasattr(state.player.buffs, debuff_type):
                    setattr(state.player.buffs, debuff_type, 0)
                    messages.append(f"{debuff_type} 效果已清除。")
            
            consumed = use_config.get("consume", False)
        
        elif effect_type == "craft":
            # Crafting system
            recipe = use_config.get("recipe", {})
            requires = recipe.get("requires", [])
            creates = recipe.get("creates")
            craft_message = recipe.get("message", "合成成功！")
            
            # Check if player has all required items
            can_craft = True
            for req in requires:
                req_item = req["item"]
                req_qty = req["qty"]
                if not self.has_item(state, req_item, req_qty):
                    messages.append(f"需要 {req_qty} 個 {req_item}。")
                    can_craft = False
            
            if can_craft:
                # Remove required items
                for req in requires:
                    self.remove_item(state, req["item"], req["qty"])
                
                # Give created item
                messages.append(craft_message)
                messages.extend(self.add_item(state, creates, 1))
                consumed = False
            
            return messages
        
        elif effect_type == "call_ai":
            # AI-powered features with parameter-based dispatch
            parameter = use_config.get("parameter")
            effect_message = use_config.get("message", f"你使用了{item_display}。")
            messages.append(effect_message)
            
            # Dispatch based on parameter
            if parameter == "generate_map":
                # Add a generating notice
                messages.append("🔄 AI 正在繪製地圖...")
                map_text = self.generate_text_map(state)
                messages.append(map_text)
            else:
                messages.append(f"⚠️ 未知的 AI 功能：{parameter}")
            
            consumed = use_config.get("consume", False)
        
        elif effect_type == "context":
            # Context-based usage (e.g., torch in well, key for doors)
            contexts = use_config.get("contexts", {})
            context_key = context if context and context in contexts else "default"
            context_effect = contexts.get(context_key, contexts.get("default", {}))
            
            if context_effect:
                # Check if required items are present (for crafting in specific context)
                requires = context_effect.get("requires", [])
                if requires:
                    can_use = True
                    for req in requires:
                        req_item = req["item"]
                        req_qty = req["qty"]
                        # Check if player has enough of the required item
                        player_item = next((i for i in state.player.inventory if i.name == req_item), None)
                        if not player_item or player_item.qty < req_qty:
                            item_display_req = self.get_bilingual_name(req_item, "item")
                            messages.append(f"需要 {req_qty} 個{item_display_req}才能使用。")
                            can_use = False
                            break
                    
                    if not can_use:
                        return messages
                    
                    # Remove required items if specified
                    remove_items = context_effect.get("remove_items", [])
                    for req in remove_items:
                        self.remove_item(state, req["item"], req["qty"])
                
                # Display message
                effect_message = context_effect.get("message", f"你使用了{item_display}。")
                messages.append(effect_message)
                
                # Display craft message if present (for crafting recipes)
                if "craft_message" in context_effect:
                    messages.append(context_effect["craft_message"])
                
                # Give item if specified
                if "give_item" in context_effect:
                    messages.extend(self.add_item(state, context_effect["give_item"], 1))
                    # Only remove give_item if it's marked as one-time use
                    if context_effect.get("one_time_give", True):
                        # Remove give_item from context to prevent duplicate acquisition
                        del contexts[context_key]["give_item"]
                
                # Unlock location if specified (e.g., key opens door)
                if "unlock_location" in context_effect:
                    unlock_loc = context_effect["unlock_location"]
                    world = self.get_current_world(state)
                    current_location = world["locations"].get(state.location_id, {})
                    
                    # Remove locked_exits entry
                    if "locked_exits" in current_location:
                        if unlock_loc in current_location["locked_exits"]:
                            del current_location["locked_exits"][unlock_loc]
                    
                    # Add to available exits
                    if "exits" in current_location and unlock_loc not in current_location["exits"]:
                        current_location["exits"].append(unlock_loc)
                    
                    # Auto-move player through the opened door
                    unlocked_loc_data = world["locations"].get(unlock_loc, {})
                    if unlocked_loc_data:
                        state.location_id = unlock_loc
                        state.location = unlocked_loc_data["name"]
                        if unlock_loc not in state.visited:
                            state.visited.append(unlock_loc)
                        
                        # Add movement message
                        location_display = self.get_bilingual_name(state.location, "location")
                        messages.append(f"你穿過開啟的大門，來到「{location_display}」。")
                        
                        # Show ambient description
                        if "ambient" in unlocked_loc_data and unlocked_loc_data["ambient"]:
                            messages.append(unlocked_loc_data["ambient"][0])
                        
                        # Store location for delayed onEnter trigger (after onUse completes quest)
                        context_effect["_trigger_enter_after_use"] = unlock_loc
                
                consumed = context_effect.get("consume", False)
            else:
                messages.append(f"{item_display} 在這裡似乎沒有作用。")
        
        else:
            messages.append(f"{item_display} 產生了未知效果。")
            consumed = use_config.get("consume", False)
        
        # Remove item if consumable
        if consumed:
            self.remove_item(state, name, 1)
        
        # Trigger enemy encounter if configured
        if use_config.get("trigger_enemy", False):
            messages.extend(self.ensure_enemy(state))
        
        # Trigger quest event (onUse)
        self._trigger_quest_events(state, "onUse", item=name, context=context)
        
        # Trigger delayed onEnter event if auto-moved after using item
        if use_config.get("type") == "context":
            contexts = use_config.get("contexts", {})
            context_key = context if context and context in contexts else "default"
            context_effect = contexts.get(context_key, contexts.get("default", {}))
            if context_effect and "_trigger_enter_after_use" in context_effect:
                enter_location = context_effect["_trigger_enter_after_use"]
                self._trigger_quest_events(state, "onEnter", location=enter_location)
                # Clean up the flag
                del context_effect["_trigger_enter_after_use"]
        
        # Process player debuffs even out of combat
        if not state.enemy:
            messages.extend(self._process_player_debuffs(state))
        
        return messages
    
    # Movement and Observation
    def move_to(self, state: GameState, location_name: str) -> List[str]:
        """Move to a new location"""
        messages = []
        
        # Check if there's an enemy blocking the way
        if state.enemy:
            enemy_display = self.get_bilingual_name(state.enemy.name, "enemy")
            messages.append(f"【{enemy_display}】擋住去路！你無法離開。")
            messages.append("（提示：使用「逃跑」命令隨機逃離）")
            messages.extend(self.enemy_turn(state))
            return messages
        
        world = self.get_current_world(state)
        
        # Find location ID from name or en_name
        location_id = None
        for loc_id, loc_data in world["locations"].items():
            if (loc_data["name"] == location_name or 
                loc_id == location_name or
                loc_data.get("en_name", "").lower() == location_name.lower()):
                location_id = loc_id
                break
        
        if not location_id:
            messages.append("那裡似乎不存在。")
            return messages
        
        # Check if can move there
        current_loc = world["locations"].get(state.location_id, {})
        if location_id not in current_loc.get("exits", []):
            messages.append("無法從此處前往那裡。")
            return messages
        
        # Move
        state.location_id = location_id
        loc_data = world["locations"][location_id]
        state.location = loc_data["name"]
        
        if location_id not in state.visited:
            state.visited.append(location_id)
        
        location_display = self.get_bilingual_name(state.location, "location")
        messages.append(f"你來到「{location_display}」。")
        
        # Update exits
        self._update_exits(state)
        
        # Add location ambient description
        if loc_data.get("ambient"):
            messages.append(loc_data["ambient"][0])
        
        # 顯示可互動的對象（線索提示）
        clues = loc_data.get("clues", {})
        if clues:
            interactive_objects = [f"{cn}({clue.get('en_name', cn)})" for cn, clue in clues.items()]
            messages.append(f"💡 你可以互動的事物：{', '.join(interactive_objects)}")
        
        # Trigger quest event
        self._trigger_quest_events(state, "onEnter", location=location_id)
        
        # Maybe spawn enemy
        messages.extend(self._maybe_spawn_at_location(state, location_id))
        
        # Process player debuffs even out of combat
        messages.extend(self._process_player_debuffs(state))
        
        return messages
    
    def _update_exits(self, state: GameState):
        """Update exits information in GameState"""
        world = self.get_current_world(state)
        current_loc = world["locations"].get(state.location_id, {})
        exit_ids = current_loc.get("exits", [])
        
        state.exits = []
        for exit_id in exit_ids:
            exit_loc = world["locations"].get(exit_id, {})
            if exit_loc:
                state.exits.append({
                    "cn_name": exit_loc["name"],
                    "en_name": exit_loc.get("en_name", exit_id)
                })
    
    def _maybe_spawn_at_location(self, state: GameState, location_id: str) -> List[str]:
        """Maybe spawn enemy at location"""
        messages = []
        world = self.get_current_world(state)
        location = world["locations"].get(location_id, {})
        spawns = location.get("spawns", [])
        
        if not spawns:
            state.enemy = None
            return messages
        
        r = random.random()
        acc = 0.0
        
        for spawn in spawns:
            parts = spawn.split(':')
            enemy_id = parts[0]
            probability = float(parts[1]) if len(parts) > 1 else 0.3
            acc += probability
            
            if r <= acc: 
                messages.extend(self.spawn_enemy(state, enemy_id))
                break
        
        return messages
    
    def observe(self, state: GameState, obj: str) -> List[str]:
        """Observe an object or surroundings"""
        messages = []
        
        # ✅ 調試：打印當前線索狀態
        world = self.get_current_world(state)
        location = world["locations"].get(state.location_id, {})
        clues = location.get("clues", {})
        
        print(f"\n🔍 [DEBUG] observe(obj='{obj}')")
        print(f"   當前位置: {state.location_id}")
        print(f"   可用線索: {list(clues.keys())}")
        print(f"   obj 是否在線索中: {obj in clues}")
        
        # ========== 1. 檢查是否觀察線索對象（最高優先級）==========
        if obj in clues:
            clue_data = clues[obj]
            
            print(f"   ✅ 匹配到線索: {obj}")
            
            # OBSERVE 只顯示描述
            if "search" in clue_data:
                messages.append(f"🔍 {clue_data['search']}")
            else:
                messages.append(f"🔍 你仔細觀察{obj}，但沒有特別發現。")
            
            # Trigger quest event BEFORE giving items so sequential objectives
            # (e.g. OBSERVE then COLLECT_ITEM) are marked in the correct order
            self._trigger_quest_events(state, "onObserve", target=obj)
            
            # Give items if specified
            if "give_item" in clue_data:
                items_to_give = clue_data["give_item"]
                if isinstance(items_to_give, str):
                    items_to_give = [items_to_give]
                
                for item_name in items_to_give:
                    messages.extend(self.add_item(state, item_name, 1))
                
                # Remove give_item after use to prevent duplicates
                del clues[obj]["give_item"]
            
            return messages
        
        # 2. 檢查是否觀察敵人
        if state.enemy and obj in [state.enemy.name, "敵", "enemy"]:
            e = state.enemy
            buff_status = "有增益" if any([e.buffs.critUp, e.buffs.evasion, e.buffs.enrage]) else "無"
            enemy_display = self.get_bilingual_name(e.name, "enemy")
            messages.append(f"你觀察【{enemy_display}】：生命 {e.hp}/{e.maxhp}，狀態 {buff_status}。")
            
            # Display weak points
            enemy_data = self.data.enemies.get(e.id, {})
            body_parts = enemy_data.get("body_parts", {})
            if body_parts:
                weak_points = ", ".join(body_parts.keys())
                messages.append(f"🎯 潛在弱點：{weak_points}")
            
            return messages  # ✅ 立即返回
        
        # # 3. 檢查是否觀察物品
        # if obj in self.data.items:
        #     item_display = self.get_bilingual_name(obj, "item")
        #     messages.append(f"你打量 {item_display}：{self.data.items[obj].get('desc', '平平無奇。')}")
        #     return messages  # ✅ 立即返回
        # print(self.data.items)

        # ========== 3. 檢查玩家背包中的物品（修復）==========
        # ✅ 檢查玩家是否擁有該物品
        player_item = next((item for item in state.player.inventory if item.name == obj), None)
        
        if player_item:
            # 從遊戲數據中獲取物品詳細信息
            item_data = self.data.items.get(obj, {})
            if not item_data:
                # 如果在 items 中找不到，檢查 weapons
                item_data = self.data.weapons.get(obj, {})
            
            item_display = self.get_bilingual_name(obj, "item")
            desc = item_data.get("desc", "平平無奇。")
            messages.append(f"你打量背包中的 {item_display}：{desc}")
            return messages
        
        # ========== 4. 檢查當前位置的可拾取物品 ==========
        pickable_items = location.get("pickable_items", [])
        picked_items = state.location_states.get(state.location_id, {}).get("picked_items", [])
        
        # 查找未被拾取的物品
        for item_data in pickable_items:
            if item_data["name"] == obj and obj not in picked_items:
                item_display = self.get_bilingual_name(obj, "item")
                desc = self.data.items.get(obj, {}).get("desc", "看起來可以拾取。")
                messages.append(f"你觀察地上的 {item_display}：{desc}")
                messages.append(f"💡 使用「pick {obj}」命令來拿取它。")
                return messages
        

        # ========== 處理「四周」觀察 ==========
        if obj in ["四周", "周圍", "around"]:
            location_display = self.get_bilingual_name(state.location, "location")
            
            # Get ambient description from current location
            ambient = location.get("ambient", [])
            
            if ambient:
                messages.append(ambient[0])
            else:
                messages.append(f"你環顧四周：{location_display} 一片寂靜。")
            
            # 顯示可互動的對象（線索提示）
            if clues:
                interactive_objects = [f"{cn}({clue.get('en_name', cn)})" for cn, clue in clues.items()]
                messages.append(f"💡 你可以互動的事物：{', '.join(interactive_objects)}")
            
            # 在環境描述之後才檢查並生成敵人
            messages.extend(self.ensure_enemy(state))
            
            if state.enemy:
                enemy_display = self.get_bilingual_name(state.enemy.name, "enemy")
                messages.append(f"【{enemy_display}】正虎視眈眈。")
            
            return messages  # ✅ 返回
        
        # ========== 未找到目標 ==========
        messages.append("你東張西望，但沒有新發現。")
        messages.extend(self.ensure_enemy(state))
        
        # Process player debuffs even out of combat
        if not state.enemy:
            messages.extend(self._process_player_debuffs(state))
        
        return messages
    
    def escape(self, state: GameState) -> List[str]:
        """Escape from combat to a random exit"""
        messages = []
        
        if not state.enemy:
            messages.append("這裡沒有敵人，不需要逃跑。")
            return messages
        
        # Check stun
        if state.player.buffs.stun > 0:
            state.player.buffs.stun -= 1
            if state.player.buffs.stun > 0:
                messages.append(f"你處於暈眩狀態，無法逃跑！（剩餘 {state.player.buffs.stun} 回合）")
            else:
                messages.append("你處於暈眩狀態，無法逃跑！（眩暈即將結束）")
            messages.extend(self.enemy_turn(state))
            return messages
        
        # Check if enemy is a boss
        enemy_data = self.data.enemies.get(state.enemy.id, {})
        if enemy_data.get("is_boss", False):
            enemy_display = self.get_bilingual_name(state.enemy.name, "enemy")
            messages.append(f"【{enemy_display}】是強大的BOSS，你無法逃跑！")
            messages.extend(self.enemy_turn(state))
            return messages
        
        # Get current location exits
        world = self.get_current_world(state)
        current_loc = world["locations"].get(state.location_id, {})
        exits = current_loc.get("exits", [])
        
        if not exits:
            messages.append("這裡沒有出口，無法逃跑！")
            messages.extend(self.enemy_turn(state))
            return messages
        
        # Enemy gets one last attack
        enemy_display = self.get_bilingual_name(state.enemy.name, "enemy")
        messages.append(f"你轉身逃跑，【{enemy_display}】趨機發動攻擊！")
        messages.extend(self.enemy_turn(state))
        
        # Check if player survived
        if state.player.hp <= 0:
            return messages
        
        # Randomly pick an exit
        escape_location_id = random.choice(exits)
        loc_data = world["locations"][escape_location_id]
        
        # Move to escape location
        state.location_id = escape_location_id
        state.location = loc_data["name"]
        state.enemy = None  # Clear enemy after escape
        
        if escape_location_id not in state.visited:
            state.visited.append(escape_location_id)
        
        location_display = self.get_bilingual_name(state.location, "location")
        messages.append(f"你逃到了「{location_display}」！")
        
        # Add ambient description
        if loc_data.get("ambient"):
            messages.append(loc_data["ambient"][0])

        # Update exits
        self._update_exits(state)

        # Trigger quest event
        self._trigger_quest_events(state, "onEnter", location=escape_location_id)
        
        return messages
    
    def rest(self, state: GameState) -> List[str]:
        """Rest to recover HP"""
        messages = []
        heal = 15
        before = state.player.hp
        state.player.hp = self.clamp(state.player.hp + heal, 0, state.player.maxhp)
        messages.append(f"你稍作休息（+{state.player.hp - before} HP）。")
        
        if random.random() < 0.35:
            messages.extend(self.ensure_enemy(state))
            if state.enemy:
                messages.append("（偷襲）黑影逼近，你還來不及完全放鬆。")
                messages.extend(self.enemy_turn(state))
        else:
            # Process player debuffs even out of combat
            messages.extend(self._process_player_debuffs(state))
        
        return messages
    
    # Quest System
    def _trigger_quest_events(self, state: GameState, event_type: str, **kwargs):
        """Trigger quest events"""
        for quest in state.quests.values():
            # Check if quest should start based on quest's start trigger
            if quest.state == QuestState.NOT_STARTED:
                # Get quest data to check start conditions
                world = self.get_current_world(state)
                quest_data = next((q for q in world.get("quests", []) if q["id"] == quest.id), None)
                
                if quest_data and "start" in quest_data:
                    start_config = quest_data["start"]
                    trigger_type = start_config.get("trigger")
                    
                    # Check if trigger conditions match
                    should_start = False
                    if trigger_type == "onEnter":
                        required_location = start_config.get("location")
                        current_location = kwargs.get("location")
                        should_start = (event_type == "onEnter" and current_location == required_location)
                    
                    if should_start:
                        quest.state = QuestState.ACTIVE
                        self._add_story(state, f"🗒️ 任務啟動：{quest.title}", "sys")
                        
                        # Initialize objective counts based on current inventory
                        for obj in quest.objectives:
                            if obj.type == "COLLECT_ITEM":
                                # Check if player already has the item in inventory
                                item_name = obj.item
                                if item_name in state.player.inventory:
                                    current_qty = state.player.inventory[item_name]
                                    required_qty = obj.qty or 1
                                    # Set count to current quantity (but not more than required)
                                    obj.count = min(current_qty, required_qty)
                                    if obj.count >= required_qty:
                                        obj.done = True
            
            # Update quest objectives
            if quest.state == QuestState.ACTIVE:
                changed = False
                for i, obj in enumerate(quest.objectives):
                    if obj.done:
                        continue
                    
                    # Check if all previous objectives are completed (sequential order)
                    if i > 0 and not all(quest.objectives[j].done for j in range(i)):
                        # Previous objectives not completed, skip this one
                        continue
                    
                    if obj.type == "REACH_LOCATION" and event_type == "onEnter":
                        if kwargs.get("location") == obj.location:
                            obj.done = True
                            changed = True
                    
                    elif obj.type == "DEFEAT_ENEMY" and event_type == "onDefeat":
                        if not obj.enemy or obj.enemy == kwargs.get("enemy"):
                            obj.count = (obj.count or 0) + 1
                            if obj.count >= (obj.qty or 1):
                                obj.done = True
                            changed = True
                    
                    elif obj.type == "COLLECT_ITEM" and event_type == "onPick":
                        if kwargs.get("item") == obj.item:
                            obj.count = (obj.count or 0) + kwargs.get("qty", 1)
                            if obj.count >= (obj.qty or 1):
                                obj.done = True
                            changed = True
                    
                    elif obj.type == "USE_ITEM" and event_type == "onUse":
                        if kwargs.get("item") == obj.item:
                            if not obj.context or obj.context == kwargs.get("context"):
                                obj.done = True
                                changed = True
                    
                    elif obj.type == "OBSERVE" and event_type == "onObserve":
                        if not obj.target or obj.target == kwargs.get("target"):
                            obj.done = True
                            changed = True
                
                # Check if quest completed
                if all(obj.done for obj in quest.objectives):
                    quest.state = QuestState.COMPLETED
                    self._add_story(state, f"✅ 任務完成：{quest.title}", "sys")
                    reward_messages = self._apply_quest_rewards(state, quest)
                    # Add reward messages to story
                    for msg in reward_messages:
                        self._add_story(state, msg, "sys")
                    
                    # Check if all quests completed (victory condition)
                    self._check_victory(state)
    
    def _apply_quest_rewards(self, state: GameState, quest: Quest) -> List[str]:
        """Apply quest rewards and return messages"""
        messages = []
        for reward in quest.rewards:
            if reward["type"] == "giveItem":
                messages.extend(self.add_item(state, reward["name"], reward.get("qty", 1)))
        
        return messages
    
    def _check_victory(self, state: GameState):
        """Check if all quests are completed and set victory state"""
        if not state.quests:
            return
        
        # Check if all quests are completed
        all_completed = all(quest.state == QuestState.COMPLETED for quest in state.quests.values())
        
        if all_completed:
            state.victory = True
            self._add_story(state, "\n🎉 恭喜！你完成了所有任務！", "sys")
            self._add_story(state, "=== 遊戲勝利 ===", "sys")
            self._add_story(state, "你成功解開了所有謎團，成為了傳說中的英雄！", "sys")
            self._add_story(state, "你可以重新開始遊戲或選擇其他場景。", "sys")
    
    def _add_story(self, state: GameState, text: str, msg_type: str = "sys"):
        """Add message to story log"""
        state.story.append({"text": text, "type": msg_type})
