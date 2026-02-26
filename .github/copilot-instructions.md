# Copilot Instructions

## Project Overview
Full-stack Chinese NLP text adventure game (FABLE) with:
- Frontend: React 19 + TypeScript + Vite
- Backend: Python 3.11 + FastAPI
- Features: NLP command parsing, turn-based combat, quest system, inventory management

## Technology Stack
- **Frontend**: React, TypeScript, Vite, CSS3
- **Backend**: FastAPI, Pydantic, Python
- **NLP**: Custom Chinese language parser
- **State**: React Context API, In-memory sessions

## Project Status
✅ **INTEGRATION COMPLETE** - All systems operational

### Completed Features
- [x] Created copilot-instructions.md
- [x] Scaffolded React frontend with TypeScript
- [x] Created Python FastAPI backend
- [x] Implemented game engine (combat, inventory, quests)
- [x] Built Chinese NLP parser
- [x] Created REST API (5 endpoints)
- [x] Built React UI components (ScenarioPicker, GameScreen)
- [x] Added state management (GameContext)
- [x] Implemented responsive styling
- [x] Created comprehensive documentation
- [x] Installed all dependencies

## Key Files

### Backend
- `backend/app/main.py` - API routes
- `backend/app/game_engine.py` - Core game logic (600+ lines)
- `backend/app/nlp.py` - Chinese NLP parser
- `backend/app/models.py` - Pydantic data models
- `backend/app/game_data.py` - Game content

### Frontend
- `frontend/src/App.tsx` - Main application
- `frontend/src/context/GameContext.tsx` - State management
- `frontend/src/components/GameScreen.tsx` - Main game UI
- `frontend/src/components/ScenarioPicker.tsx` - Scenario selection
- `frontend/src/services/api.ts` - API client

### Documentation
- `README.md` - Main documentation
- `INTEGRATION_GUIDE.md` - Integration details
- `INTEGRATION_COMPLETE.md` - Completion summary
- `ARCHITECTURE.md` - System architecture
- `QUICK_REFERENCE.md` - Player guide

## How to Run

### Quick Start
```bash
.\start.cmd
```
Opens at http://localhost:8000

### Development Mode
Terminal 1: `cd backend && .venv\Scripts\activate && uvicorn app.main:app --reload`
Terminal 2: `cd frontend && npm run dev`

## API Endpoints
- `GET /api/scenarios` - List scenarios
- `POST /api/game/start` - Start game
- `POST /api/game/action` - Execute command
- `GET /api/game/state/{id}` - Get state
- `GET /api/health` - Health check

## Game Commands (Chinese)
- 攻擊 [敵人] - Attack
- 防禦 - Defend
- 觀察 [對象/四周] - Observe
- 前往 [地點] - Move
- 拾取 [物品] - Pick up
- 使用 [物品] - Use item
- 休息 - Rest

## Architecture
- Frontend: Component-based React with Context API
- Backend: FastAPI with Pydantic models
- NLP: Intent recognition + entity extraction
- Game Logic: Turn-based engine with AI
- State: In-memory sessions (no persistence yet)

## Future Enhancements
- Database integration for persistence
- User authentication system
- Advanced NLP with spaCy
- More scenarios and content
- Multiplayer support
- Save/load functionality
