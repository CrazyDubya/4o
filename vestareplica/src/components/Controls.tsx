import { useState, useCallback } from 'react';
import { COLS, ROWS } from '../utils/characters';
import { toggleMute, isMuted, setVolume } from '../audio/FlipAudio';

interface ControlsProps {
  onSendMessage: (text: string) => void;
}

const DEMO_MESSAGES = [
  'HELLO WORLD',
  'VESTAREPLICA',
  'THE QUICK BROWN FOX\nJUMPS OVER THE\nLAZY DOG',
  'GOOD MORNING',
  'OPEN SOURCE\nSPLIT FLAP\nDISPLAY',
  '12:34:56',
  'ABCDEFGHIJKLMNOPQRSTUV\n1234567890!@#$%&()',
];

export default function Controls({ onSendMessage }: ControlsProps) {
  const [text, setText] = useState('');
  const [muted, setMuted] = useState(isMuted());
  const [volume, setVolumeState] = useState(0.3);
  const [collapsed, setCollapsed] = useState(false);

  const handleSend = useCallback(() => {
    if (text.trim()) {
      onSendMessage(text.toUpperCase());
      setText('');
    }
  }, [text, onSendMessage]);

  const handleDemo = useCallback(() => {
    const msg = DEMO_MESSAGES[Math.floor(Math.random() * DEMO_MESSAGES.length)];
    onSendMessage(msg);
  }, [onSendMessage]);

  const handleClear = useCallback(() => {
    onSendMessage(' '.repeat(COLS) + ('\n' + ' '.repeat(COLS)).repeat(ROWS - 1));
  }, [onSendMessage]);

  const handleToggleMute = useCallback(() => {
    const nowMuted = toggleMute();
    setMuted(nowMuted);
  }, []);

  const handleVolumeChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const v = parseFloat(e.target.value);
    setVolumeState(v);
    setVolume(v);
  }, []);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }, [handleSend]);

  if (collapsed) {
    return (
      <button
        onClick={() => setCollapsed(false)}
        style={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          background: '#333',
          color: '#fff',
          border: '1px solid #555',
          borderRadius: '50%',
          width: 48,
          height: 48,
          cursor: 'pointer',
          fontSize: 20,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100,
        }}
        title="Show controls"
      >
        +
      </button>
    );
  }

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      background: 'rgba(20,20,20,0.95)',
      backdropFilter: 'blur(10px)',
      borderTop: '1px solid #333',
      padding: '12px 20px',
      display: 'flex',
      gap: 12,
      alignItems: 'center',
      zIndex: 100,
    }}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={`Type message (${COLS} chars per line, ${ROWS} lines max)...`}
        rows={2}
        style={{
          flex: 1,
          background: '#2a2a2a',
          color: '#fff',
          border: '1px solid #444',
          borderRadius: 6,
          padding: '8px 12px',
          fontFamily: "'Roboto Mono', monospace",
          fontSize: 14,
          resize: 'none',
          outline: 'none',
        }}
      />

      <button onClick={handleSend} style={btnStyle('#2a9d8f')}>
        Send
      </button>

      <button onClick={handleDemo} style={btnStyle('#457b9d')}>
        Demo
      </button>

      <button onClick={handleClear} style={btnStyle('#555')}>
        Clear
      </button>

      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <button onClick={handleToggleMute} style={{
          ...btnStyle('#333'),
          width: 36,
          padding: 0,
        }}>
          {muted ? 'x' : '♪'}
        </button>
        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={volume}
          onChange={handleVolumeChange}
          style={{ width: 60, accentColor: '#2a9d8f' }}
        />
      </div>

      <button
        onClick={() => setCollapsed(true)}
        style={{ ...btnStyle('#333'), width: 36, padding: 0 }}
        title="Hide controls"
      >
        _
      </button>
    </div>
  );
}

function btnStyle(bg: string): React.CSSProperties {
  return {
    background: bg,
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    padding: '8px 16px',
    fontFamily: 'system-ui, sans-serif',
    fontSize: 14,
    fontWeight: 600,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  };
}
