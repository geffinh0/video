import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C} from '../cutout/theme';
import {CutPath, Ink, Piece} from '../cutout/Paper';
import {P, ell, rect} from '../cutout/noise';
import {st} from '../cutout/motion';

type B = {x: number; y: number; s?: number; flip?: boolean; seed?: number; rot?: number; z?: number};

export const Caravel: React.FC<B & {flag?: string; sail?: string}> = ({x, y, s = 1, flip, seed = 1, rot, z, flag = C.pt, sail = C.white}) => {
	const bob = Math.sin(st(useCurrentFrame()) / 14) * 4;
	return (
		<Piece x={x} y={y + bob} s={s} flip={flip} rot={(rot ?? 0) + Math.sin(st(useCurrentFrame()) / 17) * 1.2} z={z}>
			<CutPath pts={rect(8, 190, -60, -200)} fill={C.wood} seed={seed} amp={1} sw={4} />
			<CutPath pts={rect(8, 150, 40, -160)} fill={C.wood} seed={seed + 1} amp={1} sw={4} />
			<CutPath pts={[[-52, -190], [-52, -50], [-190, -50]]} fill={sail} seed={seed + 2} amp={2} />
			<CutPath pts={[[-44, -195], [-44, -55], [70, -55], [70, -195]]} fill={sail} seed={seed + 3} amp={2} />
			<path d="M -2 -170 L -2 -80 M -34 -125 L 30 -125" stroke={flag} strokeWidth={14} />
			<CutPath pts={[[48, -155], [48, -70], [150, -70]]} fill={sail} seed={seed + 4} amp={2} />
			<CutPath pts={[[-215, -30], [210, -30], [150, 40], [-150, 40]]} fill={C.wood2} seed={seed + 5} amp={2.4} />
			<CutPath pts={[[-215, -30], [-150, -48], [210, -48], [210, -30]]} fill={C.wood} seed={seed + 6} amp={2} />
			<Ink d="M -150 0 L 150 0 M -120 18 L 120 18" w={3} />
			<CutPath pts={[[-60, -200], [-60, -226], [-20, -213]]} fill={flag} seed={seed + 7} amp={1} sw={3} />
		</Piece>
	);
};

export const FrenchShip: React.FC<B> = ({x, y, s = 1, flip, seed = 3, rot, z}) => {
	const f = st(useCurrentFrame());
	return (
		<Piece x={x} y={y + Math.sin(f / 14) * 4} s={s} flip={flip} rot={(rot ?? 0) + Math.sin(f / 17) * 1.2} z={z}>
			{[-110, 0, 110].map((mx, i) => (
				<g key={i}>
					<CutPath pts={rect(8, 200, mx - 4, -230 + (i === 1 ? -30 : 0))} fill={C.wood} seed={seed + i} amp={1} sw={4} />
					<CutPath pts={[[mx - 70, -200 + (i === 1 ? -30 : 0)], [mx + 70, -200 + (i === 1 ? -30 : 0)], [mx + 60, -90], [mx - 60, -90]]} fill={C.parch2} seed={seed + 10 + i} amp={2} />
					<CutPath pts={[[mx, -232 + (i === 1 ? -30 : 0)], [mx + 54, -218 + (i === 1 ? -30 : 0)], [mx, -204 + (i === 1 ? -30 : 0)]]} fill="#3A5F8F" seed={seed + 20 + i} amp={1} sw={3} />
				</g>
			))}
			<CutPath pts={[[-240, -40], [240, -40], [190, 50], [-190, 50]]} fill="#3B3A3A" seed={seed + 5} amp={2.4} />
			<CutPath pts={[[-240, -40], [-170, -60], [240, -60], [240, -40]]} fill="#55524E" seed={seed + 6} amp={2} />
			{[-120, -60, 0, 60, 120].map((px) => <circle key={px} cx={px} cy={0} r={8} fill={C.ink} opacity={0.7} />)}
		</Piece>
	);
};

export const Cannon: React.FC<B & {fire?: number}> = ({x, y, s = 1, flip, seed = 4, rot, z, fire = 0}) => (
	<>
	{fire > 0 && <Smoke x={x + (flip ? -80 : 80) * s} y={y - 48 * s} n={5} spread={50 * s} seed={seed} rise={150 * s} />}
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		<CutPath pts={[[-70, -42], [70, -54], [74, -34], [-64, -26]]} fill="#4E4E52" seed={seed} amp={1.2} />
		<CutPath pts={ell(11, 14, 70, -44, 8)} fill="#3A3A3D" seed={seed + 1} amp={0.8} sw={4} />
		<CutPath pts={[[-52, -26], [34, -26], [48, 6], [-60, 6]]} fill={C.wood2} seed={seed + 2} amp={1.5} />
		<CutPath pts={ell(30, 30, -8, 8, 14)} fill={C.wood} seed={seed + 3} amp={1.8} />
		<circle cx={-8} cy={8} r={7} fill={C.ink} opacity={0.5} />
	</Piece>
	</>
);

export const House: React.FC<B & {roof?: string; wall?: string; burnt?: boolean}> = ({x, y, s = 1, flip, seed = 5, rot, z, roof = C.terra, wall = C.parch2, burnt}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		<CutPath pts={rect(150, 100, -75, -100)} fill={burnt ? '#6E6256' : wall} seed={seed} amp={1.8} />
		<CutPath pts={[[-95, -96], [95, -96], [60, -150], [-60, -150]]} fill={burnt ? '#4A3F38' : roof} seed={seed + 1} amp={2} />
		<CutPath pts={rect(34, 56, -17, -56)} fill={C.wood} seed={seed + 2} amp={1} sw={4} />
		<CutPath pts={rect(28, 28, 28, -80)} fill={burnt ? '#2B2622' : '#5B7E88'} seed={seed + 3} amp={0.8} sw={4} />
		<CutPath pts={rect(28, 28, -56, -80)} fill={burnt ? '#2B2622' : '#5B7E88'} seed={seed + 4} amp={0.8} sw={4} />
	</Piece>
);

export const Church: React.FC<B & {burnt?: boolean}> = ({x, y, s = 1, flip, seed = 6, rot, z}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		<CutPath pts={rect(220, 130, -110, -130)} fill={C.parch2} seed={seed} amp={2} />
		<CutPath pts={[[-130, -126], [130, -126], [90, -190], [-90, -190]]} fill={C.terra} seed={seed + 1} amp={2.2} />
		<CutPath pts={rect(70, 190, 60, -290)} fill={C.white} seed={seed + 2} amp={2} />
		<CutPath pts={[[52, -286], [138, -286], [95, -350]]} fill={C.terra} seed={seed + 3} amp={1.6} />
		<CutPath pts={rect(10, 36, 90, -392)} fill={C.ink} seed={seed + 4} amp={0.5} sw={3} />
		<CutPath pts={rect(36, 10, 77, -380)} fill={C.ink} seed={seed + 5} amp={0.5} sw={3} />
		<CutPath pts={[[-34, 0], [-34, -64], [0, -88], [34, -64], [34, 0]]} fill={C.wood} seed={seed + 6} amp={1.2} sw={4} />
		<CutPath pts={ell(14, 22, -78, -78, 10)} fill="#5B7E88" seed={seed + 7} amp={0.8} sw={4} />
	</Piece>
);

export const Tree: React.FC<B & {c?: string}> = ({x, y, s = 1, flip, seed = 7, rot, z, c = C.forest}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		<CutPath pts={[[-12, 0], [12, 0], [8, -120], [-8, -120]]} fill={C.wood} seed={seed} amp={1.4} sw={4} />
		<CutPath pts={ell(70, 58, 0, -150, 14)} fill={c} seed={seed + 1} amp={4} />
		<CutPath pts={ell(48, 42, -42, -110, 12)} fill={C.forest2} seed={seed + 2} amp={3} />
		<CutPath pts={ell(50, 40, 44, -118, 12)} fill={c} seed={seed + 3} amp={3} />
	</Piece>
);

export const Mangrove: React.FC<B> = ({x, y, s = 1, flip, seed = 8, rot, z}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		{[-70, -35, 0, 35, 70].map((rx, i) => (
			<CutPath key={i} pts={[[rx - 5, 0], [rx + 5, 0], [rx * 0.35 + 4, -105], [rx * 0.35 - 4, -105]]} fill={C.wood} seed={seed + i} amp={1.2} sw={3} />
		))}
		<CutPath pts={ell(90, 56, 0, -135, 14)} fill={C.forest} seed={seed + 9} amp={4} />
		<CutPath pts={ell(52, 40, -50, -120, 10)} fill={C.forest2} seed={seed + 10} amp={3} />
	</Piece>
);

export const Smoke: React.FC<{x: number; y: number; n?: number; spread?: number; seed?: number; rise?: number; col?: string}> = ({x, y, n = 6, spread = 70, seed = 1, rise = 180, col = '#8C877F'}) => {
	const f = st(useCurrentFrame(), 3);
	return (
		<>
			{Array.from({length: n}, (_, i) => {
				const p = ((f / 60 + i / n) % 1);
				const r = 22 + p * 46;
				return <Piece key={i} x={x + Math.sin(i * 2.3 + seed) * spread * p} y={y - p * rise} shadow={false}><CutPath pts={ell(r, r * 0.85, 0, 0, 10)} fill={col} seed={seed + i} amp={3} opacity={1 - p * 0.8} sw={4} /></Piece>;
			})}
		</>
	);
};

export const Fire: React.FC<B> = ({x, y, s = 1, seed = 9}) => {
	const f = Math.floor(useCurrentFrame() / 3);
	const j = (k: number) => 1 + Math.sin(f * 1.7 + k) * 0.14;
	return (
		<Piece x={x} y={y} s={s} shadow={false}>
			<CutPath pts={[[-40, 0], [-30, -70 * j(1)], [-12, -40], [0, -110 * j(2)], [14, -50], [30, -80 * j(3)], [42, 0]]} fill="#C0392B" seed={seed} amp={2} sw={4} />
			<CutPath pts={[[-26, 0], [-12, -50 * j(4)], [0, -76 * j(5)], [14, -44], [28, 0]]} fill="#EE8A1B" seed={seed + 1} amp={2} sw={3} />
			<CutPath pts={[[-12, 0], [0, -40 * j(6)], [12, 0]]} fill="#F7D046" seed={seed + 2} amp={1.4} sw={3} />
		</Piece>
	);
};

export const Book: React.FC<B & {open?: boolean; fill?: string; lines?: number}> = ({x, y, s = 1, flip, seed = 10, rot, z, open, fill = C.terra, lines = 6}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		{open ? (
			<g>
				<CutPath pts={rect(150, 190, -155, -190)} fill={C.parch2} seed={seed} amp={1.4} />
				<CutPath pts={rect(150, 190, 5, -190)} fill={C.parch2} seed={seed + 1} amp={1.4} />
				{Array.from({length: lines}, (_, i) => <Ink key={i} d={`M ${-135} ${-160 + i * 24} L -25 ${-160 + i * 24} M 25 ${-160 + i * 24} L 135 ${-160 + i * 24}`} w={3} o={0.55} />)}
			</g>
		) : (
			<g>
				<CutPath pts={rect(150, 200, -75, -200)} fill={fill} seed={seed} amp={1.6} />
				<CutPath pts={rect(110, 40, -55, -160)} fill={C.ocre} seed={seed + 1} amp={1} sw={3} />
				<Ink d="M -35 -140 L 35 -140" w={4} o={0.6} />
			</g>
		)}
	</Piece>
);

export const Scroll: React.FC<B & {w?: number; h?: number}> = ({x, y, s = 1, seed = 11, rot, z, w = 280, h = 200}) => (
	<Piece x={x} y={y} s={s} rot={rot} z={z}>
		<CutPath pts={rect(w, h, -w / 2, -h)} fill={C.parch2} seed={seed} amp={2} />
		<CutPath pts={rect(w + 30, 26, -w / 2 - 15, -h - 14)} fill={C.sand} seed={seed + 1} amp={1.2} sw={4} />
		<CutPath pts={rect(w + 30, 26, -w / 2 - 15, -14)} fill={C.sand} seed={seed + 2} amp={1.2} sw={4} />
	</Piece>
);

export const Canoe: React.FC<B> = ({x, y, s = 1, flip, seed = 12, rot, z}) => {
	const f = st(useCurrentFrame());
	return (
		<Piece x={x} y={y + Math.sin(f / 12) * 3} s={s} flip={flip} rot={rot} z={z}>
			<CutPath pts={[[-170, -26], [170, -26], [120, 22], [-120, 22]]} fill={C.wood2} seed={seed} amp={2} />
			<Ink d="M -140 -6 L 140 -6" w={3} />
		</Piece>
	);
};

export const Gold: React.FC<B> = ({x, y, s = 1, seed = 13}) => (
	<Piece x={x} y={y} s={s}>
		{[[-20, 0], [8, -6], [26, 4]].map((p, i) => <CutPath key={i} pts={[[p[0] - 10, p[1]], [p[0] - 4, p[1] - 12], [p[0] + 8, p[1] - 10], [p[0] + 12, p[1]]]} fill={C.gold} seed={seed + i} amp={1} sw={3} />)}
	</Piece>
);

export const Crate: React.FC<B & {open?: boolean}> = ({x, y, s = 1, flip, seed = 14, rot, z, open}) => (
	<Piece x={x} y={y} s={s} flip={flip} rot={rot} z={z}>
		<CutPath pts={rect(96, 70, -48, -70)} fill={C.wood2} seed={seed} amp={1.4} />
		<Ink d="M -48 -35 L 48 -35 M 0 -70 L 0 0" w={3} />
		{open && <CutPath pts={[[-50, -70], [50, -70], [34, -108], [-34, -108]]} fill={C.wood} seed={seed + 1} amp={1.4} />}
	</Piece>
);

export const Cloud: React.FC<B & {fill?: string}> = ({x, y, s = 1, seed = 15, fill = C.white}) => (
	<Piece x={x} y={y} s={s} shadow={false}>
		<CutPath pts={ell(90, 36, 0, 0, 12)} fill={fill} seed={seed} amp={3} sw={4} />
		<CutPath pts={ell(50, 36, -34, -22, 10)} fill={fill} seed={seed + 1} amp={3} sw={4} />
		<CutPath pts={ell(54, 38, 28, -26, 10)} fill={fill} seed={seed + 2} amp={3} sw={4} />
	</Piece>
);

export const Waves: React.FC<{y: number; h: number; fill: string; fill2?: string; speed?: number}> = ({y, h, fill, fill2 = C.sea2, speed = 1}) => {
	const f = st(useCurrentFrame(), 3);
	return (
		<>
			<svg width={2100} height={h} style={{position: 'absolute', left: -90, top: y, overflow: 'visible'}}>
				<rect width={2100} height={h} fill={fill} />
				{Array.from({length: 4}, (_, r) =>
					Array.from({length: 18}, (_, i) => {
						const x = ((i * 130 + r * 55 + f * (r % 2 ? 1 : -1) * speed * 1.4) % 2300 + 2300) % 2300 - 100;
						const yy = 30 + r * (h / 4.2);
						return <path key={`${r}-${i}`} d={`M ${x} ${yy} q 25 -22 50 0 q 25 22 50 0`} stroke={fill2} strokeWidth={9} fill="none" strokeLinecap="round" />;
					}),
				)}
			</svg>
			<TornTop y={y} />
		</>
	);
};
const TornTop: React.FC<{y: number}> = ({y}) => <div style={{position: 'absolute', left: 0, top: y - 3, width: 1920, height: 6, background: C.outline, opacity: 0.6}} />;

export const Sun: React.FC<B> = ({x, y, s = 1, seed = 16}) => (
	<Piece x={x} y={y} s={s} shadow={false}>
		{Array.from({length: 12}, (_, i) => <CutPath key={i} pts={[[-12, -150], [12, -150], [0, -200]]} fill="#F2B544" seed={seed + i} amp={1} sw={3} />).map((el, i) => <g key={i} transform={`rotate(${i * 30})`}>{el}</g>)}
		<CutPath pts={ell(110, 110, 0, 0, 20)} fill="#F2C34C" seed={seed + 30} amp={3} />
	</Piece>
);

/** Ícones originais (sem logotipo do YouTube). */
export const IconThumb: React.FC<B> = ({x, y, s = 1, rot, seed = 20}) => (
	<Piece x={x} y={y} s={s} rot={rot}>
		<CutPath pts={rect(40, 70, -85, -75)} fill={C.pt} seed={seed} amp={1.5} />
		<CutPath pts={[[-35, -75], [-5, -75], [20, -130], [42, -120], [28, -75], [80, -75], [80, -5], [-35, -5]]} fill={C.parch2} seed={seed + 1} amp={1.8} />
	</Piece>
);
export const IconBubble: React.FC<B> = ({x, y, s = 1, rot, seed = 21}) => (
	<Piece x={x} y={y} s={s} rot={rot}>
		<CutPath pts={[[-90, -100], [90, -100], [90, 0], [20, 0], [-30, 40], [-24, 0], [-90, 0]]} fill={C.parch2} seed={seed} amp={1.8} />
		<Ink d="M -60 -66 L 60 -66 M -60 -36 L 30 -36" w={6} o={0.5} />
	</Piece>
);
export const IconBell: React.FC<B> = ({x, y, s = 1, rot, seed = 22}) => (
	<Piece x={x} y={y} s={s} rot={rot}>
		<CutPath pts={[[-70, 0], [-50, -70], [-30, -100], [30, -100], [50, -70], [70, 0]]} fill={C.gold} seed={seed} amp={1.8} />
		<CutPath pts={ell(14, 14, 0, 18, 8)} fill={C.ocre} seed={seed + 1} amp={0.8} sw={4} />
	</Piece>
);
export const IconShare: React.FC<B> = ({x, y, s = 1, rot, seed = 23}) => (
	<Piece x={x} y={y} s={s} rot={rot}>
		<CutPath pts={[[-70, -30], [10, -30], [10, -70], [80, 0], [10, 70], [10, 30], [-70, 30]]} fill={C.sea2} seed={seed} amp={1.8} />
	</Piece>
);
