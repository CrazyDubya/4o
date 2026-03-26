/**
 * Vestaboard character set — 64 flaps per Bit.
 * Indices 0–63 map to physical flap positions.
 * Color blocks use special Unicode display but are stored as codes.
 */

// The canonical Vestaboard flap order (64 characters)
// Blank, A-Z, 0-9, punctuation/symbols, color blocks
export const FLAP_CHARACTERS: string[] = [
  ' ',                                          // 0: blank
  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',     // 1-8
  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',     // 9-16
  'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',     // 17-24
  'Y', 'Z',                                     // 25-26
  '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', // 27-36
  '!', '@', '#', '$', '(', ')', '-', '+', '&',  // 37-45
  '=', ';', ':', "'", '"', '%', ',', '.', '/',  // 46-54
  '?', '°',                                     // 55-56
  // Color blocks (57-63) — rendered as solid colored squares
  '🟥', // 57: red
  '🟧', // 58: orange
  '🟨', // 59: yellow
  '🟩', // 60: green
  '🟦', // 61: blue
  '🟪', // 62: violet
  '⬜', // 63: white
];

// Map from display character to flap index
const charToIndexMap = new Map<string, number>();
FLAP_CHARACTERS.forEach((ch, i) => charToIndexMap.set(ch, i));

// Also map lowercase letters to their uppercase index
for (let i = 1; i <= 26; i++) {
  charToIndexMap.set(FLAP_CHARACTERS[i].toLowerCase(), i);
}

export const TOTAL_FLAPS = FLAP_CHARACTERS.length; // 64

export const ROWS = 6;
export const COLS = 22;
export const TOTAL_BITS = ROWS * COLS; // 132

/** Get flap index for a character. Returns 0 (blank) for unknown chars. */
export function charToFlapIndex(ch: string): number {
  return charToIndexMap.get(ch) ?? 0;
}

/** Check if a flap index is a color block */
export function isColorBlock(index: number): boolean {
  return index >= 57 && index <= 63;
}

/** Get CSS color for color block flap indices */
export function getBlockColor(index: number): string | null {
  const colors: Record<number, string> = {
    57: '#e63946', // red
    58: '#f4a261', // orange
    59: '#e9c46a', // yellow
    60: '#2a9d8f', // green
    61: '#457b9d', // blue
    62: '#7b2d8e', // violet
    63: '#f1faee', // white
  };
  return colors[index] ?? null;
}

/** Convert a text string into a 6×22 grid of flap indices */
export function textToGrid(text: string): number[][] {
  const lines = text.split('\n').slice(0, ROWS);
  const grid: number[][] = [];
  for (let r = 0; r < ROWS; r++) {
    const row: number[] = [];
    const line = lines[r] || '';
    for (let c = 0; c < COLS; c++) {
      row.push(charToFlapIndex(line[c] ?? ' '));
    }
    grid.push(row);
  }
  return grid;
}

/** Center a single line of text within 22 columns */
export function centerLine(text: string): string {
  const trimmed = text.slice(0, COLS);
  const pad = Math.floor((COLS - trimmed.length) / 2);
  return ' '.repeat(pad) + trimmed + ' '.repeat(COLS - pad - trimmed.length);
}

/** Center multiple lines of text in the 6×22 grid */
export function centerText(lines: string[]): string {
  const trimmed = lines.slice(0, ROWS);
  const topPad = Math.floor((ROWS - trimmed.length) / 2);
  const result: string[] = [];
  for (let r = 0; r < ROWS; r++) {
    const lineIdx = r - topPad;
    if (lineIdx >= 0 && lineIdx < trimmed.length) {
      result.push(centerLine(trimmed[lineIdx]));
    } else {
      result.push(' '.repeat(COLS));
    }
  }
  return result.join('\n');
}
