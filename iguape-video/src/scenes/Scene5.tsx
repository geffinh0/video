import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C} from '../cutout/theme';
import {CutPath, Label, Piece, TornStrip} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell} from '../cutout/noise';
import {Puppet} from '../characters/Puppet';
import {cast, soldier} from '../characters/cast';
import {Cannon, Crate, FrenchShip, Mangrove, Smoke, Tree} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {Arrow, BigText, Notice, SP, Walker, clamp} from './shared';
import {Waves} from '../props';

const Arrowflight: React.FC<{from: number; to: number; y: number; x0: number; x1: number; period?: number}> = ({from, to, y, x0, x1, period = 36}) => {
	const f = useCurrentFrame();
	if (f < from || f >= to) return null;
	const sf = st(f - from, 3);
	return <>{[0, 1, 2].map((i) => {
		const p = (((sf + i * (period / 3)) % period) / period);
		return <Piece key={i} x={x0 + (x1 - x0) * p} y={y + Math.sin(p * Math.PI) * -70 + i * 26} rot={(x1 > x0 ? 1 : -1) * 10 + (p - 0.5) * 40} shadow={false}><CutPath pts={[[-34, -2], [30, -2], [30, 2], [-34, 2]]} fill={C.wood} seed={i} amp={0.4} sw={2} /><CutPath pts={[[30, -7], [46, 0], [30, 7]]} fill={C.stone} seed={i + 4} amp={0.4} sw={2} /></Piece>;
	})}</>;
};

export const Scene5: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const battle = f >= a(7) && f < a(9);
	const gap = Math.round((e(2) - a(2)) / 4.4);
	return (
		<AbsoluteFill>
			<Table base="#1A1512" sheet="#CBB88F" sheet2="#9C8A62" />
			<Camera keys={[{f: 0, s: 1}, {f: a(7), s: 1}, {f: a(7) + 40, s: 1.1, x: -120, y: 20}, {f: a(9), s: 1.1, x: -120, y: 20}, {f: a(9) + 30, s: 1}]} shakeFrom={a(7)} shakeTo={a(7) + 18}>
				<BigText x={960} y={470} text="A emboscada de Iguape" at={0} until={a(1)} size={110} color={C.terra} />
				{/* navio francês capturado */}
				{f >= a(1) && f < a(3) && <>
					<div style={{position: 'absolute', left: 120, top: 100, width: 1680, height: 300, overflow: 'hidden', filter: 'drop-shadow(7px 9px 0 rgba(43,38,34,0.27))'}}><Waves y={0} h={300} fill={C.sea} /></div>
					<Enter at={a(1)} kind="right"><FrenchShip x={900} y={330} s={0.5} /></Enter>
					<Label x={1500} y={190} text="navio francês em Cananeia" at={a(1) + 20} until={a(2)} size={36} rot={2} />
					<TornStrip y={430} h={500} fill={C.sand} seed={3} />
				</>}
				{f >= a(1) && f < a(2) && <>
					<Enter at={a(1) + 16} kind="left"><Puppet x={520} y={780} s={0.75} look={cast.moschera} pose="point" seed={2} startAt={a(1)} /></Enter>
					<Enter at={a(1) + 24} kind="left"><Puppet x={380} y={790} s={0.72} look={cast.guia} pose="idle" seed={3} /></Enter>
					<Enter at={a(1) + 40} kind="drop"><Crate x={900} y={800} s={1.3} open /></Enter>
					<Enter at={a(1) + 54} kind="drop"><Crate x={1120} y={800} s={1.3} open seed={9} /></Enter>
					<Label x={1000} y={610} text="armamentos e peças de artilharia" at={a(1) + 60} size={40} rot={-1} />
				</>}
				{/* contador de canhões */}
				{f >= a(2) && f < a(3) + 40 && <>
					<TornStrip y={470} h={500} fill={C.sand} seed={4} />
					{[0, 1, 2, 3].map((i) => (
						<React.Fragment key={i}>
							<Enter at={a(2) + i * gap} kind="drop" seed={i}><Cannon x={430 + i * 330} y={770} s={0.95} /></Enter>
							<Label x={430 + i * 330} y={620} text={String(i + 1)} at={a(2) + i * gap + 10} size={86} fill={C.terra} color={C.white} />
						</React.Fragment>
					))}
					<Label x={960} y={160} text="quatro peças de artilharia" at={a(2) + 10} size={56} />
				</>}
				{/* trincheira e mangue */}
				{f >= a(3) && <>
					<TornStrip y={400} h={600} fill={C.forest2} seed={9} />
					<TornStrip y={470} h={520} fill="#BFA877" seed={11} />
					{[0, 1, 2, 3, 4, 5, 6].map((i) => <Enter key={i} at={a(3) + 4 + i * 6} kind="drop"><Piece x={250 + i * 90} y={640 + (i % 2) * 8} shadow><CutPath pts={ell(46, 24, 0, 0, 10)} fill={i % 2 ? C.wood2 : C.sand} seed={i} amp={2} /></Piece></Enter>)}
					<Label x={430} y={560} text="entrincheiramento de Iguape" at={a(3) + 20} until={a(4) + 60} size={38} rot={-2} />
				</>}
				{f >= a(4) && <>
					{[[140, 470, 0.75], [420, 480, 0.8], [700, 465, 0.7], [1000, 480, 0.85], [1300, 470, 0.75], [1600, 480, 0.85], [1840, 470, 0.7]].map(([x, y, s], i) => <Enter key={i} at={a(4) + i * 6} kind="drop"><Mangrove x={x} y={y} s={s} seed={i + 3} /></Enter>)}
					<Label x={1100} y={190} text="manguezais • canais • áreas alagadas • caminhos estreitos" at={a(4) + 20} until={a(5)} size={38} rot={-1} />
				</>}
				{/* defensores */}
				{f >= a(3) && <>
					<Enter at={a(3) + 10} kind="left"><Puppet x={330} y={830} s={0.7} look={cast.moschera} pose={battle ? 'point' : 'idle'} seed={4} /></Enter>
					<Enter at={a(3) + 16} kind="drop"><Cannon x={560} y={840} s={0.8} flip={false} fire={battle ? 1 : 0} /></Enter>
					<Enter at={a(3) + 20} kind="drop"><Cannon x={700} y={845} s={0.8} fire={battle ? 1 : 0} seed={9} /></Enter>
				</>}
				{f >= a(5) && <>
					{[0, 1, 2].map((i) => <Enter key={i} at={a(5) + i * 14} kind="drop"><Puppet x={870 + i * 170} y={590 + (i % 2) * 14} s={0.5} look={cast.indio} pose={battle ? 'bow' : 'idle'} seed={20 + i} flip /></Enter>)}
					<Label x={1250} y={330} text="indígenas flecheiros" sub="identificados em alguns relatos como carijós" at={a(5) + 10} until={a(6)} size={40} rot={-2} fill={C.ind} />
				</>}
				{/* expedição portuguesa */}
				{f >= a(6) && f < a(8) + 20 && Array.from({length: 7}, (_, i) => <Walker key={i} from={a(6) + i * 6} to={a(7) + 20} a={[1990 + i * 60, 830]} b={[1130 + i * 60, 830]} look={i === 0 ? cast.pero : soldier(i)} s={0.62} flip seed={50 + i} during="walk" after={battle ? 'aim' : 'walk'} />)}
				<Label x={1500} y={260} text="≈ 80 homens (estimativa)" sub="expedição de Pero de Góis, rumo a Icapara" at={a(6) + 20} until={a(7)} size={42} fill={C.pt} color={C.white} rot={2} />
				{/* combate */}
				<Arrowflight from={a(7)} to={a(9)} y={600} x0={900} x1={1500} />
				{battle && <><Smoke x={620} y={790} n={5} /><Smoke x={760} y={795} n={5} seed={3} /></>}
				{f >= a(8) && <>
					{[0, 1, 2, 3].map((i) => <Puppet key={i} x={1330 + i * 120} y={770} s={0.62} flip look={i === 0 ? cast.pero : soldier(i)} pose="fall" startAt={a(8) + 18 + i * 14} seed={60 + i} />)}
					<Label x={1300} y={420} text="arcabuz: arma de fogo usada na época" at={a(8) + 20} until={a(9)} size={38} rot={-2} />
				</>}
				<Label x={760} y={200} text="Vitória dos defensores" at={a(9) - 20} size={54} fill={C.forest} color={C.white} rot={-2} />
				<Arrow x={900} y={470} len={600} at={a(9) + 10} />
				<Label x={1560} y={380} text="São Vicente" at={a(9) + 26} size={64} fill={C.terra} color={C.white} rot={3} />
			</Camera>
			<AbsoluteFill style={{background: 'rgba(20,10,5,0.22)', pointerEvents: 'none'}} />
		</AbsoluteFill>
	);
};
