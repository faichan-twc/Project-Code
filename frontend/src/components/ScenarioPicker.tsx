import React, { useEffect } from 'react';
import { useGame } from '../context/GameContext';
import './ScenarioPicker.css';

// 难度星级渲染函数
const renderDifficultyStars = (difficulty: number) => {
  const stars = '⭐'.repeat(difficulty);
  const difficultyNames: { [key: number]: string } = {
    1: '新手',
    2: '簡單',
    3: '中等',
    4: '困難',
    5: '專家'
  };
  const name = difficultyNames[difficulty] || '未知';
  return `${stars} ${name}`;
};

export const ScenarioPicker: React.FC = () => {
  const { scenarios, loading, startGame, loadScenarios } = useGame();

  useEffect(() => {
    loadScenarios();
  }, [loadScenarios]);

  if (loading) {
    return (
      <div className="scenario-screen">
        <div className="panel loading">載入中...</div>
      </div>
    );
  }

  return (
    <div className="scenario-screen">
      <div className="panel scenario-panel">
        <h2>選擇你的冒險</h2>
        <p className="hint">
          建議指令：<strong>攻擊狼、觀察四周、拾取寶石、使用治療藥水、前往神殿、休息、與神秘人說話</strong>
        </p>
        <div className="scenario-grid">
          {scenarios.map((scenario) => (
            <div
              key={scenario.id}
              className="scenario-card panel"
              onClick={() => startGame(scenario.id)}
            >
              {scenario.cover_image && (
                <div className="scenario-cover">
                  <img 
                    src={`/images/story/${scenario.cover_image}`} 
                    alt={scenario.name}
                    onError={(e) => {
                      // 如果图片加载失败，隐藏图片容器
                      e.currentTarget.parentElement!.style.display = 'none';
                    }}
                  />
                </div>
              )}
              <div className="scenario-content">
                <h3>{scenario.name}</h3>
                {scenario.difficulty && (
                  <div className="difficulty-badge">
                    {renderDifficultyStars(scenario.difficulty)}
                  </div>
                )}
                <div className="tag">{scenario.locations.join('、')}</div>
                <p className="small">{scenario.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
