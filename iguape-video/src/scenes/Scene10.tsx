import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans, serif} from '../cutout/theme';
import {CutPath, Label, PhotoCard, Sheet, TornStrip} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {Puppet} from '../characters/Puppet';
import {cast} from '../characters/cast';
import {Church, Cloud, House, IconBell, IconBubble, IconShare, IconThumb, Sun, Tree} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {SP, clamp} from './shared';

const SOURCES: [string, string][] = [
	['Câmara Municipal de Iguape — História do município', 'iguape.sp.leg.br'],
	['Exército Brasileiro — O primeiro conflito entre europeus na América: a Guerra de Iguape', 'eblog.eb.mil.br'],
	['FUNAG — História da Política Exterior do Brasil', 'funag.gov.br'],
	['USP — Pesquisa acadêmica sobre a formação histórica da região', 'teses.usp.br'],
	['Câmara Municipal de Ilha Comprida — 480 anos de Iguape', 'ilhacomprida.sp.leg.br'],
];

export const Scene10: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const end = f >= sc.narrEnd + 20;
	if (end) {
		return (
			<AbsoluteFill>
				<Table base="#16120F" sheet="#3A2F27" sheet2="#2B241F" />
				<Enter at={sc.narrEnd + 20} kind="drop"><div style={{position: 'absolute', left: 100, top: 70, fontFamily: serif, fontWeight: 900, fontSize: 84, color: C.parch, filter: SHADOW}}>Fontes e referências</div></Enter>
				{SOURCES.map(([t, u], i) => (
					<Enter key={i} at={sc.narrEnd + 34 + i * 12} kind="left" seed={i + 2}>
						<Sheet x={100} y={200 + i * 150} w={1050} h={128} fill={C.parch2} rot={i % 2 ? 0.6 : -0.6} seed={i + 60}>
							<div style={{position: 'absolute', inset: 0, padding: '0 28px', display: 'flex', flexDirection: 'column', justifyContent: 'center', fontFamily: sans, color: C.ink}}>
								<div style={{fontWeight: 800, fontSize: 28, lineHeight: 1.15}}>{t}</div>
								<div style={{fontWeight: 700, fontSize: 24, color: C.terra, marginTop: 4}}>{u}</div>
							</div>
						</Sheet>
					</Enter>
				))}
				{[0, 1].map((i) => (
					<Enter key={i} at={sc.narrEnd + 50 + i * 16} kind="right" seed={i + 9}>
						<Sheet x={1260} y={230 + i * 330} w={560} h={290} fill="rgba(234,217,181,0.18)" rot={i ? 1 : -1} seed={70 + i}>
							<div style={{position: 'absolute', inset: 14, border: `4px dashed ${C.parch}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: sans, fontWeight: 800, fontSize: 32, color: C.parch, opacity: 0.8, textAlign: 'center'}}>vídeo recomendado</div>
						</Sheet>
					</Enter>
				))}
			</AbsoluteFill>
		);
	}
	const sunY = 430 + clamp((sf - 0) / Math.max(1, e(1))) * 80;
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{background: '#F2B544'}} />
			<AbsoluteFill style={{background: 'linear-gradient(#C9573A 0%, #E98A3C 55%, #F2C34C 100%)'}} />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.05}]}>
				<Sun x={960} y={sunY} s={1.15} />
				<Cloud x={380} y={230} s={1.4} fill="#F7D9A8" /><Cloud x={1500} y={170} s={1.2} fill="#F7D9A8" seed={4} />
				<TornStrip y={560} h={300} fill={C.sea} seed={4} amp={10} />
				<TornStrip y={700} h={420} fill={C.forest} seed={6} amp={22} />
				<Church x={1330} y={760} s={0.8} /><House x={1100} y={770} s={0.7} /><House x={1560} y={772} s={0.6} seed={9} /><Tree x={420} y={780} s={1.1} /><Tree x={250} y={790} s={0.9} seed={9} />
				{f < a(1) && <Enter at={30} kind="left"><PhotoCard x={80} y={120} w={520} h={340} desc="pôr do sol em Iguape (SP)" file="por-do-sol-iguape.jpg" rot={-4} /></Enter>}
				{f < a(1) && ['moschera', 'cosme', 'martim', 'pero', 'indio', 'guia'].map((k, i) => <Enter key={k} at={a(0) + 30 + i * 12} kind="drop"><Puppet x={420 + i * 220} y={895} s={0.6} look={cast[k]} pose={i === 4 || i === 5 ? 'idle' : 'talk'} seed={i + 2} flip={i > 2} startAt={a(0)} /></Enter>)}
				{f >= a(1) && f < a(2) && <>
					<Enter at={a(1)} kind="pop"><div style={{position: 'absolute', left: 260, top: 130, width: 1400, height: 500, filter: SHADOW}}><svg width={1400} height={500} style={{overflow: 'visible', position: 'absolute'}}><CutPath pts={[[0, 0], [1400, 0], [1400, 400], [380, 400], [200, 500], [240, 400], [0, 400]]} fill={C.parch2} seed={7} amp={4} /></svg><div style={{position: 'absolute', left: 0, top: 0, width: 1400, height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 80px', fontFamily: serif, fontWeight: 900, fontSize: 82, lineHeight: 1.1, color: C.ink}}>Já conhecia a Guerra de Iguape?</div></div></Enter>
				</>}
				{f >= a(2) && f < a(3) && [[IconThumb, 'curta', 420], [IconBubble, 'comente', 800], [IconBell, 'inscreva-se', 1180], [IconShare, 'compartilhe', 1530]].map(([Ic, t, x], i) => {
					const I = Ic as typeof IconThumb;
					const pulse = 1 + (f > a(2) + 40 + i * 12 ? Math.abs(Math.sin(sf / 8 + i)) * 0.08 : 0);
					return (
						<React.Fragment key={i}>
							<Enter at={a(2) + 10 + i * 14} kind="drop" seed={i}><I x={x as number} y={420} s={1.3 * pulse} /></Enter>
							<Label x={x as number} y={520} text={t as string} at={a(2) + 22 + i * 14} size={46} rot={i % 2 ? 2 : -2} />
						</React.Fragment>
					);
				})}
				{f >= a(3) && f < a(4) && <>
					<Enter at={a(3)} kind="drop"><Puppet x={960} y={880} s={0.9} look={cast.martim} pose="cheer" seed={3} startAt={a(3)} /></Enter>
					<Label x={960} y={170} text="história pode ser interessante, surpreendente" sub="e cheia de acontecimentos que merecem ser conhecidos" at={a(3) + 10} size={52} rot={-1} />
				</>}
				{f >= a(4) && <>
					<Enter at={a(4)} kind="drop"><Puppet x={960} y={900} s={0.95} look={cast.moschera} pose="cheer" seed={3} startAt={a(4)} /></Enter>
					<Label x={960} y={190} text="Até o próximo vídeo!" at={a(4) + 8} size={88} fill={C.terra} color={C.white} rot={-2} />
				</>}
			</Camera>
		</AbsoluteFill>
	);
};
