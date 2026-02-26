import { GameProvider, useGame } from './context/GameContext';
import { ScenarioPicker } from './components/ScenarioPicker';
import { GameScreen } from './components/GameScreen';
import './App.css';

function GameContent() {
  const { gameState } = useGame();

  return (
    <div className="app">
      <header className="app-header">
        FABLE — 中文 NLP 文字冒險
      </header>
      
      <main className="app-main">
        {!gameState?.scenario ? <ScenarioPicker /> : <GameScreen />}
      </main>
    </div>
  );
}

function App() {
  return (
    <GameProvider>
      <GameContent />
    </GameProvider>
  );
}

export default App;
