import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {hash} from './noise';

export const st = (f: number, n = 3) => Math.floor(f / n) * n;
/** Frame "de três em três" (~10 fps). */
export const useSF = (n = 3) => st(useCurrentFrame(), n);
export const wobbleDeg = (seed: number, f: number, amp = 0.5) => (hash(seed, Math.floor(f / 3)) - 0.5) * 2 * amp;

const bounce = (p: number) => {
	if (p >= 1) return 1;
	const e = 1 - Math.pow(1 - p, 3);
	return p < 0.7 ? e * 1.0 : 1 + Math.sin(((p - 0.7) / 0.3) * Math.PI) * 0.04;
};

type Kind = 'drop' | 'left' | 'right' | 'up' | 'pop';
/** Entrada de peça: cai sobre a mesa com quique em passos ou desliza de fora; nunca fade puro. */
export const Enter: React.FC<{at: number; until?: number; kind?: Kind; dur?: number; seed?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({
	at, until, kind = 'drop', dur = 14, seed = 1, children, style,
}) => {
	const f = useCurrentFrame();
	if (f < at || (until !== undefined && f >= until)) return null;
	const t = st(f - at, 2);
	const p = Math.min(1, t / dur);
	const e = bounce(p);
	let tx = 0, ty = 0, sc = 1, rot = 0;
	if (kind === 'drop') { ty = -1100 * (1 - e); rot = (1 - e) * 6; }
	if (kind === 'left') tx = -2300 * (1 - e);
	if (kind === 'right') tx = 2300 * (1 - e);
	if (kind === 'up') ty = 1300 * (1 - e);
	if (kind === 'pop') { sc = 0.2 + 0.8 * e; rot = (1 - e) * -8; }
	if (p >= 1) rot += wobbleDeg(seed, f, 0.35);
	return (
		<div style={{position: 'absolute', inset: 0, transform: `translate(${tx}px, ${ty}px) rotate(${rot}deg) scale(${sc})`, transformOrigin: '50% 60%', ...style}}>
			{children}
		</div>
	);
};

export type CamKey = {f: number; x?: number; y?: number; s?: number};
/** Câmera sobre a mesa de papel (suave, 30 fps). x,y: deslocamento em px; s: zoom. Shake: tremor rápido. */
export const Camera: React.FC<{keys: CamKey[]; shakeFrom?: number; shakeTo?: number; children: React.ReactNode}> = ({keys, shakeFrom = -1, shakeTo = -1, children}) => {
	const f = useCurrentFrame();
	const fr = keys.map((k) => k.f);
	const ip = (g: (k: CamKey) => number) => interpolate(f, fr, keys.map(g), {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const x = ip((k) => k.x ?? 0), y = ip((k) => k.y ?? 0), s = ip((k) => k.s ?? 1);
	let sx = 0, sy = 0;
	if (f >= shakeFrom && f < shakeTo) {
		const g = Math.floor(f / 2);
		sx = (hash(3, g) - 0.5) * 22; sy = (hash(5, g) - 0.5) * 22;
	}
	return (
		<div style={{position: 'absolute', inset: 0, transform: `translate(${-x + sx}px, ${-y + sy}px) scale(${s})`, transformOrigin: '50% 50%'}}>
			{children}
		</div>
	);
};
