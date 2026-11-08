import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans} from '../cutout/theme';
import {Label, Sheet} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {Puppet} from '../characters/Puppet';
import {cast} from '../characters/cast';
import {Caravel} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {BigText, COAST, CoastMap, Notice, SP, clamp} from './shared';

export const Scene7: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const r0 = clamp((sf - a(0)) / Math.max(1, e(0) - a(0)));
	const r1 = clamp((sf - a(1) - 20) / Math.max(1, e(1) - a(1) - 20));
	const from = COAST.iguape, to = COAST.santaCatarina;
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.05}]}>
				<CoastMap at={0} places={['saoVicente', 'iguape', 'cananeia', 'santaCatarina']} kind="drop" />
				<svg width={1920} height={1080} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
					{f >= a(0) && <path d={`M ${from[0] + 30} ${from[1] + 30} Q ${from[0] + 80} ${(from[1] + to[1]) / 2 + 40} ${to[0] + 40} ${to[1] - 10}`} stroke={C.terra} strokeWidth={9} strokeDasharray="18 14" fill="none" strokeLinecap="round" />}
					{f >= a(1) + 10 && <path d={`M ${to[0] + 10} ${to[1] + 30} Q ${to[0] - 120} ${to[1] + 80} ${MAPEND[0]} ${MAPEND[1]}`} stroke={C.es} strokeWidth={9} strokeDasharray="18 14" fill="none" strokeLinecap="round" />}
				</svg>
				{f >= a(0) && f < a(1) && <Caravel x={from[0] + 40 + r0 * (to[0] - from[0]) * 0.9} y={from[1] + 40 + r0 * (to[1] - from[1]) * 0.9 - 30} s={0.16} flip={false} />}
				<Label x={to[0] + 250} y={to[1] - 30} text="onde hoje está Florianópolis" at={a(0) + 20} until={a(2)} size={34} rot={-2} />
				{f >= a(1) && f < a(2) + 40 && <Caravel x={to[0] - r1 * 160} y={to[1] + 20 + r1 * 40} s={0.16} flip flag={C.es} />}
				<Label x={560} y={800} text="Rio da Prata" at={a(1) + 30} until={a(3)} size={38} fill={C.es} color={C.white} rot={2} />
				<Label x={1240} y={430} text="Moschera" at={a(1) + 8} until={a(2)} size={40} fill={C.es} color={C.white} rot={-2} />
				<Notice x={960} y={120} w={1000} text="Alguns relatos relacionam Moschera a Buenos Aires, mas ele não é o fundador oficial da cidade." at={a(1) + 50} until={a(2)} />
				{/* Cosme */}
				{f >= a(2) && <>
					<div style={{position: 'absolute', inset: 0, opacity: 0.55}}><Puppet x={COAST.cananeia[0] - 110} y={COAST.cananeia[1] + 20} s={0.4} look={cast.cosme} pose="idle" seed={9} /></div>
					<Label x={820} y={170} text="Cosme Fernandes" sub="continuou associado a Cananeia" at={a(2) + 8} until={a(3)} size={38} fill={C.pt} color={C.white} />
					<Label x={820} y={290} text="registros limitados sobre seus últimos anos" at={a(2) + 40} until={a(3)} size={34} rot={2} />
					{[0, 1, 2].map((i) => <Enter key={i} at={a(2) + 60 + i * 10} kind="drop"><Sheet x={1250 + i * 70} y={440 + i * 12} w={110} h={130} fill={C.parch2} rot={i * 6 - 6} seed={80 + i}>{null}</Sheet></Enter>)}
				</>}
				<Label x={960} y={110} text="o domínio português no litoral ainda não estava consolidado" at={a(3) + 20} size={42} rot={-1} fill={C.pt} color={C.white} />
			</Camera>
		</AbsoluteFill>
	);
};
const MAPEND: [number, number] = [380, 900];
