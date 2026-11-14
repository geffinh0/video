import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {FPS, f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {PhoneCam} from '../components/devices';
import {SliceGlitch} from '../components/fx';
import {PlateSpace, Seq} from '../components/plate';
import {Snd, Sounds} from '../components/AudioLayer';

// S02 — Primeira anomalia. Celular na mão: Clara de perfil, o reflexo no espelho ao lado.
// Ela pisca; o reflexo pisca depois. De novo; o atraso cresce. Ela tenta se convencer de que é a câmera.
const T0 = 2; const DUR = 27;
const Footage: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	const cut = u > DUR - 0.12 ? 1 : 0;
	return (
		<PhoneCam shake={1} focus={0.8} seed="s02" shakeBoost={u > 19 ? 0.3 : 0}>
			<SliceGlitch amount={cut} seed="s02c">
				<PlateSpace><Seq dir="s02" count={405} fps={15} /></PlateSpace>
			</SliceGlitch>
		</PhoneCam>
	);
};

const SND: Snd[] = [
	{name: 'glitch_c', at: 0, vol: 0.4},
	{name: 'phone_room', at: T0, dur: DUR, vol: 0.55},
	{name: 'fan', at: T0, dur: DUR, vol: 0.18},
	{name: 'breath_in', at: T0 + 3.3, vol: 0.35},
	{name: 'v_denovo', at: T0 + 5.4, vol: 1},
	{name: 'breath_in', at: T0 + 7.4, vol: 0.4},
	{name: 'breath_out_shaky', at: T0 + 10.8, vol: 0.45},
	{name: 'v_camera', at: T0 + 14.5, vol: 0.95},
	{name: 'breath_out_shaky', at: T0 + 19.2, vol: 0.5},
	{name: 'low_drone', at: T0 + 19, dur: 8, vol: 0.18, fadeIn: 3, fadeOut: 0.2},
	{name: 'glitch_c', at: T0 + DUR - 0.12, vol: 0.6},
];

export const FirstAnomaly: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Sequence durationInFrames={f(T0)}>
			<ArchiveCard dur={T0} lines={['ARQUIVO 0051', 'DISPOSITIVO: CELULAR', 'DATA: 14/11/2026  23:52', 'STATUS: RECUPERADO']} />
		</Sequence>
		<Sequence from={f(T0)} durationInFrames={f(DUR)}><Footage /></Sequence>
		<Sounds list={SND} />
	</AbsoluteFill>
);
