import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {FPS, f} from '../timing';
import {ArchiveCard} from '../components/ArchiveCard';
import {PhoneCam} from '../components/devices';
import {SliceGlitch, ramp, smooth} from '../components/fx';
import {PlateSpace, Seq} from '../components/plate';
import {Snd, Sounds} from '../components/AudioLayer';

// S04 — O sorriso. Celular colado ao espelho: só o reflexo enche a tela. Clara está séria (ouvimos a respiração);
// o reflexo começa a sorrir devagar. Ela recua: a câmera se afasta, mas o rosto do reflexo demora a acompanhar.
const T0 = 2; const DUR = 17; const BACK = 12.5;
const Footage: React.FC = () => {
	const fr = useCurrentFrame(); const u = fr / FPS;
	const pull = smooth(u, BACK, BACK + 0.45);                 // câmera recua (o quadro inteiro)
	const lagged = smooth(u, BACK + 0.55, BACK + 0.9);          // o rosto só acompanha depois
	const sc = 1.32 - 0.32 * pull; const scFace = 1.32 - 0.32 * lagged;
	const ghost = u > BACK && u < BACK + 0.95 ? 1 : 0;
	const cut = u > DUR - 0.1 ? 1 : 0;
	return (
		<PhoneCam shake={0.8} focus={0.6} seed="s04" shakeBoost={1.6 * ramp(u, 3.5, 12) + (u > BACK ? 1.2 : 0)} extraBlur={u > BACK && u < BACK + 0.4 ? 3 : 0}>
			<SliceGlitch amount={cut} seed="s04c">
				<AbsoluteFill style={{transform: `scale(${sc}) translate(${-30 * pull}px, ${20 * pull}px)`}}>
					<PlateSpace><Seq dir="s04" count={255} fps={15} /></PlateSpace>
				</AbsoluteFill>
				{ghost > 0 && (
					<AbsoluteFill style={{transform: `scale(${scFace})`, WebkitMaskImage: 'radial-gradient(ellipse 24% 46% at 50% 47%, #000 60%, transparent 100%)', opacity: 0.9}}>
						<PlateSpace><Seq dir="s04" count={255} fps={15} /></PlateSpace>
					</AbsoluteFill>
				)}
				{/* o vidro: respingos secos e marcas de dedo, acompanham o espelho */}
				<AbsoluteFill style={{transform: `scale(${sc})`}}>
					<Img src={staticFile('assets/fx/mirror_dirt.png')} style={{width: '100%', height: '100%', opacity: 0.5, mixBlendMode: 'screen'}} />
					<AbsoluteFill style={{background: 'linear-gradient(120deg, rgba(255,255,255,0) 30%, rgba(255,255,255,0.07) 42%, rgba(255,255,255,0) 52%)', mixBlendMode: 'screen'}} />
				</AbsoluteFill>
			</SliceGlitch>
		</PhoneCam>
	);
};
const SND: Snd[] = [
	{name: 'glitch_c', at: 0, vol: 0.4},
	{name: 'phone_room', at: T0, dur: DUR, vol: 0.55},
	{name: 'breathing', at: T0 + 0.5, dur: 16.5, vol: 0.55, fadeIn: 1},
	{name: 'v_nao', at: T0 + 9.2, vol: 0.85},
	{name: 'low_drone', at: T0 + 4, dur: 13, vol: 0.28, fadeIn: 5, fadeOut: 0.1},
	{name: 'gasp', at: T0 + BACK - 0.1, vol: 0.7},
	{name: 'sub_hit', at: T0 + BACK + 0.05, vol: 0.45},
	{name: 'glitch_c', at: T0 + DUR - 0.1, vol: 0.7},
];
export const TheSmile: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Sequence durationInFrames={f(T0)}>
			<ArchiveCard dur={T0} lines={['ARQUIVO 0071', 'DISPOSITIVO: CELULAR', 'DATA: 15/11/2026  02:58', 'STATUS: RECUPERADO']} />
		</Sequence>
		<Sequence from={f(T0)} durationInFrames={f(DUR)}><Footage /></Sequence>
		<Sounds list={SND} />
	</AbsoluteFill>
);
