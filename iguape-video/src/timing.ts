import alignment from './data/alignment.json';

export const FPS = 30;
export const TAIL = 12 * FPS; // tela final sem narração
export type Para = {text: string; from: number; to: number};
export type SceneT = {id: number; start: number; dur: number; audio: string; narrEnd: number; paras: Para[]};

export const scenes: SceneT[] = alignment.blocks.map((b, i, arr) => {
	const start = Math.round(b.start * FPS);
	const endNarr = Math.round((b.start + b.duration) * FPS);
	const next = i < arr.length - 1 ? Math.round(arr[i + 1].start * FPS) : endNarr + TAIL;
	return {
		id: b.scene, start, dur: next - start, audio: b.file, narrEnd: endNarr - start,
		paras: b.paragraphs.map((p) => ({text: p.text, from: Math.round((p.start - b.start) * FPS), to: Math.round((p.end - b.start) * FPS)})),
	};
});
export const totalFrames = scenes[scenes.length - 1].start + scenes[scenes.length - 1].dur;
/** Frame local em que o parágrafo k começa/termina. */
export const A = (sc: SceneT, k: number) => sc.paras[Math.min(k, sc.paras.length - 1)].from;
export const E = (sc: SceneT, k: number) => sc.paras[Math.min(k, sc.paras.length - 1)].to;
