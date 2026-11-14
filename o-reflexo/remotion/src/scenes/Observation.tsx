import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {SecurityCam} from '../components/devices';
import {PlateSpace, Seq} from '../components/plate';
import {MirrorGlass} from '../components/MirrorGlass';
import {Snd, Sounds} from '../components/AudioLayer';

// S03 — Observação. CAM01 fixa. Clara olha a porta; o reflexo continua olhando para a câmera.
// Quando ela volta ao espelho, tudo está normal. Sem som de "susto": câmera de segurança não grava áudio.
const T0 = 2; const DUR = 22;
const SND: Snd[] = [
	{name: 'glitch_c', at: 0, vol: 0.35},
	{name: 'cctv_tone', at: T0, dur: DUR, vol: 0.22},
	{name: 'hum', at: T0, dur: DUR, vol: 0.1},
];
export const Observation: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Sequence durationInFrames={f(T0)}>
			<ArchiveCard dur={T0} lines={['ARQUIVO 0063', 'DISPOSITIVO: CAM01', 'DATA: 15/11/2026', 'STATUS: RECUPERADO (PARCIAL)']} />
		</Sequence>
		<Sequence from={f(T0)} durationInFrames={f(DUR)}>
			<SecurityCam date="15/11/2026" time0={0 * 3600 + 17 * 60 + 44} drop={0.008}>
				<PlateSpace><Seq dir="s03" count={88} fps={4} /><MirrorGlass x={612} y={262} w={176} h={350} /></PlateSpace>
			</SecurityCam>
		</Sequence>
		<Sounds list={SND} />
	</AbsoluteFill>
);
