# FABLE - Chinese NLP Text Adventure Game

A full-stack web application featuring a Chinese text-based adventure game with advanced natural language processing capabilities. Built with React (Vite) frontend and Python (FastAPI) backend, powered by BERT machine learning models.

## 🆕 What's New (v2.0)

- **🤖 BERT Intent Classification**: Fine-tuned transformer model for accurate command understanding
- **🧠 Semantic Similarity**: BERT embeddings for intelligent entity matching
- **⚔️ Advanced Combat**: Body part targeting, attack style modifiers, sentiment-aware interactions
- **🎓 Tutorial System**: New beginner-friendly training camp scenario
- **📊 NLP Testing Suite**: 250+ test cases with 91%+ success rate
- **🌐 Bilingual Support**: Seamless Chinese ⇄ English command processing
- **📈 Difficulty System**: Progressive 5-level difficulty ratings for all scenarios

## Features

- **🤖 Advanced Natural Language Processing**: 
  - BERT-based intent classification with trained models
  - Semantic similarity matching using multilingual BERT embeddings
  - Support for both Chinese and English commands
  - Body part targeting, attack styles, sentiment analysis
  - Question pattern recognition and fuzzy matching
- **📖 Text-Based Adventure**: Interactive storytelling with multiple scenarios and difficulty levels
- **⚔️ Combat System**: Turn-based combat with tactical options, body part targeting, and attack modifiers
- **📜 Quest System**: Dynamic quests with objectives and rewards
- **🎒 Inventory Management**: Collect and use items throughout your journey
- **🗺️ AI Map Generation**: Optional AI-powered ASCII map visualization
- **🎓 Tutorial System**: Guided training camp for new players
- **⚡ Real-time State Management**: Seamless client-server communication

## Project Structure

```
Project Code/
├── frontend/              # React + Vite frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   │   ├── ScenarioPicker.tsx
│   │   │   ├── GameScreen.tsx
│   │   │   └── *.css
│   │   ├── context/       # React context
│   │   │   └── GameContext.tsx
│   │   ├── services/      # API service
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── App.css
│   ├── public/
│   └── package.json
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── main.py       # API endpoints
│   │   ├── models.py     # Pydantic models
│   │   ├── game_data.py  # Game data & configuration
│   │   ├── game_engine.py # Game logic & engine (1700+ lines)
│   │   ├── nlp.py        # NLP processing engine (900+ lines)
│   │   ├── embedding_utils.py # BERT embeddings & similarity
│   │   └── data/         # Game content data
│   │       ├── synonyms.py    # Intent synonym mappings
│   │       ├── worlds.py      # World definitions
│   │       ├── enemies.py     # Enemy data
│   │       ├── items.py       # Item data
│   │       ├── weapons.py     # Weapon data
│   │       ├── tutorial_data.py        # Tutorial world
│   │       ├── advanced_tutorial_data.py # Advanced tutorial
│   │       └── qin_dynasty_data.py     # Qin dynasty scenario
│   ├── models/           # Trained ML models
│   │   └── intent_classifier/ # BERT intent classification model
│   │       ├── config.json
│   │       ├── model.safetensors
│   │       ├── tokenizer.json
│   │       └── label_map.json
│   ├── model_training/   # Model training scripts
│   │   ├── train_intent_model.py
│   │   ├── prepare_training_data_v2.py
│   │   └── intent_training_data_enhanced.json
│   ├── requirements.txt
│   └── .env.example
├── useful_info/          # Project reference materials
├── NLP_PROJECT_REPORT.md # Detailed NLP analysis
├── TUTORIAL_GUIDE.md     # Tutorial world guide
├── QIN_DYNASTY_GUIDE.md  # Qin dynasty scenario guide
├── GAME_DATA_REFERENCE.md # Game data documentation
└── README.md
```

## Technology Stack

### Frontend
- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite 7** - Build tool & dev server
- **CSS3** - Styling with custom properties

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Python 3.11** - Core language
- **Uvicorn** - ASGI server

### NLP & Machine Learning
- **PyTorch 2.1** - Deep learning framework
- **Transformers 4.35** - Hugging Face library for BERT models
- **BERT** - Multilingual BERT for embeddings and intent classification
- **scikit-learn** - Machine learning utilities
- **NumPy** - Numerical computing

## Key Backend Files

### Core Systems
- **`backend/app/main.py`** - FastAPI application and REST endpoints
- **`backend/app/game_engine.py`** (1700+ lines) - Complete game logic including:
  - Combat system with tactical options
  - Quest management and progression
  - Inventory and item usage
  - World state management
  - AI opponent behavior
  - Boss fight mechanics

### NLP System
- **`backend/app/nlp.py`** (900+ lines) - Advanced NLP processor featuring:
  - BERT intent classification integration
  - Semantic similarity matching
  - Entity extraction (enemies, items, body parts)
  - Attack style recognition
  - Sentiment analysis
  - Question pattern detection
  - Bilingual command processing
  
- **`backend/app/embedding_utils.py`** - BERT embedding utilities:
  - Text embedding extraction
  - Semantic similarity calculation
  - Candidate ranking for entity matching

### Data Models & Content
- **`backend/app/models.py`** - Pydantic data models (GameState, CommandIntent, etc.)
- **`backend/app/game_data.py`** - Game data aggregator
- **`backend/app/data/`** - Game content modules:
  - `worlds.py` - World/scenario definitions
  - `enemies.py` - Enemy data with body parts
  - `items.py` - Item definitions
  - `weapons.py` - Weapon statistics
  - `tutorial_data.py` - Tutorial scenario
  - `qin_dynasty_data.py` - Historical scenario
  - `synonyms.py` - Intent synonym mappings

### Machine Learning
- **`backend/models/intent_classifier/`** - Pre-trained BERT model files:
  - `model.safetensors` - Model weights
  - `config.json` - Model configuration
  - `tokenizer.json` - BERT tokenizer
  - `label_map.json` - Intent label mappings
  
- **`backend/model_training/`** - Training pipeline:
  - `train_intent_model.py` - Model training script
  - `prepare_training_data_v2.py` - Data preparation
  - `intent_training_data_enhanced.json` - 800+ labeled examples

### Testing
- **`backend/test_nlp_accuracy.py`** - NLP test suite with 250+ cases
- **`backend/test_nlp_dataset.json`** - Comprehensive test dataset

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git (optional)

### Quick Start with start.cmd (Windows)

Simply run the included batch script:

```bash
.\start.cmd
```

This will:
1. Set up Python virtual environment
2. Install backend dependencies
3. Install frontend dependencies
4. Build the frontend
5. Start the combined server at http://localhost:8000

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend API will be available at:
   - Main: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/health`

#### Frontend Setup (Development Mode)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

4. Build for production:
   ```bash
   npm run build
   ```

## API Endpoints

### Game Endpoints

- `GET /api/scenarios` - Get available game scenarios
- `POST /api/game/start?scenario={id}` - Start a new game
- `POST /api/game/action` - Execute a game command
  ```json
  {
    "command": "攻擊狼",
    "session_id": "uuid"
  }
  ```
- `GET /api/game/state/{session_id}` - Get current game state
- `GET /api/health` - Health check

## Game Commands (Chinese & English)

The advanced NLP system understands both Chinese and English commands with rich variations:

### Combat
- **攻擊 / attack** [敵人名稱] [身體部位] [方式] - Attack an enemy
  - Examples: 
    - `攻擊狼` / `attack wolf`
    - `快速攻擊狼的頭部` / `quickly attack wolf's head`
    - `用力攻擊` / `attack with full strength`
    - `精準攻擊眼睛` / `precisely attack eyes`
- **防禦 / defend** - Enter defensive stance
- **休息 / rest** - Rest to recover HP

### Attack Modifiers (Advanced Combat)
- **快速 / quickly** - Quick attacks (higher accuracy, less damage)
- **用力 / heavily** - Heavy attacks (more damage, lower accuracy)
- **精準 / precisely** - Precise attacks (critical hit bonus)
- **小心 / carefully** - Defensive attacks (reduced counter damage)

### Body Part Targeting
Target specific enemy weak points for bonus damage:
- 頭/head, 眼睛/eyes, 腿/legs, 尾巴/tail, 身體/body
- 腹部/belly, 手臂/arms, 翅膀/wings, 鉗子/claws
- 核心/core, 骨骼/skeleton, 護甲/armor

### Exploration
- **觀察 / look** [對象/四周] - Observe surroundings or objects
- **前往 / go to** [地點] - Move to a location
- **拾取 / pick** [物品] - Pick up an item
- **使用 / use** [物品] - Use an item

### Examples with Sentiment
The NLP system also detects sentiment in your commands:
- **Friendly**: `請幫我觀察四周` / `please help me look around`
- **Hostile**: `去死吧！攻擊` / `die! attack`
- **Intimidating**: `投降吧，別逼我` / `surrender, don't push me`

## Game Scenarios

All scenarios feature progressive difficulty ratings (⭐-⭐⭐⭐⭐⭐):

### 🎓 冒險者訓練營 (Adventurer Training Camp) - ⭐ BEGINNER
**NEW!** Perfect for first-time players! Learn all the basic commands in a safe environment.

- **Setting**: Training grounds with guided instructions
- **Locations**: 3 training areas (Training Ground → Equipment Room → Rest Area)
- **Enemies**: 2 types (Training Dummy, Weak Slime) - non-threatening
- **Quests**: 8-step tutorial covering all basic commands
- **Features**: 
  - Step-by-step command tutorials
  - Safe combat practice
  - Item management basics
  - No real danger - focus on learning
- **Recommended for**: First-time players, learning the game mechanics
- **Playtime**: 20-30 minutes

📖 **[Complete Tutorial Guide](TUTORIAL_GUIDE.md)**

### 🆕 尋秦記：戰國風雲 (A Step Into The Past) - ⭐⭐⭐⭐⭐ EXPERT
**ADVANCED CONTENT!** Experience the Warring States period and protect the future First Emperor from legendary assassin Jing Ke!

- **Setting**: Ancient China, 227 BC - The assassination attempt that changed history
- **Locations**: 6 interconnected areas (Handan → Xianyang → Qin Palace)
- **Enemies**: 5 types including 2 challenging BOSS fights
- **Quests**: 13-step main storyline + weapon crafting side quest
- **Features**: 
  - Historical characters and events
  - Strategic boss battles (Imperial Commander, Jing Ke)
  - Weapon crafting system (forge Qin Sword)
  - Complex item synthesis (Tiger Tally fragments)
  - BOSS fights with no escape - prepare well!
- **Recommended for**: Advanced players who master combat mechanics
- **Playtime**: 2-3 hours

📖 **[Complete Guide](QIN_DYNASTY_GUIDE.md)** | 🎮 **[Quick Start](QIN_QUICKSTART.md)**

### Classic Scenarios

1. **迷霧森林 (Misty Forest)** - ⭐⭐⭐ Ancient woods shrouded in mist with lurking beasts
2. **低語之沙 (Whispering Sands)** - ⭐⭐⭐⭐ Desert wasteland with haunting spirits
3. **遺忘之城 (Forgotten City)** - ⭐⭐⭐⭐ Ruined city with ancient mechanisms

> **Difficulty Ratings:**
> - ⭐ Beginner: Tutorial, safe learning environment
> - ⭐⭐ Easy: Basic enemies, straightforward quests
> - ⭐⭐⭐ Medium: Mixed enemy types, some puzzles
> - ⭐⭐⭐⭐ Hard: Strong enemies, complex objectives
> - ⭐⭐⭐⭐⭐ Expert: Boss fights, advanced mechanics, no escape options

## Development

### Model Training (Advanced)

The project includes tools for training custom BERT intent classification models:

```bash
cd backend

# Prepare training data
python model_training/prepare_training_data_v2.py

# Train the model
python model_training/train_intent_model.py

# Test NLP accuracy
python test_nlp_accuracy.py
```

**Training Data**: `backend/model_training/intent_training_data_enhanced.json` contains 800+ labeled examples

**Pre-trained Model**: The repository includes a pre-trained BERT intent classifier in `backend/models/intent_classifier/`

### Frontend Commands

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Backend Commands

- `uvicorn app.main:app --reload` - Development server with hot reload
- `uvicorn app.main:app` - Production server
- `python -m pytest` - Run tests (if implemented)

### Environment Variables

#### Backend (.env in backend/)

```env
HOST=0.0.0.0
PORT=8000

# Optional: AI Map Generation Feature
OPENAI_API_KEY=your_openai_api_key_here
```

#### Frontend (.env in frontend/)

```env
VITE_API_URL=http://localhost:8000
```

### AI Map Generation Feature 🗺️

**New!** The game now supports AI-powered text map generation. When players use the "舊地圖" (old map) item, an AI model generates a visual ASCII map showing all locations and connections.

**Setup:**
1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Create `backend/.env` file and add: `OPENAI_API_KEY=your_key_here`
3. Install dependencies: `pip install -r requirements.txt`

**Usage in game:**
- `觀察 地圖` - View basic map description
- `使用 地圖` - Generate AI-powered text map
- `use map` - English command also works

See [MAP_FEATURE.md](MAP_FEATURE.md) for detailed documentation.

**Note:** This feature is optional. Without an API key, the map item will still work but show a notice about the feature being unavailable.

## Architecture

### Frontend Architecture
- **Component-based UI**: Modular React components
- **Context API**: Global state management
- **Service Layer**: Abstracted API calls
- **Type Safety**: Full TypeScript support

### Backend Architecture
- **RESTful API**: Clean, resource-oriented endpoints
- **Game Engine**: Separate game logic from API layer
- **NLP Module**: Dedicated Chinese/English language processing with BERT
- **ML Models**: Pre-trained BERT intent classifier and embeddings
- **Session Management**: In-memory game state storage
- **Pydantic Models**: Type-safe data validation

### NLP Pipeline Architecture

```
User Input (Chinese/English)
        ↓
Text Normalization
        ↓
┌───────────────────────────────┐
│   Intent Classification       │
│   (BERT Model)                │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│   Entity Extraction           │
│   - Enemies (Semantic Match)  │
│   - Body Parts                │
│   - Items/Weapons             │
│   - Locations                 │
└───────────┬───────────────────┘
            ↓
┌───────────────────────────────┐
│   Modifier Extraction         │
│   - Attack Styles             │
│   - Sentiment Analysis        │
│   - Question Patterns         │
└───────────┬───────────────────┘
            ↓
    CommandIntent Object
        ↓
    Game Engine Processing
```

## NLP Features

The advanced Chinese/English NLP system implements multiple sophisticated techniques:

### 🎯 Core NLP Capabilities

1. **BERT-Based Intent Classification**
   - Fine-tuned multilingual BERT model for intent recognition
   - Trained on 800+ Chinese and English command examples
   - Located in `backend/models/intent_classifier/`
   - Supports 10+ intent types with high accuracy

2. **Semantic Similarity Matching**
   - BERT embeddings for deep semantic understanding
   - Cosine similarity for entity matching (enemies, items, locations)
   - Flexible matching even with typos or variations
   - Multilingual support (Chinese & English)

3. **Entity Extraction**
   - Enemy names with fuzzy matching
   - Body part targeting (15+ targetable parts)
   - Item and weapon identification
   - Location extraction

4. **Attack Style Recognition**
   - Quick (快速/quickly): Higher accuracy, less damage
   - Heavy (用力/heavily): More damage, lower accuracy  
   - Precise (精準/precisely): Critical hit bonus
   - Defensive (小心/carefully): Reduced counter damage

5. **Sentiment Analysis**
   - Friendly sentiment: Polite, helpful expressions
   - Hostile sentiment: Aggressive, angry language
   - Intimidating sentiment: Threatening, fear-inducing words
   - Affects NPC reactions and combat dynamics

6. **Question Pattern Recognition**
   - Search questions (有什麼/what, 看到/see)
   - Origin questions (從哪/where from)
   - Method questions (怎麼/how to)
   - Reason questions (為什麼/why)

7. **Contextual Understanding**
   - Commands adapt based on game state
   - Context-aware entity resolution
   - Dynamic synonym mapping

8. **Fuzzy Matching**
   - Typo tolerance using SequenceMatcher
   - Flexible command parsing
   - Multiple synonyms per action

### 📊 Technical Implementation

- **Preprocessing**: Text normalization, punctuation handling
- **Intent Detection**: BERT classifier + keyword rules
- **Entity Resolution**: Embedding similarity + fuzzy string matching
- **Modifier Extraction**: Pattern matching for combat modifiers
- **Bilingual Support**: Seamless Chinese ⇄ English processing

### 📈 Performance Metrics

Based on testing with 250+ test cases:
- **Intent Recognition**: 96%+ accuracy
- **Entity Extraction**: 92%+ accuracy
- **Overall Success Rate**: 91%+ for complex commands

See [NLP_PROJECT_REPORT.md](NLP_PROJECT_REPORT.md) for detailed analysis and testing results.

## Future Enhancements

- [ ] Persistent storage (database integration for save games)
- [ ] User authentication and player profiles
- [ ] Enhanced NLP with transformer fine-tuning for dialogue generation
- [ ] Multiplayer/co-op modes
- [ ] More scenarios and storylines (historical periods, fantasy settings)
- [ ] Achievement system with unlockable content
- [ ] Save/load game functionality
- [ ] Mobile-responsive UI improvements
- [ ] Voice input support with speech recognition
- [ ] AI-generated dynamic quest content
- [ ] Real-time combat animations
- [ ] Equipment upgrade and crafting systems
- [ ] Character class selection and skill trees

## CORS Configuration

The backend is configured to accept requests from any origin during development. For production, update the CORS settings in `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

### Backend Issues

1. **Import errors**: Make sure virtual environment is activated
2. **Port already in use**: Change port with `--port 8001`
3. **Module not found**: Run `pip install -r requirements.txt`
4. **PyTorch/BERT loading issues**: 
   - Ensure you have enough RAM (4GB+ recommended)
   - PyTorch will use CPU if CUDA is not available (slower but functional)
   - On first run, BERT models will be downloaded (~400MB)

### Frontend Issues

1. **API connection failed**: Check backend is running on port 8000
2. **Build errors**: Delete `node_modules` and run `npm install` again
3. **TypeScript errors**: Run `npm run lint` to see specific issues

### NLP/Model Issues

1. **BERT model not loading**: 
   - Check that `backend/models/intent_classifier/` exists with model files
   - Verify PyTorch and transformers are installed: `pip list | grep -E "torch|transformers"`
   
2. **Slow command processing**: 
   - First command is slower (model loading)
   - Subsequent commands should be fast (<100ms)
   - Consider CPU vs GPU performance

3. **Intent recognition errors**:
   - Check `backend/test_nlp_accuracy.py` for test results
   - Review failed cases in test results
   - BERT model can be retrained with more examples

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Documentation

For more detailed information, see:

- **[NLP_PROJECT_REPORT.md](NLP_PROJECT_REPORT.md)** - Comprehensive NLP analysis with technical implementation details
- **[TUTORIAL_GUIDE.md](TUTORIAL_GUIDE.md)** - Complete tutorial world walkthrough
- **[QIN_DYNASTY_GUIDE.md](QIN_DYNASTY_GUIDE.md)** - Advanced Qin dynasty scenario guide
- **[QIN_QUICKSTART.md](QIN_QUICKSTART.md)** - Quick reference for Qin scenario
- **[GAME_DATA_REFERENCE.md](GAME_DATA_REFERENCE.md)** - Game data structure documentation
- **[DIFFICULTY_SYSTEM_REPORT.md](DIFFICULTY_SYSTEM_REPORT.md)** - Difficulty rating system details
- **[MOBILE_UX_IMPROVEMENTS.md](MOBILE_UX_IMPROVEMENTS.md)** - Mobile optimization notes

## License

MIT

## Credits

- Original game concept from FABLE HTML prototype
- Enhanced with advanced NLP techniques for COMP5423 course project
- BERT models: Hugging Face Transformers (bert-base-multilingual-cased)
- Developed by Fai, 2026
- Special thanks to the open-source NLP community
