import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, SHADOW, sans, serif} from '../cutout/theme';
import {CutPath, Ink, Label, Piece, Sheet} from '../cutout/Paper';
import {P, ell, rect} from '../cutout/noise';
import {Enter, st} from '../cutout/motion';
import {Puppet, Look} from '../characters/Puppet';
import {PoseName} from '../characters/poses';
import {SceneT} from '../timing';

export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export type SP = {sc: SceneT};

/** Percurso em passos de 3 frames. */
export const useMove = (f0: number, f1: number, a: [number, number], b: [number, number]) => {
	const f = st(useCurrentFrame());
	const p = clamp((f - f0) / Math.max(1, f1 - f0));
	return {x: a[0] + (b[0] - a[0]) * p, y: a[1] + (b[1] - a[1]) * p, moving: f >= f0 && f < f1, done: f >= f1};
};

export const Walker: React.FC<{from: number; to: number; a: [number, number]; b: [number, number]; look: Look; s?: number; flip?: boolean; seed?: number; after?: PoseName; during?: PoseName; z?: number; until?: number; speed?: number}> = ({from, to, a, b, look, s = 1, flip, seed = 1, after = 'idle', during = 'walk', z, until, speed = 1}) => {
	const f = useCurrentFrame();
	const m = useMove(from, to, a, b);
	if (f < from || (until !== undefined && f >= until)) return null;
	return <Puppet x={m.x} y={m.y} s={s} flip={flip} look={look} pose={m.moving ? during : after} seed={seed} z={z} speed={speed} startAt={from} />;
};

/** Pinos e mapa do litoral sul paulista (esquemático e original). Painel em (360,80), 1200x760. */
export const MAP = {x: 340, y: 70, w: 1240, h: 760};
export const COAST = {
	saoVicente: [MAP.x + 1060, MAP.y + 235] as [number, number],
	icapara: [MAP.x + 800, MAP.y + 420] as [number, number],
	iguape: [MAP.x + 745, MAP.y + 470] as [number, number],
	cananeia: [MAP.x + 620, MAP.y + 575] as [number, number],
	santaCatarina: [MAP.x + 440, MAP.y + 715] as [number, number],
};
const landPts: P[] = [[0, 0], [1240, 0], [1240, 130], [1070, 235], [920, 330], [800, 420], [745, 470], [620, 575], [520, 650], [440, 715], [380, 760], [0, 760]];

export const CoastMap: React.FC<{at: number; until?: number; places?: string[]; seed?: number; fill?: string; land?: string; kind?: 'drop' | 'left' | 'right' | 'up' | 'pop'}> = ({at, until, places = [], seed = 21, fill = C.sea, land = C.sand, kind = 'drop'}) => {
	const f = st(useCurrentFrame());
	return (
		<Enter at={at} until={until} kind={kind} seed={seed}>
			<Sheet x={MAP.x} y={MAP.y} w={MAP.w} h={MAP.h} fill={fill} seed={seed} amp={5}>
				<svg width={MAP.w} height={MAP.h} style={{position: 'absolute', overflow: 'visible'}}>
					{Array.from({length: 9}, (_, i) => <path key={i} d={`M ${760 + ((i * 140 + f * 1.2) % 460)} ${520 + (i % 3) * 90} q 22 -20 44 0 q 22 20 44 0`} stroke={C.sea2} strokeWidth={8} fill="none" strokeLinecap="round" />)}
					<CutPath pts={landPts} fill={land} seed={seed + 1} amp={7} sw={6} />
					<CutPath pts={ell(260, 130, 330, 160, 18)} fill={C.forest2} seed={seed + 2} amp={14} outline={null} opacity={0.5} />
					<CutPath pts={ell(220, 150, 380, 470, 18)} fill={C.forest} seed={seed + 3} amp={14} outline={null} opacity={0.32} />
					<CutPath pts={ell(150, 90, 880, 120, 14)} fill={C.forest2} seed={seed + 4} amp={10} outline={null} opacity={0.4} />
				</svg>
				{(Object.keys(COAST) as (keyof typeof COAST)[]).filter((k) => places.includes(k)).map((k) => <Pin key={k} k={k} />)}
			</Sheet>
		</Enter>
	);
};
const NAMES: Record<string, string> = {saoVicente: 'São Vicente', icapara: 'Icapara', iguape: 'Iguape', cananeia: 'Cananeia', santaCatarina: 'Ilha de Santa Catarina'};
const Pin: React.FC<{k: keyof typeof COAST}> = ({k}) => {
	const [x, y] = [COAST[k][0] - MAP.x, COAST[k][1] - MAP.y];
	const right = k !== 'icapara';
	return (
		<div style={{position: 'absolute', left: x, top: y}}>
			<svg width={1} height={1} style={{overflow: 'visible', position: 'absolute'}}>
				<CutPath pts={ell(11, 11, 0, 0, 8)} fill={C.terra} seed={5} amp={1} sw={4} />
			</svg>
			<div style={{position: 'absolute', left: right ? 22 : -22, top: -24, transform: right ? 'none' : 'translateX(-100%)', fontFamily: sans, fontWeight: 800, fontSize: 30, color: C.white, whiteSpace: 'nowrap', textShadow: '2px 2px 0 rgba(0,0,0,0.35)'}}>{NAMES[k]}</div>
		</div>
	);
};

/** Mapa-múndi esquemático (recortes): Américas a oeste, Europa/África a leste. Painel 1600x760 em (160,70). */
export const WORLD = {x: 160, y: 70, w: 1600, h: 760};
export const WorldMap: React.FC<{at: number; until?: number; seed?: number; kind?: 'drop' | 'left' | 'right' | 'up' | 'pop'}> = ({at, until, seed = 31, kind = 'drop'}) => {
	const f = st(useCurrentFrame());
	const americas: P[] = [[60, 0], [330, 0], [380, 120], [330, 200], [420, 300], [500, 360], [575, 430], [545, 520], [470, 600], [400, 720], [330, 760], [300, 640], [330, 520], [250, 420], [160, 300], [90, 200], [40, 100]];
	const eurafrica: P[] = [[1010, 60], [1250, 0], [1560, 0], [1600, 120], [1560, 260], [1480, 380], [1420, 520], [1340, 640], [1240, 700], [1180, 600], [1160, 460], [1100, 360], [1000, 330], [960, 230], [1000, 140]];
	return (
		<Enter at={at} until={until} kind={kind} seed={seed}>
			<Sheet x={WORLD.x} y={WORLD.y} w={WORLD.w} h={WORLD.h} fill={C.sea} seed={seed} amp={5}>
				<svg width={WORLD.w} height={WORLD.h} style={{position: 'absolute', overflow: 'visible'}}>
					{Array.from({length: 12}, (_, i) => <path key={i} d={`M ${520 + ((i * 97 + f * 1.1) % 520)} ${70 + (i % 5) * 140} q 22 -20 44 0 q 22 20 44 0`} stroke={C.sea2} strokeWidth={8} fill="none" strokeLinecap="round" />)}
					<CutPath pts={americas} fill={C.sand} seed={seed + 1} amp={7} sw={6} />
					<CutPath pts={eurafrica} fill={C.sand} seed={seed + 2} amp={7} sw={6} />
				</svg>
			</Sheet>
		</Enter>
	);
};
/** Coordenadas úteis do mapa-múndi (absolutas). */
export const WP = {line: WORLD.x + 470, cabo: [WORLD.x + 900, WORLD.y + 380] as [number, number], brazil: [WORLD.x + 560, WORLD.y + 470] as [number, number], south: [WORLD.x + 520, WORLD.y + 560] as [number, number]};

/** Seta grande de papel. */
export const Arrow: React.FC<{x: number; y: number; len?: number; rot?: number; fill?: string; at: number; seed?: number}> = ({x, y, len = 300, rot = 0, fill = C.terra, at, seed = 3}) => (
	<Enter at={at} kind="pop" seed={seed}>
		<Piece x={x} y={y} rot={rot}>
			<CutPath pts={[[0, -22], [len - 60, -22], [len - 60, -54], [len, 0], [len - 60, 54], [len - 60, 22], [0, 22]]} fill={fill} seed={seed} amp={2.4} />
		</Piece>
	</Enter>
);

export const BigText: React.FC<{x: number; y: number; text: string; size?: number; color?: string; at: number; until?: number; rot?: number; sub?: string}> = ({x, y, text, size = 120, color = C.ink, at, until, rot = -2, sub}) => (
	<Enter at={at} until={until} kind="drop" seed={9}>
		<div style={{position: 'absolute', left: x - 900, width: 1800, top: y - size, textAlign: 'center', fontFamily: serif, fontWeight: 900, fontSize: size, color, transform: `rotate(${rot}deg)`, filter: SHADOW}}>{text}{sub && <div style={{fontFamily: sans, fontSize: size * 0.32, fontWeight: 800, marginTop: 6}}>{sub}</div>}</div>
	</Enter>
);

/** Quadro "Atenção" (aviso de cautela histórica). */
export const Notice: React.FC<{x: number; y: number; w?: number; text: string; at: number; until?: number; rot?: number}> = ({x, y, w = 900, text, at, until, rot = 1}) => (
	<Enter at={at} until={until} kind="drop" seed={4}>
		<Sheet x={x - w / 2} y={y} w={w} h={132} fill={C.parch2} rot={rot} seed={13} tape>
			<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 40px', textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 34, color: C.es, lineHeight: 1.18}}>{text}</div>
		</Sheet>
	</Enter>
);
