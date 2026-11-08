import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, SHADOW} from '../cutout/theme';
import {CutPath} from '../cutout/Paper';
import {ell, limb, rect, P} from '../cutout/noise';
import {wobbleDeg} from '../cutout/motion';
import {Pose, PoseName, poses} from './poses';

export type Item = 'arcabuz' | 'bow' | 'sword' | 'scroll' | 'book' | 'pan' | 'oar' | 'none';
export type Hat = 'morrion' | 'barrete' | 'hood' | 'wide' | 'none';
export type Look = {
	skin: string; shirt: string; pants: string; hair?: string; hat?: Hat; hatColor?: string; beard?: boolean;
	cape?: string; collar?: boolean; item?: Item; boots?: string; sash?: string; long?: boolean; bare?: boolean;
};

const ItemShape: React.FC<{item: Item; seed: number}> = ({item, seed}) => {
	switch (item) {
		case 'arcabuz': return (<g><CutPath pts={rect(11, 70, -5, -20)} fill={C.wood} seed={seed} amp={1} sw={4} /><CutPath pts={rect(7, 62, -3, 48)} fill="#4A4A4A" seed={seed + 1} amp={1} sw={4} /></g>);
		case 'bow': return (<g><path d="M -52 8 Q 0 -44 52 8" stroke={C.wood} strokeWidth={8} fill="none" strokeLinecap="round" /><path d="M -52 8 L 52 8" stroke={C.ink} strokeWidth={2} /><path d="M 0 -6 L 0 92" stroke={C.wood2} strokeWidth={4} /><path d="M -6 88 L 0 102 L 6 88Z" fill={C.stone} /></g>);
		case 'sword': return (<g><CutPath pts={rect(9, 88, -4.5, 8)} fill="#BFC3C7" seed={seed} amp={0.8} sw={4} /><CutPath pts={rect(34, 8, -17, 2)} fill={C.ocre} seed={seed + 1} amp={0.6} sw={3} /></g>);
		case 'scroll': return (<g><CutPath pts={rect(22, 52, -11, -6)} fill={C.white} seed={seed} amp={1} sw={4} /><CutPath pts={ell(14, 5, 0, -6, 8)} fill={C.parch} seed={seed + 1} amp={0.5} sw={3} /></g>);
		case 'book': return (<CutPath pts={rect(44, 56, -22, -6)} fill={C.terra} seed={seed} amp={1.2} sw={4} />);
		case 'pan': return (<CutPath pts={[[-40, 10], [40, 10], [18, 30], [-18, 30]]} fill="#6C6C6C" seed={seed} amp={1} sw={4} />);
		case 'oar': return (<g><CutPath pts={rect(8, 130, -4, -20)} fill={C.wood2} seed={seed} amp={1} sw={4} /><CutPath pts={rect(24, 50, -12, 100)} fill={C.wood} seed={seed + 1} amp={1} sw={4} /></g>);
		default: return null;
	}
};

const Arm: React.FC<{a: [number, number]; look: Look; ox: number; oy: number; seed: number; item?: Item}> = ({a, look, ox, oy, seed, item}) => (
	<g transform={`translate(${ox} ${oy}) rotate(${a[0]})`}>
		<CutPath pts={limb(54, 19)} fill={look.bare ? look.skin : look.shirt} seed={seed} amp={1.2} sw={5} />
		<g transform={`translate(0 52) rotate(${a[1]})`}>
			<CutPath pts={limb(48, 16)} fill={look.bare ? look.skin : look.shirt} seed={seed + 1} amp={1.2} sw={5} />
			<g transform="translate(0 50)">
				<CutPath pts={ell(8, 9, 0, 3, 8)} fill={look.skin} seed={seed + 2} amp={0.8} sw={4} />
				{item && item !== 'none' && <ItemShape item={item} seed={seed + 3} />}
			</g>
		</g>
	</g>
);

const Leg: React.FC<{a: [number, number]; look: Look; ox: number; seed: number}> = ({a, look, ox, seed}) => (
	<g transform={`translate(${ox} 0) rotate(${a[0]})`}>
		<CutPath pts={limb(62, 24)} fill={look.pants} seed={seed} amp={1.2} sw={5} />
		<g transform={`translate(0 60) rotate(${a[1]})`}>
			<CutPath pts={limb(60, 20)} fill={look.boots ?? look.pants} seed={seed + 1} amp={1.2} sw={5} />
			<CutPath pts={[[-9, 54], [24, 54], [26, 68], [-9, 68]]} fill={look.boots ?? C.ink} seed={seed + 2} amp={1} sw={4} />
		</g>
	</g>
);

const Head: React.FC<{look: Look; seed: number}> = ({look, seed}) => (
	<g>
		<CutPath pts={rect(18, 18, -9, -6)} fill={look.skin} seed={seed} amp={0.6} sw={4} />
		{look.hair && look.long && <CutPath pts={[[-30, -48], [26, -48], [28, 20], [-32, 24]]} fill={look.hair} seed={seed + 5} amp={1.4} sw={5} />}
		<CutPath pts={ell(28, 32, 0, -34, 14)} fill={look.skin} seed={seed + 1} amp={1.3} sw={5} />
		{look.beard && <CutPath pts={[[-22, -22], [24, -22], [20, 4], [0, 14], [-18, 4]]} fill={look.hair ?? C.ink} seed={seed + 2} amp={1.4} sw={4} />}
		<circle cx={9} cy={-38} r={3.4} fill={C.ink} /><circle cx={-6} cy={-38} r={3.4} fill={C.ink} />
		<path d="M 3 -33 L 9 -26 L 2 -25" stroke={C.ink} strokeWidth={2} fill="none" opacity={0.5} />
		<path d="M 1 -17 Q 8 -14 14 -18" stroke={look.beard ? C.white : C.ink} strokeWidth={2.4} fill="none" opacity={0.7} />
		{look.hair && !look.long && look.hat !== 'morrion' && look.hat !== 'barrete' && look.hat !== 'hood' && <CutPath pts={[[-29, -40], [-24, -62], [0, -70], [24, -62], [29, -40], [18, -52], [-12, -54]]} fill={look.hair} seed={seed + 3} amp={1.2} sw={4} />}
		{look.long && look.hair && <CutPath pts={[[-30, -38], [-26, -64], [0, -72], [26, -64], [30, -38], [14, -54], [-14, -54]]} fill={look.hair} seed={seed + 3} amp={1.2} sw={4} />}
		{look.hat === 'morrion' && (<g><CutPath pts={[[-32, -48], [-24, -76], [0, -84], [24, -76], [32, -48]]} fill="#7D8084" seed={seed + 4} amp={1} sw={4} /><CutPath pts={[[-50, -48], [50, -48], [34, -58], [-34, -58]]} fill="#6B6F73" seed={seed + 6} amp={1} sw={4} /><CutPath pts={[[-3, -84], [3, -84], [2, -96], [-2, -96]]} fill="#6B6F73" seed={seed + 7} amp={0.5} sw={3} /></g>)}
		{look.hat === 'barrete' && <CutPath pts={[[-32, -46], [-26, -72], [0, -80], [24, -72], [34, -46], [10, -52], [-18, -50]]} fill={look.hatColor ?? C.es} seed={seed + 4} amp={1.2} sw={4} />}
		{look.hat === 'hood' && <CutPath pts={[[-36, -30], [-30, -72], [0, -86], [30, -72], [36, -30], [20, -50], [-20, -50]]} fill={look.hatColor ?? C.ink} seed={seed + 4} amp={1.4} sw={4} />}
		{look.hat === 'wide' && <CutPath pts={[[-58, -52], [-26, -58], [-22, -78], [22, -78], [26, -58], [58, -52], [30, -46], [-30, -46]]} fill={look.hatColor ?? C.wood} seed={seed + 4} amp={1.4} sw={4} />}
	</g>
);

export const Puppet: React.FC<{
	x: number; y: number; s?: number; flip?: boolean; look: Look; pose?: PoseName | ((t: number) => Pose);
	startAt?: number; seed?: number; z?: number; speed?: number; hold?: number;
}> = ({x, y, s = 1, flip, look, pose = 'idle', startAt = 0, seed = 1, z, speed = 1, hold}) => {
	const f = useCurrentFrame();
	const step = Math.floor((f - startAt) / 3);
	const t = (hold ?? step * 3) / 30 * speed;
	const p = typeof pose === 'function' ? pose(t) : poses[pose](t);
	const wob = wobbleDeg(seed, f - startAt, 0.5);
	const L = {...look};
	const capeColor = look.cape;
	return (
		<svg width={1} height={1} style={{position: 'absolute', left: x, top: y, overflow: 'visible', filter: SHADOW, zIndex: z}}>
			<g transform={`translate(${(p.dx ?? 0) * (flip ? -1 : 1) * s} 0) scale(${flip ? -s : s} ${s}) rotate(${(p.rot ?? 0) + wob}) translate(0 ${-125 + p.y})`}>
				{capeColor && <CutPath pts={[[-34, -104], [34, -104], [48, 10], [-48, 10]]} fill={capeColor} seed={seed + 40} amp={2} sw={5} />}
				<Arm a={p.aL} look={L} ox={-32} oy={-92} seed={seed * 10 + 1} />
				<Leg a={p.lL} look={L} ox={-13} seed={seed * 10 + 2} />
				<Leg a={p.lR} look={L} ox={13} seed={seed * 10 + 3} />
				<g transform={`rotate(${p.torso} 0 0)`}>
					<CutPath pts={[[-33, -104], [33, -104], [29, 4], [-29, 4]]} fill={look.shirt} seed={seed * 10 + 4} amp={1.6} sw={5} />
					{look.sash && <CutPath pts={[[-31, -10], [31, -10], [30, 4], [-30, 4]]} fill={look.sash} seed={seed * 10 + 5} amp={1} sw={0} outline={null} />}
					{look.collar && <CutPath pts={[[-28, -108], [28, -108], [20, -94], [-20, -94]]} fill={C.white} seed={seed * 10 + 6} amp={1} sw={4} />}
					<g transform={`translate(0 -104) rotate(${p.head})`}><Head look={L} seed={seed * 10 + 7} /></g>
				</g>
				<Arm a={p.aR} look={L} ox={32} oy={-92} seed={seed * 10 + 8} item={look.item} />
			</g>
		</svg>
	);
};
