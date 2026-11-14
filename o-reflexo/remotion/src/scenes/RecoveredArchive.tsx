import React from 'react';
import {AbsoluteFill, Img, Sequence, random, staticFile, useCurrentFrame} from 'remotion';
import {FPS, f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {SecurityCam} from '../components/devices';
import {Grain, SliceGlitch, VHS} from '../components/fx';
import {Plate, PlateSpace} from '../components/plate';
import {Snd, Sounds} from '../components/AudioLayer';

// S01 — Arquivo recuperado. Ruído de fita, identificação, e o banheiro pela CAM01.
// Ela entra, olha o espelho e sai (a 4 quadros por segundo, como uma câmera de segurança barata).
// Depois que ela sai, o espelho continua mostrando alguém por alguns segundos.
const CCTV0 = 8;
const plateAt = (u: number) => (u < 3.5 ? 'cctv_empty' : u < 4.75 ? 'cctv_walk' : u < 9.5 ? 'cctv_mirror' : u < 10.5 ? 'cctv_walk' : 'cctv_empty');

const Footage: React.FC = () => {
	const fr = useCurrentFrame(); const u = Math.floor((fr / FPS) * 4) / 4;   // 4 fps
	const ghost = u >= 13.5 && u < 17 ? (u < 14 ? 0.12 : u < 16.25 ? 0.42 + 0.08 * Math.sin(u * 7) : 0.15) : 0;
	const glitch = u > 18.5 ? 0.9 : 0;
	return (
		<SecurityCam date="14/11/2026" time0={23 * 3600 + 41 * 60 + 7} drop={0.01}>
			<SliceGlitch amount={glitch} seed="s01">
				<PlateSpace>
					<Plate name={plateAt(u)} />
					{ghost > 0 && (
						// no espelho vazio (715–970 × 145–385): a figura que não está no banheiro
						<div style={{position: 'absolute', left: 715, top: 145, width: 255, height: 240, overflow: 'hidden', opacity: ghost}}>
							<Img src={staticFile('assets/plates/s06_comp.png')} style={{position: 'absolute', left: -455, top: -211, width: 1344 * 0.78, height: 768 * 0.78, filter: 'blur(1.2px) contrast(1.1) brightness(0.95)', WebkitMaskImage: 'radial-gradient(ellipse 45% 60% at 47% 55%, #000 55%, transparent 100%)'}} />
						</div>
					)}
				</PlateSpace>
			</SliceGlitch>
		</SecurityCam>
	);
};

const SND: Snd[] = [
	{name: 'tape_in', at: 0, vol: 0.7},
	{name: 'vhs_hiss', at: 0, dur: 8.2, vol: 0.45, fadeOut: 0.4},
	{name: 'clicks', at: 2.6, vol: 0.5},
	{name: 'cctv_tone', at: 8, dur: 19, vol: 0.22, fadeIn: 0.05},
	{name: 'hum', at: 8, dur: 19, vol: 0.12},
	{name: 'low_drone', at: 20.5, dur: 7, vol: 0.22, fadeIn: 2, fadeOut: 2},
	{name: 'glitch_a', at: 26.4, vol: 0.55},
];

export const RecoveredArchive: React.FC = () => {
	const fr = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Sequence durationInFrames={f(3)}>
				<VHS strength={1.4} tracking={1} seed="intro">
					<AbsoluteFill style={{background: '#111'}}><Grain opacity={0.9} scale={2} blend="normal" /></AbsoluteFill>
				</VHS>
				{random(`fl${fr}`) < 0.15 && <AbsoluteFill style={{background: '#000'}} />}
			</Sequence>
			<Sequence from={f(3)} durationInFrames={f(5)}>
				<ArchiveCard dur={5} lines={['ARQUIVO 0047', 'DISPOSITIVO: CAM01', 'DATA: 14/11/2026', 'STATUS: RECUPERADO']} />
			</Sequence>
			<Sequence from={f(CCTV0)} durationInFrames={f(19)}><Footage /></Sequence>
			<Sounds list={SND} />
		</AbsoluteFill>
	);
};
