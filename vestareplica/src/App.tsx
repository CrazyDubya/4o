import { useState, useCallback, useEffect } from 'react';
import Board from './components/Board';
import Controls from './components/Controls';
import { textToGrid, centerText, ROWS, COLS } from './utils/characters';

const WELCOME_TEXT = centerText([
  'VESTAREPLICA',
  'SPLIT FLAP DISPLAY',
  'OPEN SOURCE',
]);

export default function App() {
  const [grid, setGrid] = useState<number[][]>(() => {
    // Start blank, then flip to welcome message
    const blank: number[][] = [];
    for (let r = 0; r < ROWS; r++) {
      blank.push(new Array(COLS).fill(0));
    }
    return blank;
  });

  // Show welcome message after a short delay
  useEffect(() => {
    const timer = setTimeout(() => {
      setGrid(textToGrid(WELCOME_TEXT));
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  const handleSendMessage = useCallback((text: string) => {
    // If text has newlines, use as-is; otherwise center it
    if (text.includes('\n')) {
      setGrid(textToGrid(text));
    } else {
      setGrid(textToGrid(centerText([text])));
    }
  }, []);

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#1a1a1a',
      padding: 'min(2vw, 24px)',
      paddingBottom: '80px', // Room for controls
    }}>
      {/* Board container with Vestaboard aspect ratio */}
      <div style={{
        width: '100%',
        maxWidth: '1400px',
        aspectRatio: '22 / 7',
        maxHeight: 'calc(100vh - 120px)',
      }}>
        <Board grid={grid} />
      </div>

      <Controls onSendMessage={handleSendMessage} />
    </div>
  );
}
