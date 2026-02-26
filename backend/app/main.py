import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.models import GameAction, GameResponse, GameState
from app.nlp import ChineseNLP
from app.game_engine import GameEngine

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="FABLE Game API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game components
engine = GameEngine()
nlp = ChineseNLP(engine.data)  # Share the same GameData instance

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/game/start", response_model=GameResponse)
async def start_game(scenario: str, session_id: str = None):
    """Start a new game with selected scenario"""
    state = engine.get_or_create_session(session_id)
    messages = engine.start_game(state, scenario)
    
    # Add all opening messages to story
    for msg in messages:
        engine._add_story(state, msg, "sys")
    
    return GameResponse(
        state=state,
        message="\n".join(messages),
        message_type="sys"
    )

@app.post("/api/game/action", response_model=GameResponse)
async def execute_action(action: GameAction):
    """Execute a game action"""
    state = engine.get_or_create_session(action.session_id)
    
    if not state.scenario:
        raise HTTPException(status_code=400, detail="Game not started. Please start a game first.")
    
    # Check if game is over
    if state.game_over:
        return GameResponse(
            state=state,
            message="遊戲已結束。請重新開始遊戲。",
            message_type="sys"
        )
    
    # Check if game is won
    if state.victory:
        return GameResponse(
            state=state,
            message="你已經完成所有任務！請重新開始遊戲或選擇其他場景。",
            message_type="sys"
        )
    
    # Parse command with NLP
    intent = nlp.parse(action.command)
    messages = []
    msg_type = "sys"
    
    # Add player message to story
    engine._add_story(state, action.command, "player")
    
    # Handle different intents
    if intent.intent == "ATTACK":
        if not state.enemy:
            messages.extend(engine.ensure_enemy(state))
        
        # Smart weapon resolution: if weapon refers to something not in inventory,
        # check if it's a partial name and find matching weapons
        if intent.weapon:
            inventory_names = [item.name for item in state.player.inventory]
            if intent.weapon not in inventory_names:
                # Try to find weapons in inventory that contain the weapon name
                matching_weapons = []
                for item_name in inventory_names:
                    # Check if item_name contains the weapon name (e.g., "碎石" in "尖銳碎石")
                    if intent.weapon in item_name or item_name in intent.weapon:
                        matching_weapons.append(item_name)
                
                # Use first matching weapon
                if matching_weapons:
                    intent.weapon = matching_weapons[0]
        
        # 傳遞完整的intent對象以支持進階攻擊
        messages.extend(engine.player_attack(state, intent))
    
    elif intent.intent == "DEFEND":
        messages.extend(engine.player_defend(state))
    
    elif intent.intent == "OBSERVE":
        obj = intent.object or "四周"
        # Smart item resolution: if object refers to an item not in inventory,
        # check if it's a generic term (like "key") and find matching items in inventory
        if obj and obj != "四周":
            inventory_names = [item.name for item in state.player.inventory]
            
            # If parsed object is not in inventory, try to find items in inventory
            # that match the generic term (e.g., "key" → "森林古鑰")
            if obj not in inventory_names:
                # Extract generic terms from the command to match against inventory
                cmd_lower = action.command.lower()
                generic_terms = []
                
                # Common generic terms
                if "key" in cmd_lower or "鑰匙" in cmd_lower or "钥匙" in cmd_lower:
                    generic_terms.extend(["key", "鑰匙", "钥匙"])
                if "potion" in cmd_lower or "藥水" in cmd_lower:
                    generic_terms.extend(["potion", "藥水", "药水"])
                if "crystal" in cmd_lower or "水晶" in cmd_lower:
                    generic_terms.extend(["crystal", "水晶"])
                
                # Find items in inventory that contain these generic terms
                matching_items = []
                for item_name in inventory_names:
                    # Check against generic terms
                    for term in generic_terms:
                        if term in item_name.lower():
                            matching_items.append(item_name)
                            break
                    # Also check English equivalents
                    if not matching_items:
                        en_names = [en for en, cn in engine.data.en_to_cn.items() if cn == item_name]
                        for en_name in en_names:
                            for term in generic_terms:
                                if term in en_name.lower():
                                    matching_items.append(item_name)
                                    break
                            if matching_items:
                                break
                
                # Use first matching item from inventory
                if matching_items:
                    obj = matching_items[0]
        
        messages.extend(engine.observe(state, obj))
    
    elif intent.intent == "PICK":
        # Smart item resolution: prioritize items in current location's pickable_items
        item_name = intent.item
        
        if item_name and item_name != "未知物品":
            # Get current location's pickable items
            world = engine.get_current_world(state)
            location = world["locations"].get(state.location_id, {})
            pickable_items = location.get("pickable_items", [])
            pickable_names = [item["name"] for item in pickable_items]
            
            # Check if parsed item is not in pickable list
            if item_name not in pickable_names:
                # Try to find matching items in current location
                matching = []
                for pickable_name in pickable_names:
                    # Check if item_name is a substring or vice versa
                    if item_name in pickable_name or pickable_name in item_name:
                        matching.append(pickable_name)
                
                # Use first matching pickable item
                if matching:
                    item_name = matching[0]
        
        # Try to pick from location
        messages.extend(engine.pick_from_location(state, item_name))
        messages.extend(engine.ensure_enemy(state))
    
    elif intent.intent == "USE":
        item = intent.item
        # Smart item resolution: if item refers to something not in inventory,
        # check if it's a generic term (like "key") and find matching items in inventory
        inventory_names = [i.name for i in state.player.inventory]
        
        # If parsed item is not in inventory and not "未知物品"
        if item not in inventory_names and item != "未知物品":
            # Extract generic terms from the command
            cmd_lower = action.command.lower()
            generic_terms = []
            
            # Common generic terms
            if "key" in cmd_lower or "鑰匙" in cmd_lower or "钥匙" in cmd_lower:
                generic_terms.extend(["key", "鑰匙", "钥匙"])
            if "potion" in cmd_lower or "藥水" in cmd_lower:
                generic_terms.extend(["potion", "藥水", "药水"])
            if "crystal" in cmd_lower or "水晶" in cmd_lower or "shard" in cmd_lower or "碎片" in cmd_lower:
                generic_terms.extend(["crystal", "水晶", "shard", "碎片"])
            if "torch" in cmd_lower or "火把" in cmd_lower:
                generic_terms.extend(["torch", "火把"])
            
            # Find items in inventory that contain these generic terms
            matching_items = []
            for item_name in inventory_names:
                # Check against generic terms
                for term in generic_terms:
                    if term in item_name.lower():
                        matching_items.append(item_name)
                        break
                # Also check English equivalents
                if not matching_items:
                    en_names = [en for en, cn in engine.data.en_to_cn.items() if cn == item_name]
                    for en_name in en_names:
                        for term in generic_terms:
                            if term in en_name.lower():
                                matching_items.append(item_name)
                                break
                        if matching_items:
                            break
            
            # Use first matching item from inventory
            if matching_items:
                item = matching_items[0]
        
        # 支持帶修飾詞的使用（如"使用治療藥水然後後退"）
        messages.extend(engine.use_item(state, item))
        if hasattr(intent, 'modifiers') and intent.modifiers:
            if "後退" in intent.modifiers or "retreat" in intent.modifiers:
                messages.append("你使用後謹慎地後退，保持距離。")
                state.player.buffs.evasion = 0.1
    
    elif intent.intent == "MOVE":
        location = intent.location
        # If NLP couldn't match the location, try translating it via en_to_cn
        if location == "未知地點":
            # Extract location name from original command
            cmd_lower = action.command.lower()
            for move_word in ["go to", "前往", "移動到", "去"]:
                if move_word in cmd_lower:
                    # Get text after the move keyword
                    parts = cmd_lower.split(move_word, 1)
                    if len(parts) > 1:
                        potential_location = parts[1].strip()
                        # Remove common articles
                        potential_location = potential_location.replace("the ", "").strip()
                        
                        # Get current world to validate locations
                        world = engine.get_current_world(state)
                        
                        # Helper function to check if name is a valid location
                        def is_valid_location(name: str) -> bool:
                            for loc_id, loc_data in world["locations"].items():
                                if (loc_data["name"] == name or 
                                    loc_id == name or
                                    loc_data.get("en_name", "").lower() == name.lower()):
                                    return True
                            return False
                        
                        # Try different translations and check if they're valid locations
                        candidates = [
                            potential_location,
                            f"old {potential_location}",
                            f"ancient {potential_location}",
                            f"{potential_location} hall",
                            f"{potential_location} room"
                        ]
                        
                        for candidate in candidates:
                            if candidate in engine.data.en_to_cn:
                                translated = engine.data.en_to_cn[candidate]
                                # Check if this translation is actually a location
                                if is_valid_location(translated):
                                    location = translated
                                    break
                        break
        
        messages.extend(engine.move_to(state, location))
    
    elif intent.intent == "REST":
        messages.extend(engine.rest(state))
    
    elif intent.intent == "ESCAPE":
        # 檢查是否是威嚇意圖
        if hasattr(intent, 'sentiment') and intent.sentiment == "intimidating":
            messages.extend(engine.handle_intimidation(state, intent.sentiment))
        else:
            messages.extend(engine.escape(state))
    
    elif intent.intent == "TALK":
        # 功能2：情境感知對話
        if hasattr(intent, 'sentiment'):
            if state.enemy:
                messages.extend(engine.handle_intimidation(state, intent.sentiment))
            else:
                if intent.sentiment == "friendly":
                    messages.append("你友善地打招呼，但這裡暫時沒有回應。")
                else:
                    messages.append("你試著交談，但這裡暫時沒有回應。")
        else:
            messages.append("你試著交談，但這裡暫時沒有回應。")
        messages.extend(engine.ensure_enemy(state))
    
    elif intent.intent == "QUESTION":
        # 功能4：環境互動問答系統
        messages.extend(engine.handle_environment_question(state, intent))
        messages.extend(engine.ensure_enemy(state))
    
    elif intent.intent == "QUEST_LIST":
        messages.append("（任務列表已於右側面板顯示）")
    
    else:
        messages.append("我未聽明白（NLU 未匹配）。試試「攻擊狼／使用治療藥水／觀察四周」。")
        messages.extend(engine.ensure_enemy(state))
    
    # Add messages to story
    for msg in messages:
        if isinstance(msg, dict) and "text" in msg and "type" in msg:
            # 處理帶有類型的消息（如敵人出現）
            engine._add_story(state, msg["text"], msg["type"])
        else:
            # 普通字符串消息
            engine._add_story(state, msg, msg_type)
    
    # Prepare plain text messages for response
    plain_messages = []
    for msg in messages:
        if isinstance(msg, dict) and "text" in msg:
            plain_messages.append(msg["text"])
        else:
            plain_messages.append(msg)
    
    return GameResponse(
        state=state,
        message="\n".join(plain_messages),
        message_type=msg_type
    )

@app.get("/api/game/state/{session_id}", response_model=GameState)
async def get_game_state(session_id: str):
    """Get current game state"""
    state = engine.get_or_create_session(session_id)
    return state

@app.get("/api/scenarios")
async def get_scenarios():
    """Get available game scenarios"""
    from app.game_data import GameData
    data = GameData()
    return {
        "scenarios": [
            {"id": key, **value}
            for key, value in data.get_scenarios().items()
        ]
    }

# Get the absolute path to the frontend build directory
# First check if build is in backend/static (Azure deployment)
frontend_build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

# If not found, check for frontend/dist (local development - Vite default)
if not os.path.exists(frontend_build_path):
    frontend_build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "frontend/dist"))

print(f"Frontend build path: {frontend_build_path}")
print(f"Static directory exists: {os.path.exists(os.path.join(frontend_build_path, 'dist'))}")

# Serve static files from React build
if os.path.exists(os.path.join(frontend_build_path, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_build_path, "assets")), name="assets")
if os.path.exists(os.path.join(frontend_build_path, "dist")):
    app.mount("/dist", StaticFiles(directory=os.path.join(frontend_build_path, "dist")), name="dist")

# Serve images directory (from frontend/dist/images or frontend/public/images)
images_path = os.path.join(frontend_build_path, "images")
if not os.path.exists(images_path):
    # Fallback to public/images during development
    images_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "frontend/public/images"))
if os.path.exists(images_path):
    app.mount("/images", StaticFiles(directory=images_path), name="images")
    print(f"Images directory mounted: {images_path}")
else:
    print(f"Warning: Images directory not found at {images_path}")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve the React app for all non-API routes to support client-side routing"""
    # Skip API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check if the path is requesting a specific file (has an extension)
    if "." in full_path and not full_path.endswith(".html"):
        # Try to serve the file from the build directory
        file_path = os.path.join(frontend_build_path, full_path)
        if os.path.exists(file_path):
            return FileResponse(file_path)
    
    # For all other paths, serve the main index.html
    index_path = os.path.join(frontend_build_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # If no index.html, return API info
    return {"message": "FABLE Game API", "version": "1.0.0", "docs": "/docs"}