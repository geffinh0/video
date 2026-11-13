import React from 'react';
import {AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {loadFont} from '@remotion/google-fonts/CormorantGaramond';
import {EXTERIOR, FPS, INTERIOR_CANDLE, Shot as ShotT} from './timing';
import {Fog, GlassDrops, Grain, Layer, Rain, flicker} from './fx';
import manifest from './data/manifest.json';

const {fontFamily: serif} = loadFont('normal', {weights: ['500', '600']});
const M = manifest as Record<string, {plate: boolean; layer: number}>;
const ease = Easing.bezier(0.42, 0, 0.58, 1);

const Missing: React.FC<{id: string; desc: string}> = ({id, desc}) => (
	<AbsoluteFill style={{background: '#0b0d10', color: '#556', fontFamily: serif, fontSize: 34, alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 80}}>
		[{id}] {desc}
	</AbsoluteFill>
);

/** Planos 2D (foto, relógio, retrato) a partir das texturas do filme. */
const Photo2D: React.FC = () => (
	<AbsoluteFill style={{background: 'radial-gradient(ellipse at 30% 30%, #3a2210 0%, #140a04 55%, #050302 100%)'}}>
		<div style={{position: 'absolute', left: 760, top: 40, width: 420, height: 560, transform: 'rotate(-4deg)', boxShadow: '30px 40px 60px rgba(0,0,0,0.8)', border: '18px solid #6b6258', outline: '3px solid #2b2620'}}>
			<Img src={staticFile('textures/photo_couple.png')} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(2.2px) contrast(0.95) brightness(0.72)'}} />
		</div>
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 25% 20%, rgba(255,170,80,0.35) 0%, rgba(0,0,0,0) 45%)', mixBlendMode: 'screen'}} />
	</AbsoluteFill>
);

const Clock2D: React.FC<{face: string; t: number; dawn?: boolean}> = ({face, t, dawn}) => {
	const swing = Math.sin(t * Math.PI) * 7;
	return (
		<AbsoluteFill style={{background: dawn ? 'radial-gradient(ellipse at 50% 40%, #2a2c30 0%, #0c0d10 70%)' : 'radial-gradient(ellipse at 50% 40%, #3b200c 0%, #120803 70%)'}}>
			<div style={{position: 'absolute', left: 960 - 330, top: 40, width: 660, height: 660, borderRadius: '50%', border: '34px solid #3a1c0b', boxShadow: 'inset 0 0 60px rgba(0,0,0,0.8), 0 30px 80px rgba(0,0,0,0.9)', overflow: 'hidden'}}>
				<Img src={staticFile(`textures/${face}`)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: dawn ? 'brightness(0.75) saturate(0.6)' : 'brightness(0.9) sepia(0.25)'}} />
			</div>
			<div style={{position: 'absolute', left: 958, top: 720, width: 4, height: 300, background: 'linear-gradient(#a07a3a,#5a4020)', transformOrigin: '50% 0', transform: `rotate(${swing}deg)`, opacity: dawn ? 0 : 0.9}} />
			<AbsoluteFill style={{background: dawn ? 'linear-gradient(90deg, rgba(120,150,190,0.18), rgba(0,0,0,0) 60%)' : 'radial-gradient(ellipse at 80% 30%, rgba(255,160,70,0.28) 0%, rgba(0,0,0,0) 55%)', mixBlendMode: 'screen'}} />
		</AbsoluteFill>
	);
};

const Portrait2D: React.FC = () => (
	<AbsoluteFill style={{background: 'radial-gradient(ellipse at 60% 30%, #2a2018 0%, #0d0907 70%)'}}>
		<div style={{position: 'absolute', left: 760, top: 60, width: 400, height: 540, transform: 'rotate(9deg)', border: '30px solid #6d4b18', boxShadow: 'inset 0 0 30px rgba(0,0,0,0.8), 20px 30px 60px rgba(0,0,0,0.9)', outline: '6px solid #3a2608'}}>
			<Img src={staticFile('textures/eleanor_portrait.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
		</div>
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 30% 10%, rgba(255,160,70,0.25) 0%, rgba(0,0,0,0) 50%)', mixBlendMode: 'screen'}} />
	</AbsoluteFill>
);

const Title: React.FC<{t: number}> = ({t}) => {
	const o = interpolate(t, [0.3, 1.8, 4.0, 4.9], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', background: '#000'}}>
			<div style={{fontFamily: serif, fontWeight: 600, fontSize: 118, letterSpacing: 26, color: '#d8d2c6', opacity: o * flicker(t * 24, 0.04), textShadow: '0 0 30px rgba(200,190,170,0.25)'}}>O ÚLTIMO POUSO</div>
		</AbsoluteFill>
	);
};

const CREDITS = ['O ÚLTIMO POUSO', '', 'Uma obra original inspirada na atmosfera de “O Corvo”, de Edgar Allan Poe', '', 'Arthur Blackwood • Eleanor Blackwood • O Corvo', '', 'Imagens 3D: Blender (Cycles)  •  Montagem: Remotion', 'Vozes: Kokoro-82M (código aberto)', 'Sons e trilha: sintetizados para este filme'];
const Credits: React.FC<{t: number; dur: number}> = ({t, dur}) => {
	const y = interpolate(t, [0, dur], [520, -260]);
	const o = interpolate(t, [0, 1.2, dur - 1.5, dur], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	return (
		<AbsoluteFill style={{background: '#000', opacity: o}}>
			<div style={{position: 'absolute', top: y, width: '100%', textAlign: 'center', fontFamily: serif, color: '#cfc8bb'}}>
				{CREDITS.map((c, i) => <div key={i} style={{fontSize: i === 0 ? 72 : 36, letterSpacing: i === 0 ? 16 : 2, margin: '10px 0', minHeight: 20}}>{c}</div>)}
			</div>
		</AbsoluteFill>
	);
};

export const ShotView: React.FC<{s: ShotT & {frames: number}}> = ({s}) => {
	const f = useCurrentFrame(); const t = f / FPS; const p = Math.min(1, f / s.frames);
	if (s.set === 'black') return <AbsoluteFill style={{background: '#000'}} />;
	if (s.set === 'title') return <Title t={t} />;
	if (s.set === 'credits') return <Credits t={t} dur={s.dur} />;
	const zoom = s.move?.zoom ? interpolate(ease(p), [0, 1], s.move.zoom) : 1;
	const pan = s.move?.pan ? [interpolate(ease(p), [0, 1], [s.move.pan[0][0], s.move.pan[1][0]]), interpolate(ease(p), [0, 1], [s.move.pan[0][1], s.move.pan[1][1]])] : [0, 0];
	const m = M[s.id] ?? {plate: false, layer: 0};
	const candle = INTERIOR_CANDLE.has(s.set) && !s.set.startsWith('dawn');
	const bright = candle ? flicker(f, 0.045) : 1;
	const rack = s.rack ? interpolate(t, s.rack, [0, 7], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
	const ext = EXTERIOR.has(s.set);
	const grade = `${s.warm ? 'sepia(0.45) saturate(1.25) brightness(1.05)' : ext ? 'saturate(0.7) hue-rotate(-6deg) brightness(0.62)' : 'saturate(0.88)'} contrast(1.1) brightness(${bright})`;
	let content: React.ReactNode;
	if (s.set === 'photo') content = <Photo2D />;
	else if (s.set === 'clock') content = <Clock2D face="clock_face.png" t={t} />;
	else if (s.set === 'clock_317') content = <Clock2D face="clock_face_317.png" t={t} dawn />;
	else if (s.set === 'portrait') content = <Portrait2D />;
	else if (s.inserts) {
		const k = Math.min(s.inserts.length - 1, Math.floor(t / (s.dur / s.inserts.length)));
		const id = s.inserts[k]; const local = t - k * (s.dur / s.inserts.length);
		content = M[id]?.plate ? <Img src={staticFile(`scenes/${id}/plate.png`)} style={{width: '100%', height: '100%', transform: `scale(${1.05 + local * 0.06})`}} /> : <Missing id={id} desc="inserto" />;
	} else if (m.plate) {
		content = (
			<>
				<Img src={staticFile(`scenes/${s.id}/plate.png`)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', filter: rack ? `blur(${rack}px)` : undefined}} />
				<Layer id={s.id} count={m.layer} t={t} />
			</>
		);
	} else content = <Missing id={s.id} desc={s.desc} />;
	const flash = (s.flash ?? []).reduce((a, ft) => Math.max(a, interpolate(t, [ft - 0.02, ft, ft + 0.08, ft + 0.16, ft + 0.5], [0, 0.85, 0.2, 0.6, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})), 0);
	const black = s.blackout ? interpolate(t, [s.blackout[0], s.blackout[0] + 0.12, s.blackout[1] - 0.25, s.blackout[1]], [0, 1, 1, s.id === 's29' ? 1 : 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
	const insertFlash = s.inserts ? interpolate((t % (s.dur / s.inserts.length)), [0, 0.06, 0.18], [0.7, 0.25, 0], {extrapolateRight: 'clamp'}) : 0;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<div style={{position: 'absolute', left: 0, top: 140, width: 1920, height: 800, overflow: 'hidden'}}>
				<div style={{position: 'absolute', inset: 0, transform: `translate(${pan[0]}px, ${pan[1]}px) scale(${zoom})`, filter: grade}}>{content}</div>
				{ext && <><Fog opacity={0.18} /><Rain /></>}
				{(s.rainGlass || ['window_int', 'ots_window', 'arthur_recoil', 'raven_eye'].includes(s.set)) && <GlassDrops opacity={s.rainGlass ? 0.45 : 0.25} />}
				{['study_return', 'raven_chair', 'raven_wings'].includes(s.set) && <Rain density={90} opacity={0.12} />}
				{s.warm && <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, rgba(255,150,60,0.18), rgba(40,15,0,0.35))', mixBlendMode: 'screen'}} />}
				<AbsoluteFill style={{background: '#fff', opacity: Math.max(flash, insertFlash), mixBlendMode: 'screen'}} />
				<AbsoluteFill style={{background: '#000', opacity: black}} />
				<Grain amount={0.12} />
			</div>
		</AbsoluteFill>
	);
};
