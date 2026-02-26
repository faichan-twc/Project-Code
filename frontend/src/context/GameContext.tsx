import React, { createContext, useContext, useState, useCallback } from 'react';
import { GameState, gameAPI, Scenario } from '../services/api';

interface GameContextType {
  gameState: GameState | null;
  scenarios: Scenario[];
  currentScenario: Scenario | null;
  loading: boolean;
  error: string | null;
  startGame: (scenario: string) => Promise<void>;
  executeCommand: (command: string) => Promise<void>;
  loadScenarios: () => Promise<void>;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export const GameProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadScenarios = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await gameAPI.getScenarios();
      setScenarios(data.scenarios);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load scenarios');
    } finally {
      setLoading(false);
    }
  }, []);

  const startGame = useCallback(async (scenario: string) => {
    try {
      setLoading(true);
      setError(null);
      // 保存当前选中的 scenario 对象
      const selectedScenario = scenarios.find(s => s.id === scenario);
      if (selectedScenario) {
        setCurrentScenario(selectedScenario);
      }
      const response = await gameAPI.startGame(scenario, gameState?.session_id);
      setGameState(response.state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start game');
    } finally {
      setLoading(false);
    }
  }, [gameState?.session_id, scenarios]);

  const executeCommand = useCallback(async (command: string) => {
    if (!gameState?.session_id) {
      setError('No active game session');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // 检测是否为 AI 相关命令（如 use map），立即显示加载提示
      const isAICommand = /use.*(map|地[圖图])|使用.*(map|地[圖图])/i.test(command);
      if (isAICommand && gameState) {
        setGameState({
          ...gameState,
          story: [
            ...gameState.story,
            {
              text: "🔄 AI 正在生成內容，請稍候...",
              type: "sys"
            }
          ]
        });
      }
      
      const response = await gameAPI.executeAction(command, gameState.session_id);
      setGameState(response.state);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to execute command');
    } finally {
      setLoading(false);
    }
  }, [gameState]);

  return (
    <GameContext.Provider
      value={{
        gameState,
        scenarios,        currentScenario,        loading,
        error,
        startGame,
        executeCommand,
        loadScenarios
      }}
    >
      {children}
    </GameContext.Provider>
  );
};

export const useGame = () => {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame must be used within GameProvider');
  }
  return context;
};
