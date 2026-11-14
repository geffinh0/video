import React from 'react';
import {AbsoluteFill, Img, random, staticFile, useCurrentFrame} from 'remotion';
import {FPS} from '../timing';

// ---------- utilidades ----------
export const noise1 = (seed: string, t: number) => {
	// ruído suave 1D (interpolação de valores aleatórios)
	const i = Math.floor(t), fr = t - i, s = fr * fr * (3 - 2 * fr);
	return random(`${seed}${i}`) * (1 - s) + random(`${seed}${i + 1}`) * s - 0.5;
};
export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const ramp = (t: number, a: number, b: number) => clamp((t - a) / (b - a));
export const smooth = (t: number, a: number, b: number) => {const x = ramp(t, a, b); return x * x * (3 - 2 * x);};

// ---------- sequência de quadros (rosto animado) ----------
// Mostra renders/frames/<dir>/NNNN.jpg na cadência `fps` do material (4 = CCTV, 15 = celular).
export const FrameSeq: React.FC<{dir: string; count: number; fps: number; start?: number; style?: React.CSSProperties; hold?: number}> = ({dir, count, fps, start = 0, style, hold}) => {
	const fr = useCurrentFrame();
	const t = Math.max(0, fr / FPS - start);
	const idx = hold !== undefined ? hold : Math.min(count - 1, Math.floor(t * fps));
	return <Img src={staticFile(`frames/${dir}/${String(idx).padStart(4, '0')}.jpg`)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', ...style}} />;
};

// ---------- grão ----------
export const Grain: React.FC<{opacity?: number; scale?: number; fps?: number; blend?: string}> = ({opacity = 0.12, scale = 1, fps = 30, blend = 'overlay'}) => {
	const fr = useCurrentFrame();
	const k = Math.floor((fr / FPS) * fps);
	const n = Math.floor(random(`g${k}`) * 8);
	const ox = Math.floor(random(`gx${k}`) * 512), oy = Math.floor(random(`gy${k}`) * 512);
	return (
		<AbsoluteFill style={{backgroundImage: `url(${staticFile(`assets/fx/noise_${n}.png`)})`, backgroundPosition: `${ox}px ${oy}px`, backgroundSize: `${512 * scale}px`, opacity, mixBlendMode: blend as any, imageRendering: scale > 1 ? 'pixelated' : 'auto'}} />
	);
};

export const Vignette: React.FC<{opacity?: number}> = ({opacity = 0.8}) => (
	<Img src={staticFile('assets/fx/vignette.png')} style={{position: 'absolute', width: '100%', height: '100%', opacity}} />
);

// ---------- VHS ----------
// Scanlines, aberração cromática, banda de tracking, ruído de troca de cabeça e jitter horizontal.
export const VHS: React.FC<{children: React.ReactNode; strength?: number; tracking?: number; seed?: string}> = ({children, strength = 1, tracking = 0, seed = 'v'}) => {
	const fr = useCurrentFrame(); const t = fr / FPS;
	const jit = (noise1(`${seed}j`, t * 12) * 3 + (random(`${seed}J${fr}`) < 0.03 * strength ? (random(`${seed}JJ${fr}`) - 0.5) * 40 : 0)) * strength;
	const ca = 3 * strength;
	const bandY = ((t * 0.21 + random(`${seed}b`)) % 1.3) * 1080 - 100;
	return (
		<AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
			<AbsoluteFill style={{transform: `translateX(${jit}px)`, filter: `saturate(${1 - 0.35 * strength}) contrast(${1 + 0.08 * strength}) blur(${0.6 * strength}px)`}}>
				<AbsoluteFill style={{mixBlendMode: 'screen', filter: 'url(#vhsR)', transform: `translateX(${ca}px)`}}>{children}</AbsoluteFill>
				<AbsoluteFill style={{mixBlendMode: 'screen', filter: 'url(#vhsG)'}}>{children}</AbsoluteFill>
				<AbsoluteFill style={{mixBlendMode: 'screen', filter: 'url(#vhsB)', transform: `translateX(${-ca}px)`}}>{children}</AbsoluteFill>
			</AbsoluteFill>
			<svg width="0" height="0" style={{position: 'absolute'}}>
				<filter id="vhsR"><feColorMatrix type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
				<filter id="vhsG"><feColorMatrix type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
				<filter id="vhsB"><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" /></filter>
			</svg>
			{/* scanlines */}
			<AbsoluteFill style={{backgroundImage: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.28) 0px, rgba(0,0,0,0.28) 1px, transparent 1px, transparent 3px)', opacity: 0.6 * strength}} />
			{/* banda de tracking */}
			{tracking > 0 && <div style={{position: 'absolute', left: 0, right: 0, top: bandY, height: 26 + 40 * tracking, background: 'linear-gradient(rgba(255,255,255,0), rgba(220,220,220,0.35), rgba(255,255,255,0))', mixBlendMode: 'screen', filter: 'blur(2px)', opacity: tracking}} />}
			{/* ruído de troca de cabeça (rodapé) */}
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 18, overflow: 'hidden', opacity: 0.8 * strength}}>
				<div style={{position: 'absolute', inset: 0, transform: `translateX(${(random(`${seed}h${fr}`) - 0.5) * 60}px)`, backgroundImage: `url(${staticFile(`assets/fx/noise_${fr % 8}.png`)})`, backgroundSize: '256px 8px', filter: 'contrast(3)'}} />
			</div>
			<Grain opacity={0.18 * strength} blend="screen" scale={2} />
		</AbsoluteFill>
	);
};

// ---------- glitch digital por fatias ----------
export const SliceGlitch: React.FC<{children: React.ReactNode; amount: number; seed?: string}> = ({children, amount, seed = 's'}) => {
	const fr = useCurrentFrame();
	if (amount <= 0.001) return <>{children}</>;
	const n = 9;
	return (
		<AbsoluteFill>
			{Array.from({length: n}).map((_, i) => {
				const y0 = (i / n) * 100, y1 = ((i + 1) / n) * 100;
				const on = random(`${seed}${fr}-${i}`) < amount;
				const dx = on ? (random(`${seed}dx${fr}-${i}`) - 0.5) * 220 * amount : 0;
				const hue = on && random(`${seed}c${fr}-${i}`) < 0.3 ? 'contrast(1.6) brightness(1.3) saturate(0.4)' : 'none';
				return <AbsoluteFill key={i} style={{clipPath: `inset(${y0}% 0 ${100 - y1}% 0)`, transform: `translateX(${dx}px)`, filter: hue}}>{children}</AbsoluteFill>;
			})}
			{random(`${seed}blk${fr}`) < amount * 0.5 && <div style={{position: 'absolute', left: `${random(`${seed}bx${fr}`) * 80}%`, top: `${random(`${seed}by${fr}`) * 80}%`, width: `${10 + random(`${seed}bw${fr}`) * 30}%`, height: `${3 + random(`${seed}bh${fr}`) * 10}%`, background: random(`${seed}bc${fr}`) < 0.5 ? '#bfbfb8' : '#1a1a1a', mixBlendMode: 'normal', opacity: 0.55}} />}
		</AbsoluteFill>
	);
};

// ---------- texto de OSD ----------
export const OSD: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<div style={{position: 'absolute', fontFamily: '"DejaVu Sans Mono", monospace', color: '#e8e8e0', fontSize: 30, letterSpacing: 2, textShadow: '2px 2px 0 rgba(0,0,0,0.85), 0 0 6px rgba(255,255,255,0.25)', whiteSpace: 'pre', ...style}}>{children}</div>
);
