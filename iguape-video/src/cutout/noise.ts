export type P = [number, number];
export const hash = (a: number, b = 0): number => {
	let h = (Math.imul(a | 0, 374761393) + Math.imul(b | 0, 668265263)) | 0;
	h = Math.imul(h ^ (h >>> 13), 1274126177);
	return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
};
/** Borda de tesoura: subdivide as arestas e desloca os pontos com ruído determinístico (seed). */
export const rough = (pts: P[], seed: number, amp = 2.5): P[] => {
	const out: P[] = [];
	let id = 0;
	const j = (x: number, y: number): P => [
		x + (hash(seed, id++) - 0.5) * 2 * amp,
		y + (hash(seed, id++) - 0.5) * 2 * amp,
	];
	for (let i = 0; i < pts.length; i++) {
		const p = pts[i];
		const q = pts[(i + 1) % pts.length];
		out.push(j(p[0], p[1]));
		const len = Math.hypot(q[0] - p[0], q[1] - p[1]);
		const sub = Math.min(4, Math.floor(len / 55));
		for (let s = 1; s <= sub; s++) {
			const t = s / (sub + 1);
			out.push(j(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t));
		}
	}
	return out;
};
export const toPath = (pts: P[]) => 'M' + pts.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join('L') + 'Z';
export const rect = (w: number, h: number, x = 0, y = 0): P[] => [[x, y], [x + w, y], [x + w, y + h], [x, y + h]];
export const ell = (rx: number, ry: number, cx = 0, cy = 0, n = 14): P[] =>
	Array.from({length: n}, (_, i) => [cx + Math.cos((i / n) * 6.2832) * rx, cy + Math.sin((i / n) * 6.2832) * ry] as P);
export const limb = (len: number, w: number): P[] => [[-w / 2, -3], [w / 2, -3], [w * 0.4, len], [-w * 0.4, len]];
