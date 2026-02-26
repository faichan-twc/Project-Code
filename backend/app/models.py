# Game Models
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
import uuid

class QuestState(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Item(BaseModel):
    name: str
    qty: int = 1
    stack: bool = True
    desc: str = ""
    heal: Optional[int] = None
    display_name: Optional[str] = None

class Buff(BaseModel):
    critUp: int = 0
    evasion: float = 0.0
    enrage: bool = False
    # Debuffs
    poison: int = 0      # Deals damage over time
    slow: int = 0        # Reduces attack damage
    bleed: int = 0       # Deals damage over time
    confusion: int = 0   # Reduces accuracy
    stun: int = 0        # Prevents action

class PlayerState(BaseModel):
    hp: int = 100
    maxhp: int = 100
    defending: bool = False
    buffs: Buff = Field(default_factory=Buff)
    inventory: List[Item] = Field(default_factory=list)
    weapon_debuff: Optional[Dict[str, int]] = None  # Debuff to apply on next attack
    weapon_debuff_duration: int = 0  # Duration of weapon buff

class Enemy(BaseModel):
    id: str
    name: str
    hp: int
    maxhp: int
    baseAtk: int = 10  # Enemy's attack power
    buffs: Buff = Field(default_factory=Buff)
    cd: Dict[str, int] = Field(default_factory=dict)
    hint: str = ""
    display_name: Optional[str] = None

class Objective(BaseModel):
    type: str
    desc: str
    done: bool = False
    location: Optional[str] = None
    enemy: Optional[str] = None
    item: Optional[str] = None
    qty: Optional[int] = None
    count: Optional[int] = 0
    target: Optional[str] = None
    context: Optional[str] = None

class Quest(BaseModel):
    id: str
    title: str
    desc: str
    state: QuestState = QuestState.NOT_STARTED
    objectives: List[Objective] = Field(default_factory=list)
    rewards: List[Dict[str, Any]] = Field(default_factory=list)

class GameState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scenario: Optional[str] = None
    location_id: str = "grove"
    location: str = "—"
    player: PlayerState = Field(default_factory=PlayerState)
    enemy: Optional[Enemy] = None
    quests: Dict[str, Quest] = Field(default_factory=dict)
    tracked_quest: Optional[str] = None
    visited: List[str] = Field(default_factory=list)
    stats: Dict[str, Any] = Field(default_factory=dict)
    story: List[Dict[str, str]] = Field(default_factory=list)
    # 新增：情境記憶
    conversation_context: List[str] = Field(default_factory=list)  # 最近5句對話
    last_mentioned_entity: Optional[Dict[str, str]] = None  # {"type": "enemy", "name": "影牙狼"}
    environment_state: Dict[str, Any] = Field(default_factory=dict)  # 環境狀態（如發現的線索）
    location_states: Dict[str, Dict[str, Any]] = Field(default_factory=dict)  # 場景狀態（如已拾取物品）
    game_over: bool = False  # 遊戲結束（死亡）
    victory: bool = False    # 遊戲勝利（完成所有任務）
    exits: List[Dict[str, str]] = Field(default_factory=list)  # 當前地點的出口

class AttackStyle(str, Enum):
    PRECISE = "precise"  # 精準攻擊
    HEAVY = "heavy"      # 重擊
    QUICK = "quick"      # 快速攻擊
    DEFENSIVE = "defensive"  # 防守反擊
    NORMAL = "normal"    # 普通攻擊

class Sentiment(str, Enum):
    FRIENDLY = "friendly"
    HOSTILE = "hostile"
    INTIMIDATING = "intimidating"
    NEUTRAL = "neutral"

class CommandIntent(BaseModel):
    intent: str
    target: Optional[str] = None
    item: Optional[str] = None
    location: Optional[str] = None
    object: Optional[str] = None
    raw: Optional[str] = None
    # 新增：進階解析欄位
    weapon: Optional[str] = None  # 使用的武器
    body_part: Optional[str] = None  # 目標部位
    attack_style: Optional[AttackStyle] = None  # 攻擊方式
    sentiment: Optional[Sentiment] = None  # 情感
    question_type: Optional[str] = None  # 問題類型（環境互動）
    modifiers: List[str] = Field(default_factory=list)  # 修飾詞（如"快速"、"用力"）

class GameAction(BaseModel):
    command: str
    session_id: Optional[str] = None

class GameResponse(BaseModel):
    state: GameState
    message: str
    message_type: str = "sys"  # sys, player, enemy
