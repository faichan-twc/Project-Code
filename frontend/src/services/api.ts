// API Service for game communication

export interface GameState {
  session_id: string;
  scenario: string | null;
  location_id: string;
  location: string;
  player: PlayerState;
  enemy: Enemy | null;
  quests: Record<string, Quest>;
  tracked_quest: string | null;
  visited: string[];
  stats: Record<string, any>;
  story: StoryMessage[];
  game_over: boolean;
  victory: boolean;
  exits: Array<{cn_name: string; en_name: string}>;
}

export interface PlayerState {
  hp: number;
  maxhp: number;
  defending: boolean;
  buffs: Buff;
  inventory: Item[];
}

export interface Buff {
  critUp: number;
  evasion: number;
  enrage: boolean;
  // Debuffs
  poison?: number;
  slow?: number;
  bleed?: number;
  confusion?: number;
  stun?: number;
}

export interface Item {
  name: string;
  qty: number;
  stack?: boolean;
  desc?: string;
  heal?: number;
  display_name?: string;
}

export interface Enemy {
  id: string;
  name: string;
  hp: number;
  maxhp: number;
  buffs: Buff;
  cd: Record<string, number>;
  ai: string;
  hint: string;
  display_name?: string;
}

export interface Quest {
  id: string;
  title: string;
  desc: string;
  state: 'NOT_STARTED' | 'ACTIVE' | 'COMPLETED' | 'FAILED';
  objectives: Objective[];
  rewards: any[];
}

export interface Objective {
  type: string;
  desc: string;
  done: boolean;
  location?: string;
  enemy?: string;
  item?: string;
  qty?: number;
  count?: number;
}

export interface StoryMessage {
  text: string;
  type: 'sys' | 'player' | 'enemy';
}

export interface Scenario {
  id: string;
  name: string;
  opening: string;
  description?: string;
  difficulty?: number;  // 难度等级 1-5
  cover_image?: string;
  locations: string[];
  spawn: string[];
}

export interface GameResponse {
  state: GameState;
  message: string;
  message_type: string;
}

class GameAPI {
  async getScenarios(): Promise<{ scenarios: Scenario[] }> {
    const response = await fetch('/api/scenarios');
    if (!response.ok) throw new Error('Failed to fetch scenarios');
    return response.json();
  }

  async startGame(scenario: string, sessionId?: string): Promise<GameResponse> {
    const params = new URLSearchParams();
    params.append('scenario', scenario);
    if (sessionId) params.append('session_id', sessionId);

    const response = await fetch(`/api/game/start?${params}`, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to start game');
    return response.json();
  }

  async executeAction(command: string, sessionId: string): Promise<GameResponse> {
    const response = await fetch('/api/game/action', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command, session_id: sessionId })
    });
    if (!response.ok) throw new Error('Failed to execute action');
    return response.json();
  }

  async getGameState(sessionId: string): Promise<GameState> {
    const response = await fetch(`/api/game/state/${sessionId}`);
    if (!response.ok) throw new Error('Failed to fetch game state');
    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch('/api/health');
    if (!response.ok) throw new Error('Health check failed');
    return response.json();
  }
}

export const gameAPI = new GameAPI();
