import React from 'react';
import {AbsoluteFill, Img, random, staticFile, useCurrentFrame} from 'remotion';

/** Chuva em linhas finas (determinística). */
export const Rain: React.FC<{density?: number; opacity?: number; angle?: number; speed?: number}> = ({density = 220, opacity = 0.22, angle = 8, speed = 70}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={800} style={{position: 'absolute', inset: 0}}>
			{Array.from({length: density}, (_, i) => {
				const x0 = random(`rx${i}`) * 2100 - 90; const len = 30 + random(`rl${i}`) * 60; const sp = speed * (0.7 + random(`rs${i}`) * 0.6);
				const y = ((random(`ry${i}`) * 900 + f * sp) % 900) - 60; const dx = Math.tan((angle * Math.PI) / 180) * len;
				return <line key={i} x1={x0 + y * 0.14} y1={y} x2={x0 + y * 0.14 + dx} y2={y + len} stroke="rgb(190,205,220)" strokeWidth={random(`rw${i}`) < 0.2 ? 1.6 : 1} opacity={opacity * (0.4 + random(`ro${i}`) * 0.6)} />;
			})}
		</svg>
	);
};

/** Gotas escorrendo no vidro. */
export const GlassDrops: React.FC<{opacity?: number}> = ({opacity = 0.35}) => {
	const f = useCurrentFrame();
	return (
		<svg width={1920} height={800} style={{position: 'absolute', inset: 0}}>
			{Array.from({length: 70}, (_, i) => {
				const x = random(`gx${i}`) * 1920; const sp = 0.6 + random(`gs${i}`) * 2.5; const y = ((random(`gy${i}`) * 900 + f * sp) % 900) - 50;
				const r = 2 + random(`gr${i}`) * 5;
				return <g key={i} opacity={opacity}><ellipse cx={x} cy={y} rx={r} ry={r * 1.3} fill="rgba(200,215,230,0.25)" stroke="rgba(230,240,250,0.5)" strokeWidth={0.8} /><line x1={x} y1={y - r} x2={x} y2={y - r - sp * 18} stroke="rgba(200,215,230,0.18)" strokeWidth={r * 0.6} /></g>;
			})}
		</svg>
	);
};

/** Neblina em movimento (duas camadas de textura). */
export const Fog: React.FC<{opacity?: number}> = ({opacity = 0.35}) => {
	const f = useCurrentFrame();
	return (
		<>
			<AbsoluteFill style={{backgroundImage: `url(${staticFile('textures/fog.png')})`, backgroundSize: '1400px 1400px', backgroundPosition: `${-f * 0.9}px ${f * 0.1}px`, opacity, mixBlendMode: 'screen'}} />
			<AbsoluteFill style={{backgroundImage: `url(${staticFile('textures/fog.png')})`, backgroundSize: '900px 900px', backgroundPosition: `${f * 0.5}px ${-f * 0.15}px`, opacity: opacity * 0.6, mixBlendMode: 'screen'}} />
		</>
	);
};

/** Grão de filme + vinheta. */
export const Grain: React.FC<{amount?: number}> = ({amount = 0.1}) => {
	const f = useCurrentFrame();
	return (
		<>
			<AbsoluteFill style={{backgroundImage: `url(${staticFile('textures/grain.png')})`, backgroundSize: '512px 512px', backgroundPosition: `${random(`g${f}`) * 512}px ${random(`h${f}`) * 512}px`, opacity: amount, mixBlendMode: 'overlay'}} />
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,0,0,0.75) 100%)'}} />
		</>
	);
};

export const flicker = (f: number, amt = 0.05) => 1 + amt * (Math.sin(f * 0.9) * 0.4 + Math.sin(f * 2.3 + 1) * 0.3 + (random(`fl${Math.floor(f / 2)}`) - 0.5) * 0.6);

export const Layer: React.FC<{id: string; count: number; t: number}> = ({id, count, t}) => {
	if (!count) return null;
	const idx = Math.min(count - 1, Math.max(0, Math.floor(t * 12)));
	return <Img src={staticFile(`scenes/${id}/layer/${String(idx).padStart(4, '0')}.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%'}} />;
};
