import React from 'react';
import {random} from 'remotion';
import {clamp} from './fx';

// Letras de "dedo no vidro embaçado": traços simples desenhados à mão (caixa alta), com tremor próprio.
// Cada letra é uma lista de traços; cada traço é uma lista de pontos numa grade 0..1 (x) por 0..1.4 (y).
const G: Record<string, number[][][]> = {
	A: [[[0, 1.4], [0.5, 0], [1, 1.4]], [[0.2, 0.85], [0.8, 0.85]]],
	G: [[[0.95, 0.25], [0.6, 0], [0.2, 0.1], [0, 0.7], [0.2, 1.3], [0.6, 1.4], [0.95, 1.15], [0.95, 0.8], [0.55, 0.8]]],
	O: [[[0.5, 0], [0.08, 0.25], [0, 0.7], [0.1, 1.2], [0.5, 1.4], [0.9, 1.2], [1, 0.7], [0.9, 0.2], [0.5, 0]]],
	R: [[[0, 1.4], [0, 0], [0.7, 0.05], [0.9, 0.35], [0.7, 0.7], [0, 0.72]], [[0.45, 0.72], [0.95, 1.4]]],
	E: [[[0.95, 0], [0, 0], [0, 1.4], [0.95, 1.4]], [[0, 0.7], [0.75, 0.7]]],
	'É': [[[0.95, 0.15], [0, 0.15], [0, 1.4], [0.95, 1.4]], [[0, 0.78], [0.75, 0.78]], [[0.35, -0.15], [0.65, -0.4]]],
	M: [[[0, 1.4], [0.05, 0], [0.5, 0.8], [0.95, 0], [1, 1.4]]],
	I: [[[0.5, 0], [0.5, 1.4]]],
	N: [[[0, 1.4], [0, 0], [1, 1.4], [1, 0]]],
	H: [[[0, 0], [0, 1.4]], [[1, 0], [1, 1.4]], [[0, 0.7], [1, 0.7]]],
	V: [[[0, 0], [0.5, 1.4], [1, 0]]],
	Z: [[[0, 0], [1, 0], [0, 1.4], [1, 1.4]]],
	' ': [],
};

type Stroke = {d: string; len: number};
const build = (text: string, x0: number, y0: number, size: number, gap: number, seed: string) => {
	const strokes: Stroke[] = []; let x = x0;
	for (const [ci, ch] of [...text].entries()) {
		const g = G[ch] ?? []; const w = ch === 'I' ? 0.35 : ch === ' ' ? 0.6 : 0.95;
		for (const [si, s] of g.entries()) {
			const pts = s.map(([px, py], k) => [x + (ch === 'I' ? px * 0.35 : px * w) * size + (random(`${seed}${ci}${si}${k}x`) - 0.5) * size * 0.08, y0 + py * size + (random(`${seed}${ci}${si}${k}y`) - 0.5) * size * 0.08 + Math.sin(ci * 1.3) * size * 0.06]);
			let len = 0; for (let k = 1; k < pts.length; k++) len += Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]);
			strokes.push({d: 'M' + pts.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L'), len});
		}
		x += w * size + gap;
	}
	return strokes;
};

// progress 0..1 = quanto do texto já foi escrito (traços revelados em ordem, cada um na sua duração).
// O traço "limpa" o embaçado: desenhamos em preto numa máscara que recorta a camada de vapor.
export const useFogStrokes = (lines: {text: string; x: number; y: number; size: number}[], seed = 'fw') => {
	const all: Stroke[] = [];
	lines.forEach((l, i) => all.push(...build(l.text, l.x, l.y, l.size, l.size * 0.28, `${seed}${i}`)));
	const total = all.reduce((a, s) => a + s.len + 60, 0);
	return {strokes: all, total};
};

export const StrokeMask: React.FC<{strokes: Stroke[]; total: number; progress: number; width: number; color: string; blur?: number}> = ({strokes, total, progress, width, color, blur = 3}) => {
	let acc = 0; const P = progress * total;
	return (
		<g style={{filter: `blur(${blur}px)`}}>
			{strokes.map((s, i) => {
				const start = acc; acc += s.len + 60;
				const shown = clamp((P - start) / s.len) * s.len;
				if (shown <= 0) return null;
				return <path key={i} d={s.d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={`${shown} ${s.len + 10}`} />;
			})}
		</g>
	);
};
