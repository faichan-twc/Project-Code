import React, { useState, useRef, useEffect } from 'react';
import { useGame } from '../context/GameContext';
import './GameScreen.css';

export const GameScreen: React.FC = () => {
  const { gameState, currentScenario, executeCommand } = useGame();
  const [command, setCommand] = useState('');
  const [showOpening, setShowOpening] = useState(true);
  const [displayedText, setDisplayedText] = useState('');
  const [openingComplete, setOpeningComplete] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(window.innerWidth <= 768); // 手机默认折叠
  const storyRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const openingText = currentScenario?.opening || '';

  // 监听窗口大小变化
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setSidebarCollapsed(true);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // 打字机效果
  useEffect(() => {
    if (!showOpening || !openingText) return;
    
    let index = 0;
    setDisplayedText('');
    setOpeningComplete(false);
    
    timerRef.current = setInterval(() => {
      if (index < openingText.length) {
        setDisplayedText(openingText.slice(0, index + 1));
        index++;
      } else {
        setOpeningComplete(true);
        if (timerRef.current) {
          clearInterval(timerRef.current);
          timerRef.current = null;
        }
      }
    }, 50); // 每50ms显示一个字符
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [showOpening, openingText]);

  // 跳过开场白
  const skipOpening = () => {
    // 清除定时器
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    // 立即显示全部文本
    setDisplayedText(openingText);
    setOpeningComplete(true);
  };

  // 关闭开场白
  const closeOpening = () => {
    setShowOpening(false);
  };

  useEffect(() => {
    if (storyRef.current) {
      storyRef.current.scrollTop = storyRef.current.scrollHeight;
    }
  }, [gameState?.story]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim()) {
      executeCommand(command.trim());
      setCommand('');
    }
  };

  const quickAction = (action: string) => {
    setCommand(action);
    executeCommand(action);
    setCommand('');
  };

  if (!gameState || !gameState.scenario) {
    return null;
  }

  const player = gameState.player;
  const enemy = gameState.enemy;
  const hpPercent = (player.hp / player.maxhp) * 100;
  const enemyHpPercent = enemy ? (enemy.hp / enemy.maxhp) * 100 : 0;

  // Check for game over or victory
  const isGameEnded = gameState.game_over || gameState.victory;

  return (
    <div className="game-screen">
      {/* Sidebar Toggle Button (Mobile) */}
      <button 
        className={`sidebar-toggle ${sidebarCollapsed ? 'collapsed' : ''}`}
        onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
        aria-label="切換側邊欄"
      >
        {sidebarCollapsed ? '📊' : '✖️'}
      </button>

      {/* Opening Story Overlay */}
      {showOpening && openingText && (
        <div className="opening-overlay">
          <div className="opening-modal">
            <div className="opening-title">{currentScenario?.name}</div>
            <div className="opening-text">
              {displayedText}
              {!openingComplete && <span className="typing-cursor">|</span>}
            </div>
            <div className="opening-actions">
              {!openingComplete && (
                <button className="btn ghost" onClick={skipOpening}>
                  跳過 ⏩
                </button>
              )}
              {openingComplete && (
                <button className="btn" onClick={closeOpening}>
                  開始冒險 ⚔️
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Game Over / Victory Overlay */}
      {isGameEnded && (
        <div className="game-over-overlay">
          <div className="game-over-modal">
            <img 
              src={gameState.victory ? '/images/victory.png' : '/images/gameover.png'} 
              alt={gameState.victory ? 'Victory' : 'Game Over'}
              className="game-end-image"
            />
            <p>
              {gameState.victory 
                ? '恭喜你完成了所有任務！你成為了傳說中的英雄！' 
                : '你的冒險到此為止...'}
            </p>
            <button 
              className="btn" 
              onClick={() => window.location.reload()}
            >
              返回選單
            </button>
          </div>
        </div>
      )}

      <div className="game-left">
        {/* Story Area */}
        <div className="panel story-area" ref={storyRef}>
          {gameState.story.map((msg, idx) => (
            <div key={idx} className={`story-block ${msg.type}`}>
              {msg.type === 'player' && '你：'}
              {msg.type === 'enemy' && '敵人：'}
              {msg.text}
            </div>
          ))}
        </div>

        {/* Location Bar */}
        <div className="panel location-bar">
          <div className="location-row">
            <div>
              <strong>當前地點：</strong>
              <span>{gameState.location}</span>
            </div>
            {gameState.exits && gameState.exits.length > 0 && (
              <div className="exits-info">
                <strong>出口：</strong>
                <span>{gameState.exits.map(exit => `${exit.cn_name}(${exit.en_name})`).join('、')}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="game-right" data-collapsed={sidebarCollapsed}>
        {/* Overlay for mobile when sidebar is open */}
        {!sidebarCollapsed && (
          <div 
            className="sidebar-overlay"
            onClick={() => setSidebarCollapsed(true)}
          />
        )}

        {/* Player Stats */}
        <div className="panel stats-panel">
          <h3>玩家狀態</h3>
          <div className="stat-row">
            <span>生命值</span>
            <span>{player.hp} / {player.maxhp}</span>
          </div>
          <div className="bar">
            <div className="fill hp-fill" style={{ width: `${hpPercent}%` }}></div>
          </div>
          
          {/* Buffs */}
          <div className="chips">
            {player.defending && <span className="chip">防禦姿態</span>}
            {player.buffs.critUp > 0 && <span className="chip">會心+{player.buffs.critUp}</span>}
            {player.buffs.evasion > 0 && <span className="chip">閃避+{Math.round(player.buffs.evasion * 100)}%</span>}
            {(player.buffs.stun || 0) > 0 && <span className="chip debuff">💫暈眩 {player.buffs.stun}回合</span>}
            {(player.buffs.poison || 0) > 0 && <span className="chip debuff">🧪中毒 {player.buffs.poison}回合</span>}
            {(player.buffs.bleed || 0) > 0 && <span className="chip debuff">🩸流血 {player.buffs.bleed}回合</span>}
            {(player.buffs.slow || 0) > 0 && <span className="chip debuff">🐌減速 {player.buffs.slow}回合</span>}
            {(player.buffs.confusion || 0) > 0 && <span className="chip debuff">😵混亂 {player.buffs.confusion}回合</span>}
          </div>

          <hr />
          <h4>背包</h4>
          <div className="inventory">
            {player.inventory.map((item, idx) => (
              <div key={idx}>• {item.display_name || item.name} × {item.qty}</div>
            ))}
          </div>
        </div>

        {/* Enemy Stats */}
        <div className="panel stats-panel">
          <h3>
            敵人 <span className="hint-text">{enemy ? (enemy.display_name || enemy.name) : '（無）'}</span>
          </h3>
          {enemy ? (
            <>
              <div className="stat-row">
                <span>敵人生命</span>
                <span>{enemy.hp} / {enemy.maxhp}</span>
              </div>
              <div className="bar">
                <div className="fill enemy-fill" style={{ width: `${enemyHpPercent}%` }}></div>
              </div>
              <div className="chips">
                {(enemy.buffs.stun || 0) > 0 && <span className="chip">💫暈眩 {enemy.buffs.stun}回合</span>}
                {enemy.buffs.evasion > 0 && <span className="chip">閃避+{Math.round(enemy.buffs.evasion * 100)}%</span>}
                {enemy.buffs.enrage && <span className="chip">狂暴</span>}
                {enemy.buffs.critUp > 0 && <span className="chip">會心+{enemy.buffs.critUp}</span>}
              </div>
              {enemy.hint && <div className="hint-text">{enemy.hint}</div>}
            </>
          ) : (
            <div className="hint-text">當前沒有敵人</div>
          )}
        </div>

        {/* Quests */}
        <div className="panel stats-panel">
          <h3>任務</h3>
          <div className="quest-list">
            {Object.values(gameState.quests).filter(q => q.state === 'ACTIVE').length > 0 ? (
              Object.values(gameState.quests)
                .filter(q => q.state === 'ACTIVE')
                .map(quest => (
                  <div key={quest.id} className="quest-item">
                    <strong>{quest.title}</strong>
                    <div className="hint-text">{quest.desc}</div>
                    <ul>
                      {quest.objectives.map((obj, idx) => (
                        <li key={idx} className="hint-text">
                          {obj.done ? '✅' : '⬜'} {obj.desc}
                          {obj.qty && ` (${obj.count || 0}/${obj.qty})`}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))
            ) : (
              <div className="hint-text">（尚未有任務）</div>
            )}
          </div>
        </div>
      </div>

      {/* Input Bar */}
      <div className="input-bar">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            placeholder="中英文皆可，如：attack wolf / use potion / look around / go to temple"
            className="command-input"
          />
          <button type="submit" className="btn">送出</button>
        </form>
        <div className="quick-actions">
          <button className="btn ghost" onClick={() => quickAction('look around')}>👁️</button>
          <button className="btn ghost" onClick={() => quickAction('defend')}>🛡️</button>
          <button className="btn ghost" onClick={() => quickAction('rest')}>💤</button>
        </div>
      </div>
    </div>
  );
};
