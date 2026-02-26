# Game Data (converted from JavaScript)
from typing import Dict, List, Any

# Import data from modular files
from .data.items import ITEMS
from .data.weapons import WEAPONS
from .data.enemies import ENEMIES
from .data.worlds import WORLDS
from .data.synonyms import SYNONYMS

class GameData:
    items = ITEMS
    weapons = WEAPONS
    enemies = ENEMIES
    worlds = WORLDS
    synonyms = SYNONYMS

    # Auto-generate lexicon and mappings from worlds
    def __init__(self):
        """Initialize and auto-generate lexicons from world data"""
        # Store full data references
        self._all_enemies = ENEMIES
        self._all_items = ITEMS
        self._all_weapons = WEAPONS
        
        # Active data (will be loaded when scenario is selected)
        self.enemies = {}
        self.items = {}
        self.weapons = {}
        self.current_world = None
        self.lexicon = {"enemies": [], "items": [], "locations": []}
        self.en_to_cn = {}
        self.clue_names = []
    
    def load_scenario_data(self, scenario_id: str):
        """Load only data needed for the selected scenario"""
        world = self.get_world_by_id(scenario_id)
        if not world:
            return
        
        self.current_world = world
        
        # Extract enemy IDs used in this world
        used_enemy_ids = set()
        for loc_id, loc_data in world["locations"].items():
            spawns = loc_data.get("spawns", [])
            for spawn in spawns:
                # spawns can be either string "enemy_id:chance" or dict {"id": "enemy_id", "chance": 0.5}
                if isinstance(spawn, str):
                    enemy_id = spawn.split(":")[0]
                    used_enemy_ids.add(enemy_id)
                else:
                    used_enemy_ids.add(spawn["id"])
        
        # Filter enemies - only load enemies used in this world
        self.enemies = {
            enemy_id: enemy_data 
            for enemy_id, enemy_data in self._all_enemies.items() 
            if enemy_id in used_enemy_ids
        }
        
        # Extract item IDs used in this world (from inventory, drops, clues, etc.)
        used_item_ids = set()
        
        # 1. From initial inventory
        for item in world.get("initial_inventory", []):
            used_item_ids.add(item["name"])
        
        # 2. From enemy drops
        for enemy_id in used_enemy_ids:
            enemy_data = self._all_enemies.get(enemy_id, {})
            for drop in enemy_data.get("drops", []):
                used_item_ids.add(drop["item"])
        
        # 3. From quest rewards
        for quest in world.get("quests", []):
            for reward in quest.get("rewards", []):
                if reward.get("type") == "giveItem":
                    used_item_ids.add(reward["name"])
        
        # 4. From location clues (items given when observing/searching)
        for loc_id, loc_data in world["locations"].items():
            clues = loc_data.get("clues", {})
            for clue_name, clue_data in clues.items():
                if "give_item" in clue_data:
                    items = clue_data["give_item"]
                    if isinstance(items, str):
                        used_item_ids.add(items)
                    else:
                        used_item_ids.update(items)
        
        # Filter items
        self.items = {
            item_id: item_data 
            for item_id, item_data in self._all_items.items() 
            if item_id in used_item_ids
        }
        
        # Extract weapon IDs used in this world
        used_weapon_ids = set()
        
        # 1. From initial inventory
        for item in world.get("initial_inventory", []):
            if item["name"] in self._all_weapons:
                used_weapon_ids.add(item["name"])
        
        # 2. From pickable items in locations
        for loc_id, loc_data in world["locations"].items():
            pickable = loc_data.get("pickable_items", [])
            for item in pickable:
                if item["name"] in self._all_weapons:
                    used_weapon_ids.add(item["name"])
        
        # 3. From enemy drops (weapons can be dropped too)
        for enemy_id in used_enemy_ids:
            enemy_data = self._all_enemies.get(enemy_id, {})
            for drop in enemy_data.get("drops", []):
                if drop["item"] in self._all_weapons:
                    used_weapon_ids.add(drop["item"])
        
        # Filter weapons
        self.weapons = {
            weapon_id: weapon_data 
            for weapon_id, weapon_data in self._all_weapons.items() 
            if weapon_id in used_weapon_ids
        }
        
        print(f"📦 Loaded scenario '{world['name']}':")
        print(f"   - {len(self.enemies)} enemies")
        print(f"   - {len(self.items)} items")
        print(f"   - {len(self.weapons)} weapons: {list(self.weapons.keys())}")
        print(f"   - {len(world['locations'])} locations")
        
        # Rebuild lexicon and mappings for the filtered data
        self._rebuild_lexicon_for_world(world)
    
    def _rebuild_lexicon_for_world(self, world):
        """Rebuild lexicon and mappings for specific world"""
        # Auto-generate enemy names from filtered enemies
        cn_enemies = []
        for enemy_id, enemy_data in self.enemies.items():
            enemy_name = enemy_data["name"]
            if enemy_name not in cn_enemies:
                cn_enemies.append(enemy_name)
            if "abbr" in enemy_data and enemy_data["abbr"] not in cn_enemies:
                cn_enemies.append(enemy_data["abbr"])
        
        # Auto-generate item names
        cn_items = list(self.items.keys())
        cn_items.extend(list(self.weapons.keys()))
        
        print(f"\n🔧 _rebuild_lexicon_for_world:")
        print(f"   - cn_items (含武器): {cn_items}")
        
        # Generate Chinese location names for this world only
        cn_locations = []
        en_locations = []
        en_to_cn_map = {}
        
        for loc_id, loc_data in world["locations"].items():
            cn_name = loc_data["name"]
            en_name = loc_data.get("en_name", loc_id)
            
            if cn_name not in cn_locations:
                cn_locations.append(cn_name)
            
            en_lower = en_name.lower()
            if en_lower not in en_locations:
                en_locations.append(en_lower)
            
            # Add short forms
            words = en_lower.split()
            if len(words) > 1 and words[-1] not in en_locations:
                en_locations.append(words[-1])
            
            en_to_cn_map[en_lower] = cn_name
            if len(words) > 1:
                en_to_cn_map[words[-1]] = cn_name
        
        # Rebuild lexicon
        self.lexicon = {
            "enemies": cn_enemies,
            "items": cn_items,
            "locations": cn_locations
        }
        
        print(f"   - lexicon['items']: {self.lexicon['items']}")
        
        # Rebuild en_to_cn mapping
        self.en_to_cn = {}
        
        # Enemy mappings
        for enemy_id, enemy_data in self.enemies.items():
            cn_name = enemy_data["name"]
            if "en_id" in enemy_data:
                self.en_to_cn[enemy_data["en_id"]] = cn_name
            if "en_name" in enemy_data:
                self.en_to_cn[enemy_data["en_name"].lower()] = cn_name
            if "abbr" in enemy_data:
                self.en_to_cn[enemy_data["abbr"]] = cn_name
        
        # Item mappings
        for cn_item_name, item_data in self.items.items():
            if "en_name" in item_data:
                en_name = item_data["en_name"]
                self.en_to_cn[en_name.lower()] = cn_item_name
                words = en_name.lower().split()
                if len(words) > 1:
                    self.en_to_cn[words[-1]] = cn_item_name
        
        # Weapon mappings
        for cn_weapon_name, weapon_data in self.weapons.items():
            if "en_name" in weapon_data:
                en_name = weapon_data["en_name"]
                self.en_to_cn[en_name.lower()] = cn_weapon_name
                words = en_name.lower().split()
                if len(words) > 1:
                    self.en_to_cn[words[-1]] = cn_weapon_name
        
        print(f"   - Weapon mappings in en_to_cn:")
        for en_key, cn_val in self.en_to_cn.items():
            if cn_val in self.weapons:
                print(f"     '{en_key}' -> '{cn_val}'")
        
        # Location mappings (including short forms from en_to_cn_map)
        self.en_to_cn.update(en_to_cn_map)
        
        # Special terms
        self.en_to_cn["around"] = "四周"
        
        # Clue mappings for this world
        for loc_id, loc_data in world["locations"].items():
            if "clues" in loc_data:
                for cn_clue_name, clue_data in loc_data["clues"].items():
                    if "en_name" in clue_data:
                        en_name = clue_data["en_name"]
                        self.en_to_cn[en_name.lower()] = cn_clue_name
                        if not en_name.endswith('s'):
                            self.en_to_cn[en_name.lower() + 's'] = cn_clue_name
        
        # Extract clue names for this world
        clue_names = set()
        for loc_id, loc_data in world["locations"].items():
            if "clues" in loc_data:
                for clue_name in loc_data["clues"].keys():
                    clue_names.add(clue_name)
        self.clue_names = list(clue_names)
    
    def get_world_by_id(self, world_id: str):
        """Get world data by scenario id"""
        for world in self.worlds:
            if world["id"] == world_id:
                return world
        return None
    
    def get_scenarios(self):
        """Get list of available scenarios for selection menu"""
        scenarios = {}
        for world_data in self.worlds:
            # Extract location names for display
            location_names = [loc["name"] for loc in world_data["locations"].values()]
            
            scenarios[world_data["id"]] = {
                "name": world_data["name"],
                "en_name": world_data.get("en_name", world_data["name"]),
                "description": world_data.get("description", ""),
                "difficulty": world_data.get("difficulty", 3),  # 添加难度字段，默认为3（中等）
                "cover_image": world_data.get("cover_image"),
                "opening": world_data["opening"],
                "locations": location_names
            }
        return scenarios
