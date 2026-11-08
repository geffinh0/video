import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, sans} from '../cutout/theme';
import {Label, Sheet, TornStrip} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {Puppet} from '../characters/Puppet';
import {cast, soldier} from '../characters/cast';
import {Caravel, Church, House} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {BigText, COAST, CoastMap, SP, Walker, clamp} from './shared';
import {Waves} from '../props';

const Node: React.FC<{x: number; at: number; year: string; text: string}> = ({x, at, year, text}) => (
	<Enter at={at} kind="drop" seed={x}>
		<Sheet x={x - 220} y={100} w={440} h={190} fill={C.parch2} rot={x % 2 ? 1.2 : -1.2} seed={x % 40} tape>
			<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: sans, fontWeight: 800, color: C.ink}}>
				<div style={{fontSize: 64, color: C.terra, lineHeight: 1}}>{year}</div><div style={{fontSize: 28}}>{text}</div>
			</div>
		</Sheet>
	</Enter>
);

export const Scene4: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const sail = clamp((sf - a(0)) / Math.max(1, e(2) - a(0)));
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.04}]}>
				{/* linha do tempo + mar */}
				{f < a(3) && <>
					<Node x={380} at={a(0)} year="1530" text="Portugal organiza a expedição" />
					<Node x={960} at={a(1)} year="1531" text="Chegada ao Brasil" />
					<Node x={1540} at={a(2)} year="1532" text="Fundação de São Vicente" />
					<Enter at={a(0) + 6} until={a(3)} kind="up"><div style={{position: 'absolute', left: 140, top: 320, width: 1640, height: 210, overflow: 'hidden', borderRadius: 3, filter: 'drop-shadow(7px 9px 0 rgba(43,38,34,0.27))'}}><Waves y={0} h={230} fill={C.sea} /></div></Enter>
					<Caravel x={260 + sail * 1300} y={480} s={0.33} flag={C.pt} />
					<Caravel x={160 + sail * 1100} y={500} s={0.24} flag={C.pt} seed={4} />
				</>}
				{/* Martim Afonso e a missão */}
				{f < a(2) && <Enter at={a(1)} kind="left"><Puppet x={300} y={860} s={0.9} look={cast.martim} pose={f > a(1) + 30 ? 'point' : 'talk'} seed={2} startAt={a(1)} /></Enter>}
				{f < a(2) && <>
					<Label x={1150} y={640} text="explorar o litoral" at={a(1) + 20} size={40} rot={-2} />
					<Label x={1250} y={730} text="combater atividades consideradas ilegais" at={a(1) + 50} size={40} rot={1.5} />
					<Label x={1200} y={820} text="estabelecer núcleos de ocupação" at={a(1) + 80} size={40} rot={-1} />
				</>}
				{f >= a(0) && f < a(1) && <Enter at={a(0) + 4} kind="left"><Puppet x={300} y={860} s={0.9} look={cast.martim} pose="talk" seed={2} startAt={a(0)} /></Enter>}
				{/* São Vicente montada peça por peça */}
				{f >= a(2) && f < a(3) && <>
					<TornStrip y={640} h={300} fill={C.forest2} seed={7} />
					<Enter at={a(2) + 6} kind="drop"><House x={520} y={810} s={0.85} /></Enter>
					<Enter at={a(2) + 22} kind="drop"><Church x={900} y={800} s={0.62} /></Enter>
					<Enter at={a(2) + 38} kind="drop"><House x={1230} y={810} s={0.85} seed={9} /></Enter>
					<Enter at={a(2) + 54} kind="drop"><House x={1500} y={812} s={0.7} seed={11} roof={C.ocre} /></Enter>
					<Label x={1000} y={600} text="São Vicente" sub="um dos primeiros centros de povoamento português na América" at={a(2) + 70} size={46} />
				</>}
				{/* litoral sul */}
				<CoastMap at={a(3)} until={a(7) + 9999} places={['saoVicente', 'iguape', 'cananeia']} kind="pop" />
				{f >= a(3) && <>
					<Puppet x={COAST.saoVicente[0] - 90} y={COAST.saoVicente[1] + 30} s={0.34} look={cast.martim} pose="idle" seed={5} />
					<Puppet x={COAST.cananeia[0] - 90} y={COAST.cananeia[1] + 30} s={0.34} look={cast.cosme} pose={f >= a(4) + 40 ? 'shake' : 'cross'} seed={6} startAt={a(4)} />
					<Puppet x={COAST.iguape[0] - 90} y={COAST.iguape[1] + 20} s={0.34} look={cast.moschera} pose={f >= a(4) + 40 ? 'shake' : 'cross'} seed={7} startAt={a(4)} />
				</>}
				<Label x={1300} y={690} text="Moschera e Cosme não reconheciam a autoridade" at={a(3) + 20} until={a(4)} size={34} rot={-2} />
				{f >= a(4) && f < a(5) && <Enter at={a(4)} kind="left"><Puppet x={170} y={600} s={0.65} look={cast.martim} pose="point" seed={8} startAt={a(4)} /></Enter>}
				<Label x={170} y={330} text="Deixem o território!" at={a(4) + 12} until={a(5)} size={34} rot={-3} />
				<Label x={1300} y={710} text="Eles não obedeceram." at={a(4) + 50} until={a(5)} fill={C.terra} color={C.white} size={38} rot={2} />
				{/* expedição de Pero de Góis */}
				<Enter at={a(5)} kind="left"><Puppet x={190} y={640} s={0.65} look={cast.pero} pose="point" seed={12} startAt={a(5)} /></Enter>
				<Label x={190} y={370} text="Pero de Góis" sub="expedição militar" at={a(5) + 10} size={34} rot={-2} fill={C.pt} color={C.white} />
				{[0, 1, 2, 3].map((i) => <Walker key={i} from={a(5) + 50 + i * 12} to={e(5) + 90} a={[COAST.saoVicente[0] - 70, COAST.saoVicente[1] + 10 + i * 6]} b={[COAST.iguape[0] - 100, COAST.iguape[1] + 6 + i * 6]} look={soldier(i)} s={0.3} seed={40 + i} />)}
				<Label x={1330} y={600} text="eles conheciam o terreno" at={a(6) + 10} size={44} rot={-2} fill={C.forest} color={C.white} />
			</Camera>
		</AbsoluteFill>
	);
};
