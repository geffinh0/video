import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans} from '../cutout/theme';
import {CutPath, Ink, Label, Piece, Sheet, TornStrip} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell, rect} from '../cutout/noise';
import {Puppet} from '../characters/Puppet';
import {cast, soldier} from '../characters/cast';
import {Book, Canoe, Church, Crate, Fire, House, Smoke} from '../props';
import {IconThumb} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {BigText, Notice, SP, Walker, clamp} from './shared';

const Lens: React.FC<{x: number; y: number}> = ({x, y}) => (
	<Piece x={x} y={y} rot={-20}><CutPath pts={ell(40, 40, 0, 0, 14)} fill="#BFE0E8" seed={3} amp={1} /><CutPath pts={rect(12, 70, -6, 38)} fill={C.wood} seed={4} amp={1} sw={3} /></Piece>
);

export const Scene6: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const burnt = f >= a(2) + 60;
	const burn = clamp((sf - a(5)) / Math.max(1, e(5) - a(5)));
	const village = f < a(4) || f >= a(3) && f < a(4);
	return (
		<AbsoluteFill>
			<Table base="#1A1512" sheet="#C9B58A" sheet2="#9C8A62" />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.04}]} shakeFrom={a(2) + 4} shakeTo={a(2) + 16}>
				{/* vila de São Vicente */}
				{f < a(4) && <>
					<div style={{position: 'absolute', left: 120, top: 120, width: 1680, height: 190, overflow: 'hidden', filter: SHADOW}}><svg width={1680} height={190}><rect width={1680} height={190} fill={C.sea} />{Array.from({length: 10}, (_, i) => <path key={i} d={`M ${(i * 180 + sf * 1.2) % 1700} ${40 + (i % 3) * 50} q 22 -20 44 0 q 22 20 44 0`} stroke={C.sea2} strokeWidth={8} fill="none" strokeLinecap="round" />)}</svg></div>
					<TornStrip y={330} h={620} fill={C.forest2} seed={8} />
					<Enter at={6} kind="drop"><House x={380} y={700} s={0.95} burnt={burnt} /></Enter>
					<Enter at={14} kind="drop"><Church x={820} y={690} s={0.72} /></Enter>
					<Enter at={22} kind="drop"><House x={1230} y={700} s={0.95} seed={8} burnt={burnt} /></Enter>
					<Enter at={30} kind="drop"><House x={1560} y={702} s={0.85} seed={11} roof={C.ocre} burnt={burnt} /></Enter>
					<Label x={400} y={190} text="São Vicente" sub="administração e comércio" at={a(1)} until={a(2)} size={44} />
					{f >= a(0) && f < a(2) && [0, 1, 2].map((i) => <Walker key={i} from={a(1) + 20 + i * 20} to={a(2) + 40} a={[1900 + i * 80, 830]} b={[1250 + i * 90, 830]} look={i === 1 ? cast.indio : cast.espanhol} s={0.55} flip seed={70 + i} during="run" />)}
				</>}
				{/* invasão: saque, prisioneiros, destruição */}
				{f >= a(2) && f < a(3) && <>
					<Enter at={a(2) + 20} kind="drop"><Crate x={760} y={880} s={1} open /></Enter>
					<Enter at={a(2) + 30} kind="drop"><Fire x={380} y={620} s={0.9} /></Enter>
					<Enter at={a(2) + 60} kind="drop"><Fire x={1560} y={640} s={0.9} /></Enter>
					<Enter at={a(2) + 40} kind="drop"><Sheet x={920} y={620} w={180} h={250} fill="#6B6358" rot={-2} seed={5}><div style={{position: 'absolute', inset: 14, background: `repeating-linear-gradient(90deg, ${C.ink} 0 8px, transparent 8px 28px)`, opacity: 0.7}} /></Sheet><Puppet x={1010} y={860} s={0.5} look={cast.marinheiro} pose="cheer" seed={9} startAt={a(2) + 70} /></Enter>
					<Label x={960} y={410} text="A vila sofreu grandes perdas humanas e materiais." at={a(2) + 70} size={40} fill={C.terra} color={C.white} rot={-1} />
				</>}
				{/* incêndio do cartório */}
				{f >= a(3) && f < a(4) && <>
					<TornStrip y={330} h={620} fill={C.forest2} seed={8} />
					<House x={620} y={760} s={1.5} burnt wall={C.parch2} />
					<Fire x={620} y={540} s={1.4} />
					<Smoke x={620} y={430} n={6} />
					<Label x={620} y={820} text="Cartório" at={a(3) + 6} size={44} />
					<Enter at={a(3) + 30} kind="drop"><Book x={1250} y={720} s={1.1} /></Enter>
					<Label x={1250} y={760} text="Livro do Tombo" sub="registros oficiais" at={a(3) + 40} size={48} fill={C.terra} color={C.white} rot={2} />
				</>}
				{/* sem computadores */}
				{f >= a(4) && f < a(5) && <>
					<Enter at={a(4)} kind="drop"><Sheet x={200} y={120} w={1520} h={640} fill={C.parch2} rot={-0.8} seed={31} tape /></Enter>
					<BigText x={960} y={260} text="Sem computadores. Sem bancos de dados." at={a(4) + 6} size={64} />
					{[0, 1, 2, 3, 4].map((i) => <Enter key={i} at={a(4) + 18 + i * 8} kind="drop"><Book x={330 + i * 120} y={560} s={0.46} fill={[C.terra, C.forest, C.pt, C.wood2, C.es][i]} seed={i + 2} /></Enter>)}
					{[['propriedades', 340], ['concessões de terras', 700], ['decisões administrativas', 1100], ['acontecimentos', 1490]].map(([t, x], i) => <Label key={i} x={x as number} y={690 + (i % 2) * 30} text={t as string} at={a(4) + 50 + i * 20} size={32} rot={i % 2 ? 2 : -2} />)}
					<Enter at={a(4) + 30} kind="drop"><Puppet x={1500} y={560} s={0.6} look={cast.pesquisadora} pose="read" seed={5} startAt={a(4)} /></Enter>
				</>}
				{/* livro queima: lacunas */}
				{f >= a(5) && f < a(6) && <>
					<Sheet x={560} y={110} w={800} h={650} fill="#3A2F27" rot={0} seed={41} />
					<Book x={960} y={700} s={2.6} open lines={Math.max(1, Math.round(7 * (1 - burn)))} />
					{Array.from({length: Math.round(burn * 7)}, (_, i) => <Piece key={i} x={780 + (i * 97) % 400} y={420 + ((i * 61) % 240)} shadow={false}><CutPath pts={ell(46 + i * 6, 38 + i * 4, 0, 0, 10)} fill="#3A2F27" seed={i + 5} amp={4} outline={null} /></Piece>)}
					<Fire x={800} y={620} s={1.4} /><Fire x={1120} y={600} s={1.2} seed={4} />
					<Label x={960} y={90} text="lacunas nos registros" at={a(5) + 60} size={50} fill={C.terra} color={C.white} rot={-1} />
				</>}
				{/* pesquisadores */}
				{f >= a(6) && <>
					<Enter at={a(6)} kind="drop"><Sheet x={260} y={420} w={1400} h={140} fill={C.wood2} seed={51} /></Enter>
					{[0, 1, 2, 3].map((i) => <Enter key={i} at={a(6) + 8 + i * 8} kind="drop"><Sheet x={420 + i * 280} y={380} w={150} h={70} fill={C.parch2} rot={i * 4 - 6} seed={60 + i} /></Enter>)}
					<Enter at={a(6) + 20} kind="left"><Puppet x={540} y={860} s={0.8} look={cast.pesquisador} pose="read" seed={6} startAt={a(6)} /></Enter>
					<Enter at={a(6) + 26} kind="right"><Puppet x={1380} y={860} s={0.8} look={cast.pesquisadora} pose="point" seed={7} flip startAt={a(6)} /></Enter>
					<Enter at={a(6) + 40} kind="pop"><Lens x={960} y={330} /></Enter>
					<Label x={960} y={160} text="lacunas documentais" at={a(6) + 30} size={64} fill={C.terra} color={C.white} />
					<Label x={960} y={260} text="por isso alguns detalhes ainda são discutidos" at={a(6) + 70} size={42} rot={1} />
				</>}
			</Camera>
			<AbsoluteFill style={{background: 'rgba(20,10,5,0.2)', pointerEvents: 'none'}} />
		</AbsoluteFill>
	);
};
