import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans, serif} from '../cutout/theme';
import {CutPath, Label, Piece, Sheet} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell, rect} from '../cutout/noise';
import {Book, Caravel} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {CoastMap, COAST, SP, clamp} from './shared';

const Tab: React.FC<{n: number; at: number; until?: number; fill: string}> = ({n, at, until, fill}) => (
	<Enter at={at} until={until} kind="left" seed={n}>
		<Sheet x={80} y={120 + (n - 1) * 130} w={150} h={110} fill={fill} seed={n + 3}>
			<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: serif, fontWeight: 900, fontSize: 80, color: C.white}}>{n}</div>
		</Sheet>
	</Enter>
);

export const Scene9: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const tear = clamp((sf - a(1) - 80) / 20);
	const nodes: [number, number][] = [[620, 240], [900, 200], [1200, 280], [760, 470], [1080, 500], [1360, 470]];
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.04}]}>
				<Label x={960} y={440} text="Por que estudar a Guerra de Iguape?" at={0} until={a(1)} size={70} />
				{f >= a(1) && <Tab n={1} at={a(1)} fill={C.terra} />}
				{f >= a(2) && <Tab n={2} at={a(2)} fill={C.pt} />}
				{f >= a(3) && <Tab n={3} at={a(3)} fill={C.forest} />}
				{/* 1: visão simplificada -> teia */}
				{f >= a(1) && f < a(2) && <>
					<Enter at={a(1) + 6} kind="drop"><Sheet x={330} y={130} w={1400} h={680} fill={C.parch2} rot={-0.6} seed={9} /></Enter>
					<div style={{position: 'absolute', left: 330, top: 130, width: 1400, height: 680, clipPath: `polygon(0 0, ${100 - tear * 100}% 0, ${96 - tear * 100}% 30%, ${101 - tear * 100}% 60%, ${97 - tear * 100}% 100%, 0 100%)`}}>
						<div style={{position: 'absolute', inset: 0, background: C.white}} />
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: 60, fontFamily: sans, fontWeight: 800, fontSize: 56, color: C.ink}}>“os portugueses chegaram, ocuparam e construíram vilas”</div>
					</div>
					{tear > 0.3 && <>
						<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
							{[[0, 1], [1, 2], [0, 3], [1, 3], [1, 4], [2, 4], [2, 5], [3, 4], [4, 5]].map(([i, j], k) => <path key={k} d={`M ${nodes[i][0]} ${nodes[i][1]} L ${nodes[j][0]} ${nodes[j][1]}`} stroke={C.ink} strokeWidth={6} strokeDasharray="14 10" opacity={0.6} />)}
						</svg>
						{[['europeus', C.pt], ['indígenas', C.ind], ['interesses comerciais', C.ocre], ['conflitos políticos', C.es], ['alianças', C.forest], ['disputas', C.terra]].map(([t, c], i) => <Label key={i} x={nodes[i][0]} y={nodes[i][1]} text={t as string} at={a(1) + 100 + i * 14} size={38} fill={c as string} color={C.white} rot={i % 2 ? 2 : -2} />)}
					</>}
				</>}
				{/* 2: Tordesilhas rachada */}
				{f >= a(2) && f < a(3) && <>
					<Enter at={a(2) + 6} kind="drop"><Sheet x={330} y={130} w={1400} h={680} fill={C.sea} rot={0.6} seed={12} /></Enter>
					<Enter at={a(2) + 14} kind="drop"><div style={{position: 'absolute', left: 1010, top: 130, width: 14, height: 680, background: `repeating-linear-gradient(${C.white} 0 24px, transparent 24px 38px)`, transform: 'rotate(2deg)'}} /></Enter>
					<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}><path d="M 1010 330 l 30 40 l -26 36 l 34 50 M 1000 560 l -34 30 l 30 40" stroke={C.ink} strokeWidth={6} fill="none" /></svg>
					<Label x={700} y={250} text="Tordesilhas" sub="a linha imaginária" at={a(2) + 30} size={50} />
					<Enter at={a(2) + 50} kind="left"><Caravel x={560} y={600} s={0.3} flag={C.es} /></Enter>
					<Enter at={a(2) + 62} kind="right"><Caravel x={1500} y={600} s={0.3} flip flag={C.pt} /></Enter>
					<Label x={1290} y={300} text="ocupações e conflitos nascendo ao redor" at={a(2) + 90} size={38} rot={-2} fill={C.terra} color={C.white} />
					<Label x={960} y={740} text="regiões que nem estavam devidamente mapeadas" at={a(2) + 120} size={36} rot={1} />
				</>}
				{/* 3: litoral e Vale do Ribeira */}
				{f >= a(3) && f < a(4) && <>
					<CoastMap at={a(3) + 6} until={a(4)} places={['iguape', 'saoVicente', 'cananeia']} kind="drop" />
					<Enter at={a(3) + 40} kind="pop"><svg width={1} height={1} style={{position: 'absolute', left: COAST.iguape[0], top: COAST.iguape[1], overflow: 'visible'}}><circle r={46} fill="none" stroke={C.gold} strokeWidth={10} strokeDasharray="14 8" /></svg></Enter>
					<Label x={1000} y={640} text="Iguape" sub="na formação do litoral paulista" at={a(3) + 50} size={46} fill={C.gold} />
					<Label x={640} y={260} text="Vale do Ribeira" at={a(3) + 80} size={44} fill={C.forest} color={C.white} />
				</>}
				{/* fechamento: frase atribuída + pilha de livros */}
				{f >= a(4) && <>
					<Enter at={a(4)} kind="drop"><Sheet x={260} y={110} w={1400} h={300} fill={C.parch2} rot={-1} seed={31} tape>
						<div style={{position: 'absolute', inset: 0, padding: '0 70px', display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: serif, fontWeight: 900, fontSize: 60, lineHeight: 1.15, color: C.ink}}>“um dos primeiros conflitos armados entre europeus em território americano”</div>
					</Sheet></Enter>
					<Label x={960} y={470} text="segundo alguns estudos de história militar" at={a(4) + 40} size={44} fill={C.es} color={C.white} rot={1} />
					<Enter at={a(4) + 70} kind="drop"><Book x={640} y={850} s={0.8} fill={C.pt} /><Book x={860} y={850} s={0.8} fill={C.forest} seed={3} /><Book x={1080} y={850} s={0.8} fill={C.wood2} seed={4} /><Book x={750} y={690} s={0.8} fill={C.terra} seed={5} rot={-4} /></Enter>
					<Enter at={a(4) + 100} kind="pop"><Piece x={1380} y={820} rot={4}><CutPath pts={rect(190, 230, -95, -230)} fill={C.parch2} seed={9} amp={2} /><path d="M -60 -170 L 60 -170 M -60 -130 L 60 -130 M -60 -90 L 20 -90" stroke={C.ink} strokeWidth={6} opacity={0.5} /></Piece></Enter>
				</>}
			</Camera>
		</AbsoluteFill>
	);
};
