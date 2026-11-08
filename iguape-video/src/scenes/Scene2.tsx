import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C, SHADOW, sans} from '../cutout/theme';
import {CutPath, Label, Sheet} from '../cutout/Paper';
import {Enter, st, Camera} from '../cutout/motion';
import {ell} from '../cutout/noise';
import {Caravel, Scroll} from '../props';
import {Table} from '../Table';
import {A, E} from '../timing';
import {Arrow, BigText, SP, WORLD, WP, WorldMap, clamp} from './shared';

const Hut: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<svg width={1} height={1} style={{position: 'absolute', left: x, top: y, overflow: 'visible', filter: SHADOW}}>
		<g transform={`scale(${s})`}><CutPath pts={[[-30, 0], [30, 0], [24, -26], [0, -62], [-24, -26]]} fill={C.ind} seed={4} amp={1.6} /><CutPath pts={[[-8, 0], [8, 0], [8, -22], [-8, -22]]} fill={C.wood} seed={5} amp={0.8} sw={3} /></g>
	</svg>
);

export const Scene2: React.FC<SP> = ({sc}) => {
	const f = useCurrentFrame();
	const a = (k: number) => A(sc, k), e = (k: number) => E(sc, k);
	const sf = st(f);
	const shake = f >= a(5) && f < a(6) ? Math.sin(sf / 4) * 34 : 0;
	const lineX = WP.line + shake;
	const lineVisible = f >= a(4);
	const zoom = f >= a(7) && f < a(9) ? 1.9 : 1;
	const camX = (WP.south[0] - 960) * 1.9, camY = (WP.south[1] - 540) * 1.9;
	const m1 = clamp((sf - a(1)) / Math.max(1, e(1) - a(1)));
	const m6 = clamp((sf - a(6)) / Math.max(1, e(6) - a(6)));
	return (
		<AbsoluteFill>
			<Table />
			<Camera keys={[{f: 0, s: 1}, {f: a(7) - 1, s: 1}, {f: a(7) + 24, s: 1.9, x: camX, y: camY}, {f: a(9) - 1, s: 1.9, x: camX, y: camY}, {f: a(9) + 20, s: 1}]}>
				<WorldMap at={0} until={a(9) + 8} />
				{/* tintas dos lados do tratado */}
				{lineVisible && f < a(9) && <>
					<div style={{position: 'absolute', left: WORLD.x, top: WORLD.y, width: lineX - WORLD.x, height: WORLD.h, background: C.es, opacity: 0.2}} />
					<div style={{position: 'absolute', left: lineX, top: WORLD.y, width: WORLD.x + WORLD.w - lineX, height: WORLD.h, background: C.pt, opacity: 0.2}} />
				</>}
				<Label x={1290} y={225} text="Portugal" at={8} until={a(2)} fill={C.pt} color={C.white} size={36} />
				<Label x={1010} y={330} text="Espanha" at={14} until={a(2)} fill={C.es} color={C.white} size={36} />
				{/* 1492 */}
				{f >= a(1) && f < a(3) && <Caravel x={1100 - m1 * 480} y={560 - m1 * 60} s={0.26} flag={C.es} />}
				<Label x={800} y={680} text="1492 — Colombo" sub="expedição financiada pela Coroa espanhola" at={a(1) + 10} until={a(3)} size={38} />
				{/* 1494 */}
				<Enter at={a(2)} until={a(4)} kind="drop"><Scroll x={960} y={560} s={1.25} /><div style={{position: 'absolute', left: 760, top: 300, width: 400, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 40, color: C.ink, transform: 'rotate(-1deg)'}}>Tratado de Tordesilhas<div style={{color: C.terra, fontSize: 54}}>1494</div></div></Enter>
				<BigText x={960} y={300} text="?" at={a(3)} until={a(4)} size={240} color={C.terra} />
				{/* linha */}
				{lineVisible && f < a(9) && <Enter at={a(4)} kind="drop" seed={8}><div style={{position: 'absolute', left: lineX - 7, top: WORLD.y, width: 14, height: WORLD.h, background: `repeating-linear-gradient(${C.ink} 0 22px, transparent 22px 36px)`, filter: SHADOW}} /></Enter>}
				<Label x={680} y={150} text="Espanha" at={a(4) + 18} until={a(6)} fill={C.es} color={C.white} size={36} />
				<Label x={1040} y={150} text="Portugal" at={a(4) + 24} until={a(6)} fill={C.pt} color={C.white} size={36} />
				<Enter at={a(4) + 6} until={a(6)} kind="pop"><svg width={1} height={1} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}><circle cx={WP.cabo[0]} cy={WP.cabo[1]} r={13} fill={C.terra} stroke={C.outline} strokeWidth={4} /></svg></Enter>
				<Label x={WP.cabo[0] + 10} y={WP.cabo[1] + 56} text="Ilhas de Cabo Verde" at={a(4) + 10} until={a(6)} size={30} />
				<Arrow x={WP.line + 20} y={WP.cabo[1] - 4} len={WP.cabo[0] - WP.line - 60} rot={0} at={a(4) + 20} fill={C.ocre} />
				<Label x={(WP.line + WP.cabo[0]) / 2} y={WP.cabo[1] - 80} text="370 léguas" sub="a oeste das ilhas de Cabo Verde" at={a(4) + 28} until={a(6)} size={44} rot={-2} />
				<Label x={960} y={760} text="mapas imprecisos, fronteiras difíceis" at={a(5)} until={a(6)} fill={C.terra} color={C.white} size={44} rot={1} />
				{[0, 1, 2].map((i) => <BigText key={i} x={560 + i * 300} y={440 + (i % 2) * 90} text="?" at={a(5) + 6 + i * 8} until={a(6)} size={150} color={C.ink} rot={i * 8 - 8} />)}
				{/* 1500 */}
				{f >= a(6) && f < a(7) + 30 && <Caravel x={1010 - m6 * 360} y={440 + m6 * 60} s={0.24} flip flag={C.pt} />}
				<Label x={1000} y={650} text="1500 — chegada ao Brasil" at={a(6) + 8} until={a(7)} size={40} />
				{/* litoral sul */}
				<Label x={WP.south[0] + 90} y={WP.south[1] - 10} text="Iguape e Cananeia" at={a(7) + 24} until={a(9)} size={20} rot={-2} />
				{[0, 1, 2].map((i) => <Enter key={i} at={a(8) + i * 14} until={a(9)} kind="drop"><Hut x={WP.south[0] - 15 + i * 26} y={WP.south[1] + 28 + (i % 2) * 14} s={0.42} /></Enter>)}
				<Label x={WP.south[0] + 170} y={WP.south[1] + 70} text="já habitada por diferentes povos" at={a(8) + 20} until={a(9)} size={19} fill={C.ind} />
			</Camera>
			{/* tabuleiro final */}
			<Enter at={a(9)} kind="drop">
				<Sheet x={470} y={110} w={980} h={640} fill={C.parch2} rot={-1} seed={44} tape>
					{[[C.pt, 'Coroa portuguesa', 250, 190], [C.es, 'Coroa espanhola', 730, 190], [C.ind, 'Povos indígenas que já viviam ali', 490, 440]].map(([c, t, x, y], i) => (
						<Enter key={i} at={a(9) + 14 + i * 22} kind="pop" seed={i}>
							<svg width={1} height={1} style={{position: 'absolute', left: x as number, top: y as number, overflow: 'visible', filter: SHADOW}}><CutPath pts={ell(86, 86, 0, 0, 16)} fill={c as string} seed={i + 3} amp={3} /></svg>
							<div style={{position: 'absolute', left: (x as number) - 210, width: 420, top: (y as number) + 100, textAlign: 'center', fontFamily: sans, fontWeight: 800, fontSize: 36, color: C.ink}}>{t as string}</div>
						</Enter>
					))}
				</Sheet>
			</Enter>
		</AbsoluteFill>
	);
};
