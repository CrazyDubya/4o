import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

// Inject global keyframe animations for flap mechanics
const style = document.createElement('style');
style.textContent = `
  @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

  @keyframes flipDown {
    0% {
      transform: rotateX(0deg);
    }
    100% {
      transform: rotateX(-90deg);
    }
  }

  @keyframes flipUp {
    0% {
      transform: rotateX(90deg);
    }
    100% {
      transform: rotateX(0deg);
    }
  }

  /* Smooth scrollbar for controls */
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 3px;
  }

  /* Focus styles */
  textarea:focus, input:focus {
    border-color: #2a9d8f !important;
    box-shadow: 0 0 0 2px rgba(42, 157, 143, 0.3);
  }

  button:hover {
    filter: brightness(1.2);
  }
  button:active {
    filter: brightness(0.9);
    transform: scale(0.97);
  }
`;
document.head.appendChild(style);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
