import { useMemo } from 'react';
import Flap from './Flap';
import { ROWS, COLS } from '../utils/characters';

interface BoardProps {
  grid: number[][];
}

/**
 * The 6×22 split-flap display board.
 * Each cell is an independent Flap (Bit) component.
 */
export default function Board({ grid }: BoardProps) {
  // Calculate cascade delays: left-to-right with slight row offset
  const delays = useMemo(() => {
    const d: number[][] = [];
    for (let r = 0; r < ROWS; r++) {
      const row: number[] = [];
      for (let c = 0; c < COLS; c++) {
        // Column-major cascade with row stagger
        row.push(c * 30 + r * 15 + Math.random() * 20);
      }
      d.push(row);
    }
    return d;
  }, []);

  return (
    <div
      className="board"
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${COLS}, 1fr)`,
        gridTemplateRows: `repeat(${ROWS}, 1fr)`,
        gap: 'min(0.4vw, 4px)',
        width: '100%',
        height: '100%',
        padding: 'min(1.5vw, 16px)',
        background: '#111',
        borderRadius: '8px',
        boxShadow: 'inset 0 0 30px rgba(0,0,0,0.5), 0 4px 20px rgba(0,0,0,0.8)',
      }}
    >
      {grid.map((row, r) =>
        row.map((flapIndex, c) => (
          <Flap
            key={`${r}-${c}`}
            targetIndex={flapIndex}
            row={r}
            col={c}
            cascadeDelay={delays[r][c]}
          />
        ))
      )}
    </div>
  );
}
