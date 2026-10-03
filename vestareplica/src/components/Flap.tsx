import { useEffect, useRef, useState } from 'react';
import { FLAP_CHARACTERS, isColorBlock, getBlockColor } from '../utils/characters';
import { playFlipSound } from '../audio/FlipAudio';

interface FlapProps {
  targetIndex: number;
  row: number;
  col: number;
  /** Cascade delay in ms based on position */
  cascadeDelay: number;
}

/** Duration of a single flap flip in ms */
const FLIP_DURATION = 140;
/** Stagger between intermediate flaps in ms */
const INTER_FLAP_STAGGER = 12;

/**
 * A single Bit (character position) on the split-flap display.
 * Animates through intermediate flaps to reach the target character.
 */
export default function Flap({ targetIndex, row, col, cascadeDelay }: FlapProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipping, setIsFlipping] = useState(false);
  const [displayTop, setDisplayTop] = useState(' ');
  const [displayBottom, setDisplayBottom] = useState(' ');
  const [flipPhase, setFlipPhase] = useState<'idle' | 'flip-down' | 'flip-up'>('idle');
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const activeRef = useRef(false);
  const currentIndexRef = useRef(0);

  useEffect(() => {
    // Clear any pending animation
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    activeRef.current = false;

    if (targetIndex === currentIndexRef.current) return;

    // Start flipping after cascade delay
    timeoutRef.current = setTimeout(() => {
      animateToTarget(targetIndex);
    }, cascadeDelay);

    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      activeRef.current = false;
    };
  }, [targetIndex, cascadeDelay]);

  function animateToTarget(target: number) {
    setIsFlipping(true);
    activeRef.current = true;
    let current = currentIndexRef.current;

    function flipNext() {
      if (!activeRef.current || current === target) {
        setIsFlipping(false);
        setFlipPhase('idle');
        return;
      }

      // Move forward through the flap sequence (wrapping around 64)
      current = (current + 1) % 64;
      const nextChar = FLAP_CHARACTERS[current];
      const prevChar = FLAP_CHARACTERS[currentIndexRef.current];

      // Phase 1: top flap falls down, showing previous on falling flap, next on revealed bottom
      setDisplayTop(prevChar);
      setDisplayBottom(nextChar);
      setFlipPhase('flip-down');
      playFlipSound();

      setTimeout(() => {
        // Phase 2: complete the flip
        setFlipPhase('idle');
        setDisplayTop(nextChar);
        setDisplayBottom(nextChar);
        currentIndexRef.current = current;
        setCurrentIndex(current);

        // Continue to next flap
        setTimeout(flipNext, INTER_FLAP_STAGGER);
      }, FLIP_DURATION);
    }

    flipNext();
  }

  const colorBlock = isColorBlock(currentIndex);
  const blockColor = colorBlock ? getBlockColor(currentIndex) : null;
  const displayChar = FLAP_CHARACTERS[currentIndex];

  return (
    <div
      className="flap-bit"
      style={{
        position: 'relative',
        width: '100%',
        height: '100%',
        perspective: '300px',
        transformStyle: 'preserve-3d',
      }}
    >
      {/* Static background (bottom half) */}
      <div
        className="flap-static"
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          borderRadius: '3px',
          overflow: 'hidden',
          background: blockColor || '#1a1a1a',
        }}
      >
        {/* Top half */}
        <div style={{
          flex: 1,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          background: blockColor
            ? blockColor
            : 'linear-gradient(180deg, #2a2a2a 0%, #222 100%)',
          borderBottom: '1px solid #111',
          overflow: 'hidden',
          paddingBottom: '1px',
        }}>
          <span style={{
            color: blockColor ? (colorBlock ? 'transparent' : '#f0f0f0') : '#f0f0f0',
            fontSize: 'min(2.8vw, 2.8vh)',
            fontFamily: "'Roboto Mono', 'SF Mono', 'Courier New', monospace",
            fontWeight: 700,
            lineHeight: 1,
            transform: 'translateY(52%)',
            userSelect: 'none',
          }}>
            {colorBlock ? '' : (flipPhase !== 'idle' ? displayTop : displayChar)}
          </span>
        </div>
        {/* Bottom half */}
        <div style={{
          flex: 1,
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'center',
          background: blockColor
            ? blockColor
            : 'linear-gradient(180deg, #1e1e1e 0%, #252525 100%)',
          overflow: 'hidden',
          paddingTop: '1px',
        }}>
          <span style={{
            color: blockColor ? 'transparent' : '#e8e8e8',
            fontSize: 'min(2.8vw, 2.8vh)',
            fontFamily: "'Roboto Mono', 'SF Mono', 'Courier New', monospace",
            fontWeight: 700,
            lineHeight: 1,
            transform: 'translateY(-48%)',
            userSelect: 'none',
          }}>
            {colorBlock ? '' : (flipPhase !== 'idle' ? displayBottom : displayChar)}
          </span>
        </div>
      </div>

      {/* Animated flap (top half that flips down) */}
      {flipPhase === 'flip-down' && (
        <div
          className="flap-animated"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '50%',
            transformOrigin: 'bottom center',
            animation: `flipDown ${FLIP_DURATION}ms cubic-bezier(0.4, 0, 0.2, 1) forwards`,
            zIndex: 2,
            backfaceVisibility: 'hidden',
            borderRadius: '3px 3px 0 0',
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'flex-end',
            justifyContent: 'center',
            background: blockColor
              ? blockColor
              : 'linear-gradient(180deg, #2a2a2a 0%, #222 100%)',
            boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
          }}
        >
          <span style={{
            color: blockColor ? 'transparent' : '#f0f0f0',
            fontSize: 'min(2.8vw, 2.8vh)',
            fontFamily: "'Roboto Mono', 'SF Mono', 'Courier New', monospace",
            fontWeight: 700,
            lineHeight: 1,
            transform: 'translateY(52%)',
            userSelect: 'none',
          }}>
            {colorBlock ? '' : displayTop}
          </span>
        </div>
      )}
    </div>
  );
}
