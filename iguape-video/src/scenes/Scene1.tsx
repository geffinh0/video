import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans, serif} from '../cutout/theme';
import {Label, PhotoCard, Sheet} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {Puppet} from '../characters/Puppet';
import {cast, soldier} from '../characters/cast';
import {Cannon, House, Tree, Book, Fire, Smoke, Caravel} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {BigText, COAST, CoastMap, SP, Walker, WorldMap, clamp} from './shared';

const Card: React.FC<{i: number; at: number; until: number; title: string; children: React.ReactNode}> = ({i, at, until, title, children}) => (
	<Enter at={at} until={until} kind="drop" seed={20 + i}>
		<Sheet x={90 + i * 358} y={200} w={330} h={470} rot={(i % 2 ? 1.6 : -1.6)} seed={40 + i} tape>
			{children}
			<div style={{position: 'absolute', left: 0, right: 0, bottom: 18, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 31, color: C.ink}}>{title}</div>
		</Sheet>
	</Enter>
);

export const Scene1: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const dark = f < a(1);
	const reveal = clamp((st(f, 2) - 4) / 26);
	const gap = Math.round((e(1) - a(1)) / 5.4);
	const foldEnd = a(2) + Math.round((e(2) - a(2)) * 0.45);
	const fold = clamp((st(f) - foldEnd) / 9);
	return (
		<AbsoluteFill>
			{dark ? <Table base="#16120F" sheet="#3A2F27" sheet2="#2B241F" /> : <Table />}
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.05}]}>
				{/* título */}
				<Enter at={0} until={a(1)} kind="pop" seed={2}>
					<div style={{position: 'absolute', left: 210, top: 150, width: 1500, height: 330, filter: SHADOW, clipPath: `polygon(0 0, ${reveal * 104}% 0, ${reveal * 98}% 22%, ${reveal * 104}% 45%, ${reveal * 99}% 70%, ${reveal * 104}% 100%, 0 100%)`}}>
						<Sheet x={0} y={0} w={1500} h={330} fill={C.parch2} seed={5} amp={5}>
							<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontFamily: serif, fontWeight: 900, fontSize: 124, color: C.ink, letterSpacing: 2, whiteSpace: 'nowrap'}}>
								A GUERRA DE IGUAPE
								<div style={{fontFamily: sans, fontWeight: 800, fontSize: 58, color: C.terra, letterSpacing: 2}}>≈ 1534–1536</div>
							</div>
						</Sheet>
					</div>
				</Enter>
				<Enter at={12} until={a(1)} kind="left"><Puppet x={470} y={820} s={0.85} look={soldier(2)} pose="talk" seed={3} /></Enter>
				<Enter at={20} until={a(1)} kind="drop"><Puppet x={960} y={820} s={0.85} look={cast.espanhol} pose="idle" seed={4} flip /></Enter>
				<Enter at={28} until={a(1)} kind="right"><Puppet x={1450} y={820} s={0.85} look={cast.indio} pose="idle" seed={5} flip /></Enter>
				<Label x={470} y={850} text="Portugueses" at={36} until={a(1)} fill={C.pt} color={C.white} size={36} />
				<Label x={960} y={850} text="Espanhóis" at={42} until={a(1)} fill={C.es} color={C.white} size={36} />
				<Label x={1450} y={850} text="Povos indígenas" at={48} until={a(1)} fill={C.ind} color={C.ink} size={36} />

				{/* cartas: canhões, armas de fogo, emboscadas, ataques, documentos */}
				<Card i={0} at={a(1)} until={a(2)} title="Canhões"><Cannon x={130} y={330} s={0.95} fire={1} /></Card>
				<Card i={1} at={a(1) + gap} until={a(2)} title="Armas de fogo"><Puppet x={150} y={360} s={0.75} look={soldier(1)} pose="shoot" seed={9} /></Card>
				<Card i={2} at={a(1) + gap * 2} until={a(2)} title="Emboscadas"><Tree x={90} y={350} s={0.8} /><Tree x={250} y={350} s={0.7} seed={9} /><Puppet x={165} y={340} s={0.5} look={cast.guia} pose="bow" seed={11} /></Card>
				<Card i={3} at={a(1) + gap * 3} until={a(2)} title="Povoados atacados"><House x={165} y={350} s={1.1} burnt /><Fire x={165} y={270} s={0.9} /></Card>
				<Card i={4} at={a(1) + gap * 4} until={a(2)} title="Documentos queimados"><Book x={165} y={360} s={0.85} open /><Fire x={165} y={300} s={0.8} /></Card>

				{/* foto real -> mapa */}
				{f >= a(2) && f < foldEnd + 10 && (
					<div style={{position: 'absolute', inset: 0, transform: `scaleX(${1 - fold})`, transformOrigin: '50% 50%'}}>
						<Enter at={a(2)} kind="drop"><PhotoCard x={680} y={250} desc="vista aérea de Iguape (SP)" file="vista-aerea-iguape.jpg" w={600} h={400} /></Enter>
					</div>
				)}
				<CoastMap at={foldEnd + 6} until={a(6)} places={['saoVicente', 'iguape']} kind="pop" />
				{[0, 1, 2].map((i) => <Walker key={i} from={foldEnd + 30 + i * 30} to={a(6) - 20} a={[COAST.saoVicente[0] - 70 - i * 46, COAST.saoVicente[1] - 10 + i * 22]} b={[COAST.iguape[0] - 110 - i * 46, COAST.iguape[1] - 10 + i * 22]} look={soldier(i + 3)} s={0.36} seed={30 + i} until={a(6)} />)}
				<Label x={1330} y={640} text="Por que espanhóis?" at={a(3) + 10} until={a(6)} rot={-3} size={42} />
				<Label x={1290} y={725} text="Quem eram esses homens?" at={a(4) + 10} until={a(6)} rot={2} size={42} />
				<Label x={1250} y={800} text="Como chegou a São Vicente?" at={a(5) + 10} until={a(6)} rot={-2} size={42} />

				{/* mundo: Portugal e Espanha */}
				<WorldMap at={a(6)} kind="right" />
				<Enter at={a(6) + 12} kind="left"><Caravel x={700} y={430} s={0.3} flag={C.es} /></Enter>
				<Enter at={a(6) + 20} kind="right"><Caravel x={1200} y={430} s={0.3} flip flag={C.pt} /></Enter>
				<Label x={620} y={250} text="Espanha" at={a(6) + 26} fill={C.es} color={C.white} size={52} />
				<Label x={1280} y={250} text="Portugal" at={a(6) + 32} fill={C.pt} color={C.white} size={52} />
				<BigText x={960} y={800} text="Prepare-se!" at={a(7)} size={110} color={C.terra} />
				<Label x={960} y={160} text="Um dos episódios menos conhecidos da história do Brasil" at={a(7) + 18} size={40} rot={1} />
			</Camera>
		</AbsoluteFill>
	);
};
