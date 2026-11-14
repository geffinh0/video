// Linha do tempo do curta (segundos). 30 fps, 1920x1080.
export const FPS = 30;
export const W = 1920;
export const H = 1080;
export const f = (s: number) => Math.round(s * FPS);

// Cada cena: início e duração em segundos (no filme). Os tempos internos das cenas são relativos ao início.
export const SCENES = {
	archive: {from: 0, dur: 27},      // S01 Arquivo recuperado (CCTV)
	first: {from: 27, dur: 29},       // S02 Primeira anomalia (celular)
	observe: {from: 56, dur: 24},     // S03 Observação (CCTV)
	smile: {from: 80, dur: 22},       // S04 O sorriso (celular, perto do espelho)
	final: {from: 102, dur: 36},      // S05 A gravação final (celular, muito degradado)
	last: {from: 138, dur: 24},       // S06 Último registro (CCTV) + texto final
};
export const TOTAL = f(162);
