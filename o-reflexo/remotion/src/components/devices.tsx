import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {FPS} from '../timing';
import {Grain, OSD, Vignette, noise1} from './fx';

// ---------- Câmera de segurança ----------
// Fixa, ângulo alto, quadros "travados" (o material já vem a 4 fps), compressão, ruído, carimbo de data e hora.
export const SecurityCam: React.FC<{children: React.ReactNode; cam?: string; date: string; time0: number; drop?: number}> = ({children, cam = 'CAM01', date, time0, drop = 0}) => {
	const fr = useCurrentFrame(); const t = fr / FPS;
	const sec = Math.floor(time0 + t);
	const hh = String(Math.floor(sec / 3600) % 24).padStart(2, '0'), mm = String(Math.floor(sec / 60) % 60).padStart(2, '0'), ss = String(sec % 60).padStart(2, '0');
	// falha de sinal ocasional: quadro congela e fica azulado/blocado
	const fail = drop > 0 && random(`cf${Math.floor(t * 4)}`) < drop;
	return (
		<AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
			<AbsoluteFill style={{filter: `grayscale(0.55) sepia(0.15) hue-rotate(60deg) saturate(0.7) contrast(1.15) brightness(${0.92 + noise1('cb', t * 0.7) * 0.06}) blur(0.9px)`, transform: fail ? `translateY(${(random(`cy${fr}`) - 0.5) * 30}px)` : undefined}}>
				{children}
			</AbsoluteFill>
			{/* blocos de compressão: grade leve que "pulsa" a cada keyframe */}
			<AbsoluteFill style={{backgroundImage: 'linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px)', backgroundSize: '16px 16px', opacity: 0.5 + 0.5 * (Math.floor(t * 4) % 12 === 0 ? 1 : 0)}} />
			<Grain opacity={0.2} scale={1.6} fps={12} blend="overlay" />
			<Grain opacity={0.06} scale={1} fps={12} blend="screen" />
			<Vignette opacity={0.55} />
			{fail && <AbsoluteFill style={{background: 'rgba(20,40,120,0.35)', mixBlendMode: 'screen'}} />}
			<OSD style={{left: 56, top: 44}}>{cam}</OSD>
			<OSD style={{right: 56, top: 44}}>{`${date}  ${hh}:${mm}:${ss}`}</OSD>
			<OSD style={{left: 56, bottom: 46, fontSize: 24, opacity: 0.85}}>{'● REC'}</OSD>
		</AbsoluteFill>
	);
};

// ---------- Celular ----------
// Câmera na mão: tremor natural (somas de ruído), foco que respira, exposição automática que corrige atrasada,
// ruído de sensor em pouca luz e balanço de branco instável.
export const PhoneCam: React.FC<{children: React.ReactNode; shake?: number; focus?: number; seed?: string; dark?: number; extraBlur?: number; shakeBoost?: number}> = ({children, shake = 1, focus = 1, seed = 'p', dark = 0, extraBlur = 0, shakeBoost = 0}) => {
	const fr = useCurrentFrame(); const t = fr / FPS;
	const k = shake + shakeBoost;
	const x = (noise1(`${seed}x`, t * 0.9) * 22 + noise1(`${seed}x2`, t * 6) * 4 + noise1(`${seed}x3`, t * 19) * 1.6 * (1 + shakeBoost * 2)) * k;
	const y = (noise1(`${seed}y`, t * 0.8) * 18 + noise1(`${seed}y2`, t * 5.5) * 4 + noise1(`${seed}y3`, t * 17) * 1.6 * (1 + shakeBoost * 2)) * k;
	const r = (noise1(`${seed}r`, t * 0.5) * 1.4 + noise1(`${seed}r2`, t * 7) * 0.3 * (1 + shakeBoost)) * k;
	const fb = Math.max(0, (noise1(`${seed}f`, t * 0.35) + 0.25) * 2.2) * focus + extraBlur;   // respiração de foco
	const ex = 1 + noise1(`${seed}e`, t * 0.25) * 0.12 - dark;                                 // exposição automática
	const wb = noise1(`${seed}w`, t * 0.2) * 8;
	return (
		<AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
			<AbsoluteFill style={{transform: `translate(${x}px, ${y}px) rotate(${r}deg) scale(1.08)`, filter: `blur(${fb}px) brightness(${ex}) hue-rotate(${wb}deg) contrast(1.06) saturate(0.85)`}}>
				{children}
			</AbsoluteFill>
			<Grain opacity={0.16 + dark * 0.25} scale={1.2} fps={30} blend="overlay" />
			<Grain opacity={0.05 + dark * 0.1} scale={1} fps={30} blend="screen" />
			<Vignette opacity={0.35} />
		</AbsoluteFill>
	);
};
