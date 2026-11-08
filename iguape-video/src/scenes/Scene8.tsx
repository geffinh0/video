import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans, serif} from '../cutout/theme';
import {CutPath, Label, PhotoCard, Piece, Sheet, TornStrip} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell} from '../cutout/noise';
import {Puppet} from '../characters/Puppet';
import {cast} from '../characters/cast';
import {Church, Gold, House, Tree} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {Arrow, BigText, SP, clamp} from './shared';

const Icon: React.FC<{x: number; y: number; at: number; text: string; draw: React.ReactNode}> = ({x, y, at, text, draw}) => (
	<Enter at={at} kind="drop" seed={x}>
		<Sheet x={x - 150} y={y - 125} w={300} h={250} fill={C.parch2} rot={x % 2 ? 2 : -2} seed={x % 33}>
			<svg width={300} height={140} style={{position: 'absolute', overflow: 'visible', top: -10}}>{draw}</svg>
			<div style={{position: 'absolute', left: 8, right: 8, bottom: 10, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 24, lineHeight: 1.1, color: C.ink}}>{text}</div>
		</Sheet>
	</Enter>
);

export const Scene8: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.04}]}>
				{/* foto real x recorte */}
				{f < a(2) && <>
					<Enter at={0} kind="left"><PhotoCard x={150} y={140} w={640} h={440} desc="centro histórico de Iguape (SP)" file="centro-historico-iguape.jpg" rot={-3} /></Enter>
					<Enter at={14} kind="right"><PhotoCard x={150} y={520} w={600} h={300} desc="Igreja Matriz / ruas antigas" file="igreja-matriz-ruas-antigas.jpg" rot={2} seed={4} /></Enter>
					<Enter at={20} kind="drop">
						<Sheet x={900} y={140} w={880} h={680} fill={C.sea2} rot={1} seed={9}>
							<svg width={880} height={680} style={{position: 'absolute', overflow: 'visible'}}><CutPath pts={[[0, 420], [880, 400], [880, 680], [0, 680]]} fill={C.forest2} seed={6} amp={6} sw={5} /></svg>
						</Sheet>
						<Church x={1180} y={700} s={0.7} /><House x={1480} y={720} s={0.8} /><House x={1650} y={724} s={0.65} seed={9} roof={C.ocre} />
					</Enter>
					<Label x={1340} y={210} text="Iguape hoje, em recortes" at={30} until={a(2)} size={36} />
				</>}
				{/* 1537: igreja em Icapara */}
				{f >= a(1) && f < a(2) && <Label x={460} y={110} text="1537 — Icapara" sub="primeira igreja de Nossa Senhora das Neves" at={a(1) + 8} size={46} rot={-2} fill={C.terra} color={C.white} />}
				{/* ouro de aluvião */}
				{f >= a(2) && f < a(3) && <>
					<Enter at={a(2)} kind="up"><TornStrip y={620} h={400} fill={C.forest2} seed={5} /><div style={{position: 'absolute', left: 120, top: 560, width: 1680, height: 150, overflow: 'hidden'}}><svg width={1680} height={150}><rect width={1680} height={150} fill={C.sea2} />{Array.from({length: 12}, (_, i) => <path key={i} d={`M ${(i * 150 + sf * 2) % 1700} ${40 + (i % 3) * 40} q 22 -20 44 0 q 22 20 44 0`} stroke={C.sea} strokeWidth={8} fill="none" strokeLinecap="round" />)}</svg></div></Enter>
					<Enter at={a(2) + 10} kind="drop"><Tree x={260} y={620} s={1} /><Tree x={1650} y={610} s={1.1} seed={9} /></Enter>
					<Puppet x={900} y={780} s={0.95} look={{...cast.marinheiro, item: 'pan', hat: 'wide', hatColor: C.wood}} pose={(t) => ({torso: 14 + Math.sin(t * 5) * 3, head: 10, aL: [-30, -60], aR: [-40 + Math.sin(t * 5) * 22, -50], lL: [0, 20], lR: [0, 20], y: 0})} seed={12} startAt={a(2)} />
					{[0, 1, 2].map((i) => <Enter key={i} at={a(2) + 60 + i * 22} kind="drop"><Gold x={1160 + i * 90} y={760 + (i % 2) * 14} s={2} seed={i + 5} /></Enter>)}
					<Label x={1240} y={250} text="ouro de aluvião" sub="encontrado nos sedimentos de rios e cursos d'água" at={a(2) + 30} size={48} rot={-1} fill={C.gold} />
					<Label x={560} y={210} text="Vale do Ribeira — século XVI" at={a(2) + 10} size={38} rot={2} />
					<Label x={600} y={330} text="mais pessoas chegando" at={a(2) + 100} size={36} rot={-2} />
				</>}
				{/* transferência 1620–1625 */}
				{f >= a(3) && f < a(4) && <>
					<Enter at={a(3)} kind="drop"><Sheet x={160} y={100} w={1000} h={720} fill={C.sea} seed={7}><svg width={1000} height={720} style={{position: 'absolute', overflow: 'visible'}}><CutPath pts={[[0, 0], [1000, 0], [1000, 120], [740, 340], [520, 560], [360, 720], [0, 720]]} fill={C.sand} seed={8} amp={6} sw={5} /><circle cx={720} cy={200} r={16} fill={C.terra} stroke={C.outline} strokeWidth={4} /><circle cx={470} cy={560} r={16} fill={C.pt} stroke={C.outline} strokeWidth={4} /></svg></Sheet></Enter>
					<Label x={600} y={190} text="Icapara" at={a(3) + 14} size={36} />
					<Label x={800} y={700} text="centro histórico atual" at={a(3) + 40} size={36} fill={C.pt} color={C.white} />
					<Arrow x={800} y={300} len={300} rot={118} at={a(3) + 30} />
					<Label x={1500} y={160} text="1620–1625" at={a(3) + 24} size={86} fill={C.terra} color={C.white} rot={3} />
					<Icon x={1440} y={420} at={a(3) + 60} text="dificuldade de conseguir água potável" draw={<g><CutPath pts={[[150, 8], [212, 90], [150, 130], [88, 90]]} fill="#4A94B5" seed={3} amp={2} /></g>} />
					<Icon x={1440} y={660} at={a(3) + 90} text="falta de espaço para expansão" draw={<g><path d="M 80 70 L 220 70 M 100 40 L 70 70 L 100 100 M 200 40 L 230 70 L 200 100" stroke={C.terra} strokeWidth={14} fill="none" strokeLinecap="round" /></g>} />
					<Icon x={1700} y={540} at={a(3) + 120} text="outros problemas de localização" draw={<g><CutPath pts={[[150, 4], [196, 40], [150, 130], [104, 40]]} fill={C.es} seed={4} amp={2} /><circle cx={150} cy={44} r={14} fill={C.parch2} /></g>} />
				</>}
				{/* sobreposição antiga/atual */}
				{f >= a(4) && <>
					<Enter at={a(4)} kind="drop"><Sheet x={140} y={120} w={820} h={600} fill={C.sea2} rot={-1} seed={22}><svg width={820} height={600} style={{position: 'absolute', overflow: 'visible'}}><CutPath pts={[[0, 340], [820, 320], [820, 600], [0, 600]]} fill={C.forest2} seed={6} amp={6} sw={5} /></svg></Sheet><Church x={420} y={640} s={0.62} /><House x={640} y={660} s={0.7} /><House x={800} y={664} s={0.55} seed={9} /></Enter>
					<Enter at={a(4) + 12} kind="right"><PhotoCard x={1000} y={150} w={760} h={520} desc="Igreja Matriz e ruas antigas de Iguape" file="igreja-matriz-ruas-antigas.jpg" rot={2} seed={12} /></Enter>
					<Label x={1380} y={715} text="Iguape antiga + Iguape de hoje" at={a(4) + 30} size={40} rot={-1} />
					<Label x={960} y={810} text="tudo começou numa região que já era palco de disputas" at={a(4) + 60} size={44} rot={1} fill={C.terra} color={C.white} />
				</>}
			</Camera>
		</AbsoluteFill>
	);
};
