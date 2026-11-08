import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans} from '../cutout/theme';
import {CutPath, Ink, Label, Piece, Sheet} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell} from '../cutout/noise';
import {Puppet} from '../characters/Puppet';
import {cast} from '../characters/cast';
import {Caravel, Canoe, Crate, House, Mangrove, Tree} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {BigText, SP, Walker, clamp} from './shared';

const Ficha: React.FC<{x: number; at: number; until: number; name: string; role: string; fill: string; children: React.ReactNode}> = ({x, at, until, name, role, fill, children}) => (
	<Enter at={at} until={until} kind="drop" seed={x}>
		<Sheet x={x} y={90} w={540} h={700} fill={C.parch2} rot={x < 900 ? -1.4 : 1.4} seed={x % 50} tape>
			<div style={{position: 'absolute', left: 0, right: 0, top: 22, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 44, color: C.ink}}>{name}</div>
			<div style={{position: 'absolute', left: 60, right: 60, top: 82, height: 44, background: fill, color: C.white, borderRadius: 4, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 24, lineHeight: '44px', whiteSpace: 'nowrap'}}>{role}</div>
			{children}
		</Sheet>
	</Enter>
);

export const Scene3: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const p1 = clamp((sf - a(1)) / Math.max(1, e(2) - a(1)));
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: sc.dur, s: 1.04}]}>
				<BigText x={960} y={470} text="Dois personagens" at={0} until={a(1)} size={100} />
				{/* Moschera */}
				<Ficha x={240} at={a(1)} until={a(7)} name="Ruy Garcia Moschera" role="espanhol • aventureiro" fill={C.es}>
					<Puppet x={270} y={650} s={1.4} look={cast.moschera} pose="talk" seed={3} startAt={a(1)} />
				</Ficha>
				{/* rota do Rio da Prata ao litoral sul paulista */}
				<Enter at={a(1) + 8} until={a(3)} kind="drop" seed={5}>
					<Sheet x={815} y={190} w={290} h={420} fill={C.sea} rot={1} seed={6}>
						<svg width={290} height={420} style={{position: 'absolute', overflow: 'visible'}}>
							<CutPath pts={[[0, 0], [140, 0], [250, 150], [210, 330], [150, 420], [0, 420]]} fill={C.sand} seed={7} amp={5} sw={5} />
							<path d="M 120 380 Q 160 280 190 200 T 210 80" stroke={C.terra} strokeWidth={7} strokeDasharray="14 12" fill="none" strokeLinecap="round" />
						</svg>
						<div style={{position: 'absolute', left: 14, top: 330, fontFamily: sans, fontWeight: 800, fontSize: 24, color: C.ink}}>Rio da Prata</div>
						<div style={{position: 'absolute', left: 98, top: 14, fontFamily: sans, fontWeight: 800, fontSize: 24, color: C.ink}}>litoral sul de SP</div>
						<svg width={1} height={1} style={{position: 'absolute', left: 120 + p1 * 90, top: 380 - p1 * 300, overflow: 'visible'}}><circle r={13} fill={C.es} stroke={C.outline} strokeWidth={4} /></svg>
					</Sheet>
				</Enter>
				<Enter at={a(2) + 6} until={a(3)} kind="pop" seed={9}>
					<Sheet x={810} y={650} w={300} h={170} fill={C.white} rot={-3} seed={9}>
						<div style={{position: 'absolute', left: 14, top: 14, width: 130, height: 142, background: C.es, opacity: 0.85}} /><div style={{position: 'absolute', left: 156, top: 14, width: 130, height: 142, background: C.pt, opacity: 0.85}} />
						<div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: sans, fontWeight: 800, fontSize: 24, color: C.white, textAlign: 'center'}}>Tordesilhas?</div>
					</Sheet>
				</Enter>
				{/* Cosme */}
				<Ficha x={1140} at={a(3)} until={a(7)} name="Cosme Fernandes" role="Bacharel de Cananeia · português" fill={C.pt}>
					<Puppet x={270} y={650} s={1.4} look={cast.cosme} pose={f >= a(6) ? 'cross' : 'talk'} seed={4} startAt={a(3)} />
				</Ficha>
				<Label x={1400} y={850} text="bacharel = formação acadêmica" at={a(4)} until={a(5)} size={38} rot={-1} />
				<Label x={1400} y={850} text="degredado = condenado e enviado para longe" at={a(5)} until={a(6)} size={38} rot={1} fill={C.terra} color={C.white} />
				<Enter at={a(5) + 8} until={a(7)} kind="drop" seed={12}>
					<Sheet x={815} y={190} w={290} h={420} fill={C.sea} rot={-1} seed={11}>
						<svg width={290} height={420} style={{position: 'absolute', overflow: 'visible'}}><CutPath pts={[[0, 260], [290, 230], [290, 420], [0, 420]]} fill={C.sand} seed={13} amp={5} sw={5} /></svg>
						<Caravel x={90} y={190} s={0.2} />
					</Sheet>
					<Puppet x={230} y={470} s={0.4} look={cast.cosme} pose="idle" seed={5} startAt={a(5)} />
				</Enter>
				<Label x={960} y={680} text="≈ 1502" at={a(6)} until={a(7)} size={54} fill={C.terra} color={C.white} />
				{/* influência do bacharel */}
				{[[<House key="h" x={1760} y={500} s={0.5} />, 0], [<Crate key="c" x={1760} y={640} s={0.7} />, 1], [<Canoe key="k" x={1740} y={750} s={0.3} />, 2]].map(([el, i]) => <Enter key={i as number} at={a(6) + (i as number) * 18} until={a(7)} kind="drop">{el}</Enter>)}
				{/* aliança */}
				<Walker from={a(7)} to={a(7) + 45} a={[260, 760]} b={[760, 760]} look={cast.moschera} s={0.95} seed={21} after="handshake" />
				<Walker from={a(7)} to={a(7) + 45} a={[1700, 760]} b={[1180, 760]} look={cast.cosme} s={0.95} flip seed={22} after="handshake" />
				<Label x={970} y={300} text="Aliança" at={a(7) + 50} until={a(8)} fill={C.ocre} size={76} rot={-3} />
				{/* povos indígenas */}
				<Enter at={a(8)} kind="up" seed={30}>
					<Sheet x={120} y={150} w={1680} h={690} fill={C.sea2} seed={14} amp={4} rot={0.3}>
						<svg width={1680} height={690} style={{position: 'absolute', overflow: 'visible'}}>
							<CutPath pts={[[0, 0], [1680, 0], [1680, 200], [0, 260]]} fill={C.forest2} seed={15} amp={7} sw={5} />
							<CutPath pts={[[0, 560], [1680, 520], [1680, 690], [0, 690]]} fill={C.forest} seed={16} amp={7} sw={5} />
						</svg>
					</Sheet>
				</Enter>
				<Enter at={a(8) + 10} kind="drop"><Tree x={300} y={400} s={0.9} /><Tree x={1500} y={390} s={1} seed={9} /><Mangrove x={900} y={440} s={0.8} /></Enter>
				<Enter at={a(8) + 22} kind="left"><Canoe x={560} y={640} s={0.8} /></Enter>
				<Walker from={a(8) + 20} to={a(9) + 30} a={[260, 810]} b={[700, 810]} look={cast.guia} s={0.8} seed={31} />
				<Walker from={a(8) + 30} to={a(9) + 30} a={[1700, 820]} b={[1240, 820]} look={cast.indio} s={0.8} flip seed={32} after="bow" />
				<Label x={960} y={175} text="Povos indígenas" sub="conheciam os rios, as matas, os caminhos e o litoral" at={a(8) + 30} fill={C.ind} size={54} />
				{f >= a(9) && <>
					<Label x={960} y={470} text="alianças militares e estratégicas" at={a(9) + 8} size={46} rot={-2} fill={C.parch2} />
				</>}
				<Label x={560} y={860} text="Interesses políticos" at={a(10)} size={40} fill={C.es} color={C.white} rot={-2} />
				<Label x={960} y={860} text="Disputas territoriais" at={a(10) + 12} size={40} fill={C.pt} color={C.white} rot={2} />
				<Label x={1360} y={860} text="Alianças locais" at={a(10) + 24} size={40} fill={C.ind} rot={-1} />
			</Camera>
		</AbsoluteFill>
	);
};
