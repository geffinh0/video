import React from 'react';
import {AbsoluteFill, Sequence, random, useCurrentFrame} from 'remotion';
import {FPS, f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {SecurityCam} from '../components/devices';
import {OSD, SliceGlitch, VHS} from '../components/fx';
import {Plate, PlateSpace, Seq} from '../components/plate';
import {Snd, Sounds} from '../components/AudioLayer';

// S06 — Último registro. Silêncio. CAM01: o banheiro vazio. Só o reflexo. Ele olha para a câmera e sorri.
// A gravação termina. "FIM DOS ARQUIVOS RECUPERADOS."
const CARD = 3, CAM = 5, DUR = 14, END = CAM + DUR;
const Footage: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	const lost = u > DUR - 1.0;
	return (
		<SecurityCam date="15/11/2026" time0={3 * 3600 + 33 * 60 + 2} drop={0.004}>
			<SliceGlitch amount={lost ? 0.85 : 0} seed="s06">
				<PlateSpace>
					<Plate name="cctv_empty" />
					{/* o reflexo, sozinho, dentro do espelho do banheiro vazio — no mesmo lugar do vulto do primeiro arquivo */}
					<div style={{position: 'absolute', left: 715, top: 145, width: 255, height: 240, overflow: 'hidden'}}>
						<div style={{position: 'absolute', left: -455, top: -211, width: 1344 * 0.78, height: 768 * 0.78, filter: 'blur(0.8px) brightness(0.97)', WebkitMaskImage: 'radial-gradient(ellipse 50% 66% at 47% 58%, #000 62%, transparent 100%)'}}>
							<div style={{position: 'absolute', left: 0, top: 0, width: 1344, height: 768, transform: 'scale(0.78)', transformOrigin: '0 0'}}>
								<Seq dir="s06" count={56} fps={4} hold={lost ? 55 : undefined} />
							</div>
						</div>
						<div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0) 20%, rgba(255,255,255,0.12) 28%, rgba(255,255,255,0) 36%)', mixBlendMode: 'screen'}} />
					</div>
				</PlateSpace>
			</SliceGlitch>
			{u > DUR - 0.45 && <AbsoluteFill style={{background: '#06102a'}}><OSD style={{left: 760, top: 500, fontSize: 40}}>{random(`ns${Math.floor(u * 3)}`) < 0.7 ? 'SEM SINAL' : ''}</OSD></AbsoluteFill>}
		</SecurityCam>
	);
};

const EndText: React.FC = () => {
	const fr = useCurrentFrame(); const t = fr / FPS;
	const s = 'FIM DOS ARQUIVOS RECUPERADOS.';
	const n = Math.floor(Math.max(0, t - 0.8) * 16);
	return (
		<VHS strength={0.5} tracking={0} seed="end">
			<AbsoluteFill style={{background: '#030303'}}>
				<OSD style={{left: 0, right: 0, top: 510, textAlign: 'center', fontSize: 38, letterSpacing: 6, opacity: t > 4.6 ? 0 : 1}}>{s.slice(0, n)}{n < s.length && Math.floor(t * 2.5) % 2 === 0 ? '█' : ' '}</OSD>
			</AbsoluteFill>
		</VHS>
	);
};

const SND: Snd[] = [
	{name: 'glitch_c', at: CARD, vol: 0.3},
	{name: 'cctv_tone', at: CAM, dur: DUR, vol: 0.2},
	{name: 'hum', at: CAM, dur: DUR, vol: 0.08},
	{name: 'glitch_a', at: END - 1.0, vol: 0.6},
	{name: 'vhs_hiss', at: END, dur: 5, vol: 0.25, fadeIn: 0.5, fadeOut: 1.5},
];

export const LastFootage: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Sequence from={f(CARD)} durationInFrames={f(CAM - CARD)}>
			<ArchiveCard dur={CAM - CARD} lines={['ARQUIVO 0075', 'DISPOSITIVO: CAM01', 'DATA: 15/11/2026', 'STATUS: RECUPERADO']} />
		</Sequence>
		<Sequence from={f(CAM)} durationInFrames={f(DUR)}><Footage /></Sequence>
		<Sequence from={f(END)} durationInFrames={f(5)}><EndText /></Sequence>
		<Sounds list={SND} />
	</AbsoluteFill>
);
