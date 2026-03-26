/**
 * Synthesized split-flap click-clack audio engine.
 * Uses Web Audio API to generate realistic mechanical flip sounds
 * with randomized micro-variations for organic feel.
 */

let audioContext: AudioContext | null = null;
let masterGain: GainNode | null = null;
let muted = false;

function getContext(): AudioContext {
  if (!audioContext) {
    audioContext = new AudioContext();
    masterGain = audioContext.createGain();
    masterGain.gain.value = 0.3;
    masterGain.connect(audioContext.destination);
  }
  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }
  return audioContext;
}

function getMasterGain(): GainNode {
  getContext();
  return masterGain!;
}

/**
 * Generate a single mechanical click sound.
 * Combines a short noise burst with a resonant knock for realism.
 */
export function playFlipSound(): void {
  if (muted) return;

  const ctx = getContext();
  const gain = getMasterGain();
  const now = ctx.currentTime;

  // Randomize timing and pitch for organic feel
  const offset = Math.random() * 0.005;
  const pitchVariation = 0.9 + Math.random() * 0.2;

  // — Click component: short burst of filtered noise —
  const clickDuration = 0.008 + Math.random() * 0.006;
  const noiseBuffer = ctx.createBuffer(1, Math.ceil(ctx.sampleRate * clickDuration), ctx.sampleRate);
  const noiseData = noiseBuffer.getChannelData(0);
  for (let i = 0; i < noiseData.length; i++) {
    noiseData[i] = (Math.random() * 2 - 1) * Math.exp(-i / (noiseData.length * 0.3));
  }

  const noiseSource = ctx.createBufferSource();
  noiseSource.buffer = noiseBuffer;

  const clickFilter = ctx.createBiquadFilter();
  clickFilter.type = 'bandpass';
  clickFilter.frequency.value = 3000 * pitchVariation;
  clickFilter.Q.value = 1.5;

  const clickGain = ctx.createGain();
  clickGain.gain.setValueAtTime(0.6, now + offset);
  clickGain.gain.exponentialRampToValueAtTime(0.001, now + offset + clickDuration);

  noiseSource.connect(clickFilter);
  clickFilter.connect(clickGain);
  clickGain.connect(gain);
  noiseSource.start(now + offset);
  noiseSource.stop(now + offset + clickDuration + 0.01);

  // — Knock component: resonant low-frequency thump —
  const knockOsc = ctx.createOscillator();
  knockOsc.type = 'sine';
  knockOsc.frequency.value = 180 * pitchVariation;

  const knockGain = ctx.createGain();
  const knockDuration = 0.015 + Math.random() * 0.01;
  knockGain.gain.setValueAtTime(0.25, now + offset);
  knockGain.gain.exponentialRampToValueAtTime(0.001, now + offset + knockDuration);

  knockOsc.connect(knockGain);
  knockGain.connect(gain);
  knockOsc.start(now + offset);
  knockOsc.stop(now + offset + knockDuration + 0.01);

  // — Clack component: higher pitched secondary impact —
  const clackDelay = 0.002 + Math.random() * 0.004;
  const clackOsc = ctx.createOscillator();
  clackOsc.type = 'square';
  clackOsc.frequency.value = 4500 * pitchVariation;

  const clackGain = ctx.createGain();
  const clackDuration = 0.004;
  clackGain.gain.setValueAtTime(0.08, now + offset + clackDelay);
  clackGain.gain.exponentialRampToValueAtTime(0.001, now + offset + clackDelay + clackDuration);

  clackOsc.connect(clackGain);
  clackGain.connect(gain);
  clackOsc.start(now + offset + clackDelay);
  clackOsc.stop(now + offset + clackDelay + clackDuration + 0.01);
}

export function setVolume(volume: number): void {
  const g = getMasterGain();
  g.gain.value = Math.max(0, Math.min(1, volume));
}

export function toggleMute(): boolean {
  muted = !muted;
  return muted;
}

export function isMuted(): boolean {
  return muted;
}
