import React from 'react';
import {AbsoluteFill, Img, Sequence, random, staticFile, useCurrentFrame} from 'remotion';
import {FPS, f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {PhoneCam} from '../components/devices';
import {Grain, SliceGlitch, VHS, ramp, smooth} from '../components/fx';
import {StrokeMask, useFogStrokes} from '../components/FogWriting';
import {PlateSpace, Seq} from '../components/plate';
import {Snd, Sounds} from '../components/AudioLayer';

// S05 — A gravação final. Imagem muito ruim, por cima do ombro de Clara. Ela sussurra; silêncio.
// O reflexo leva a mão ao vidro embaçado e escreve. Interferência. O celular cai: vemos o piso,
// ouvimos a respiração, e ao fundo ela está olhando para a câmera.
const T0 = 2.5; const MIR = 21; const FALL = T0 + MIR; const FLOOR = FALL + 0.8; const FLOOR_DUR = 8;

// espelho (coordenadas da imagem-base s05_a): vidro visível à esquerda do cabelo dela
const GL = {x0: 480, y0: 93, x1: 778, y1: 768};
const LINES = [{text: 'AGORA', x: 515, y: 118, size: 38}, {text: 'É', x: 600, y: 184, size: 38}, {text: 'MINHA', x: 512, y: 250, size: 38}, {text: 'VEZ', x: 552, y: 316, size: 38}];
const WRITE0 = 14.0, WRITE1 = 20.6;           // tempo da escrita (u)
const HAND = {w: 150, tipX: 0.345, tipY: 0.1};  // ponta do indicador na imagem da mão (fração)

const pointAt = (d: string, frac: number) => {
	const pts = d.slice(1).split(' L').map((p) => p.split(' ').map(Number));
	let tot = 0; const seg: number[] = [];
	for (let i = 1; i < pts.length; i++) {const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(l); tot += l;}
	let want = frac * tot;
	for (let i = 1; i < pts.length; i++) {
		if (want <= seg[i - 1]) {const k = want / (seg[i - 1] || 1); return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k];}
		want -= seg[i - 1];
	}
	return pts[pts.length - 1];
};

const Mirror: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	const {strokes, total} = useFogStrokes(LINES, 'esc');
	const prog = ramp(u, WRITE0, WRITE1);
	// posição da ponta do dedo: fim do traço atual
	let acc = 0, tip: number[] = [GL.x0 + 120, 640];
	const P = prog * total;
	for (const s of strokes) {const st = acc; acc += s.len + 60; if (P >= st) tip = pointAt(s.d, Math.min(1, (P - st) / s.len));}
	// mão: sobe do fundo do espelho (11–13.6), encosta (13.6), escreve, e se afasta (20.6–21)
	const rise = smooth(u, 11, 13.6), leave = smooth(u, 20.4, 21);
	const press = smooth(u, 13.4, 13.8);
	const start = [GL.x0 + 150, 560];
	const hx = (rise < 1 ? start[0] : tip[0]) + (u < 14 ? (tip[0] - start[0]) * smooth(u, 13.6, 14) : 0);
	const hy = (u < 14 ? 760 - (760 - start[1]) * rise : tip[1]) + leave * 220;
	const hScale = 0.75 + 0.25 * press - 0.1 * leave;
	const hBlur = 6 - 4.5 * press + 6 * leave;
	const fogA = 0.32 + 0.12 * ramp(u, 0, 10);
	const show = u > 10.8 && u < 21.2;
	return (
		<div style={{position: 'absolute', left: 0, top: 0, width: 1344, height: 768}}>
			{/* mão do reflexo, por trás do vapor */}
			{show && (
				<div style={{position: 'absolute', left: GL.x0, top: GL.y0, width: GL.x1 - GL.x0, height: GL.y1 - GL.y0, overflow: 'hidden'}}>
					<Img src={staticFile('assets/plates/hand_alpha.png')} style={{position: 'absolute', width: HAND.w * hScale, left: hx - GL.x0 - HAND.w * hScale * HAND.tipX, top: hy - GL.y0 - HAND.w * 1.333 * hScale * HAND.tipY, filter: `blur(${hBlur}px) brightness(0.5) sepia(0.2)`, opacity: 0.85 - 0.85 * leave}} />
				</div>
			)}
			<svg width={1344} height={768} style={{position: 'absolute', left: 0, top: 0}}>
				<defs>
					<clipPath id="glass"><rect x={GL.x0} y={GL.y0} width={GL.x1 - GL.x0} height={GL.y1 - GL.y0} /></clipPath>
					<filter id="fogN"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves={3} seed={4} /><feColorMatrix type="matrix" values="0 0 0 0 0.8  0 0 0 0 0.82  0 0 0 0 0.82  0 0 0 1.2 -0.2" /><feGaussianBlur stdDeviation="2" /></filter>
					<mask id="fogM">
						<rect x={0} y={0} width={1344} height={768} fill="white" />
						<StrokeMask strokes={strokes} total={total} progress={prog} width={14} color="black" blur={2.5} />
						{u > 13.6 && <ellipse cx={start[0] + 6} cy={start[1] + 30} rx={34} ry={46} fill="black" style={{filter: 'blur(12px)'}} opacity={0.4} />}
					</mask>
				</defs>
				<g clipPath="url(#glass)" mask="url(#fogM)">
					<rect x={GL.x0} y={GL.y0} width={GL.x1 - GL.x0} height={GL.y1 - GL.y0} fill={`rgba(205,210,208,${fogA})`} />
					<rect x={GL.x0} y={GL.y0} width={GL.x1 - GL.x0} height={GL.y1 - GL.y0} filter="url(#fogN)" opacity={0.55} />
				</g>
				{/* gotinhas que escorrem dos traços */}
				<g clipPath="url(#glass)" opacity={0.5}>
					{strokes.slice(0, Math.floor(prog * strokes.length)).map((s, i) => {
						const p = pointAt(s.d, 1); const run = 18 + random(`dr${i}`) * 50 * ramp(u, WRITE0 + i * 0.4, WRITE1 + 3);
						return random(`dd${i}`) < 0.5 ? <line key={i} x1={p[0]} y1={p[1]} x2={p[0] + 1} y2={p[1] + run} stroke="rgba(30,30,30,0.6)" strokeWidth={2.2} /> : null;
					})}
				</g>
			</svg>
		</div>
	);
};

const Footage: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	const inter = 0.08 + 0.5 * ramp(u, 19.5, 21) + (random(`i5${Math.floor(u * 6)}`) < 0.06 ? 0.4 : 0);
	return (
		<VHS strength={0.9} tracking={0.3 + ramp(u, 19, 21)} seed="s05">
			<PhoneCam shake={0.55} focus={0.5} seed="s05" dark={0.18} shakeBoost={0.6 * ramp(u, 19.5, 21)}>
				<SliceGlitch amount={inter} seed="s05g">
					<PlateSpace><Seq dir="s05" count={315} fps={15} /><Mirror /></PlateSpace>
					<Grain opacity={0.25} scale={3} fps={15} blend="overlay" />
				</SliceGlitch>
			</PhoneCam>
		</VHS>
	);
};

// queda do celular: o último quadro gira e desce, com borrão de movimento
const Fall: React.FC = () => {
	const fr = useCurrentFrame(); const k = fr / f(0.8);
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<AbsoluteFill style={{transform: `rotate(${-95 * k * k}deg) translateY(${600 * k * k}px) scale(${1 + 0.3 * k})`, filter: `blur(${2 + 16 * k}px) brightness(${1 - 0.6 * k})`}}>
				<PlateSpace><Seq dir="s05" count={315} fps={15} hold={314} /></PlateSpace>
			</AbsoluteFill>
			{k > 0.85 && <AbsoluteFill style={{background: '#fff', opacity: 0.25}} />}
		</AbsoluteFill>
	);
};

const Floor: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	return (
		<VHS strength={0.8} tracking={0.15} seed="fl">
			<PhoneCam shake={0.08} focus={0.4} seed="fl" dark={0.32}>
				<AbsoluteFill style={{transform: 'rotate(-7deg) scale(1.15)'}}>
					<SliceGlitch amount={u < 0.4 ? 0.7 : random(`fg${Math.floor(u * 5)}`) < 0.05 ? 0.3 : 0} seed="flg">
						<PlateSpace><Seq dir="s05_floor" count={120} fps={15} /></PlateSpace>
					</SliceGlitch>
				</AbsoluteFill>
				<Grain opacity={0.3} scale={3} fps={15} blend="overlay" />
			</PhoneCam>
		</VHS>
	);
};

const SND: Snd[] = [
	{name: 'glitch_b', at: 0, vol: 0.55},
	{name: 'vhs_hiss', at: 0, dur: T0 + 0.2, vol: 0.4},
	{name: 'phone_room', at: T0, dur: MIR, vol: 0.5},
	{name: 'hum', at: T0, dur: MIR, vol: 0.22},
	{name: 'v_ouvindo', at: T0 + 3.5, vol: 1},
	{name: 'low_drone', at: T0 + 10.5, dur: 11, vol: 0.32, fadeIn: 4, fadeOut: 0.3},
	{name: 'glass_squeak', at: T0 + 13.6, vol: 0.4},
	{name: 'glass_squeak', at: T0 + 15.9, vol: 0.45},
	{name: 'glass_squeak', at: T0 + 18.2, vol: 0.4},
	{name: 'glitch_b', at: T0 + 19.6, vol: 0.5},
	{name: 'glitch_a', at: FALL - 0.4, vol: 0.6},
	{name: 'phone_drop', at: FALL + 0.55, vol: 0.9},
	{name: 'breathing', at: FLOOR + 0.6, dur: FLOOR_DUR - 0.6, vol: 0.75, fadeOut: 0.2},
	{name: 'hum', at: FLOOR, dur: FLOOR_DUR, vol: 0.16},
];

export const FinalRecording: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Sequence durationInFrames={f(T0)}>
			<ArchiveCard dur={T0} corrupt={0.9} lines={['ARQUIVO 0074', 'DISPOSITIVO: CELULAR', 'DATA: 15/11/2026  03:12', 'STATUS: CORROMPIDO']} />
		</Sequence>
		<Sequence from={f(T0)} durationInFrames={f(MIR)}><Footage /></Sequence>
		<Sequence from={f(FALL)} durationInFrames={f(0.8)}><Fall /></Sequence>
		<Sequence from={f(FLOOR)} durationInFrames={f(FLOOR_DUR)}><Floor /></Sequence>
		<Sounds list={SND} />
	</AbsoluteFill>
);
