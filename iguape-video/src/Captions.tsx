import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, SHADOW, sans} from './cutout/theme';
import {scenes} from './timing';

const chunks = (t: string, max = 100): string[] => {
	const n = Math.ceil(t.length / max);
	if (n <= 1) return [t];
	const out: string[] = [];
	let start = 0;
	for (let i = 1; i < n; i++) {
		const target = Math.round((t.length * i) / n);
		let best = -1, bestScore = 1e9;
		for (let j = start + 12; j < t.length - 8; j++) {
			if (t[j] !== ' ') continue;
			const punct = /[,:;.?!]/.test(t[j - 1]) ? -14 : 0;
			const score = Math.abs(j - target) + punct;
			if (score < bestScore) { bestScore = score; best = j; }
		}
		if (best < 0) break;
		out.push(t.slice(start, best).trim());
		start = best + 1;
	}
	out.push(t.slice(start).trim());
	return out.filter(Boolean);
};

/** Legendas de fala sincronizadas com alignment.json (máx. 2 linhas). */
export const Captions: React.FC = () => {
	const f = useCurrentFrame();
	const sc = scenes.find((s) => f >= s.start && f < s.start + s.dur);
	if (!sc) return null;
	const lf = f - sc.start;
	if (lf > sc.narrEnd + 6) return null;
	let k = sc.paras.findIndex((p, i) => lf >= p.from && (i === sc.paras.length - 1 || lf < sc.paras[i + 1].from));
	if (k < 0) k = 0;
	const p = sc.paras[k];
	const endP = k < sc.paras.length - 1 ? sc.paras[k + 1].from : Math.max(p.to, sc.narrEnd);
	const cs = chunks(p.text);
	const total = cs.reduce((a, c) => a + c.length, 0);
	let acc = 0, idx = 0;
	const prog = Math.max(0, Math.min(0.999, (lf - p.from) / Math.max(1, endP - p.from)));
	for (let i = 0; i < cs.length; i++) { acc += cs[i].length / total; if (prog < acc) { idx = i; break; } idx = i; }
	return (
		<div style={{position: 'absolute', left: 0, right: 0, bottom: 38, display: 'flex', justifyContent: 'center', pointerEvents: 'none'}}>
			<div style={{maxWidth: 1560, padding: '14px 34px 16px', background: C.parch2, border: `4px solid ${C.outline}`, filter: SHADOW, transform: 'rotate(-0.3deg)', fontFamily: sans, fontWeight: 800, fontSize: 40, lineHeight: 1.22, color: C.ink, textAlign: 'center', clipPath: 'polygon(0 4%, 3% 0, 97% 3%, 100% 0, 100% 96%, 96% 100%, 4% 97%, 0 100%)'}}>
				{cs[idx]}
			</div>
		</div>
	);
};
