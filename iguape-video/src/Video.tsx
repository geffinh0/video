import React from 'react';
import {AbsoluteFill, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Audio} from '@remotion/media';
import {C, SHADOW} from './cutout/theme';
import {TornStrip} from './cutout/Paper';
import {st} from './cutout/motion';
import {Finish} from './Table';
import {Captions} from './Captions';
import {SceneT, scenes} from './timing';
import {Scene1} from './scenes/Scene1';
import {Scene2} from './scenes/Scene2';
import {Scene3} from './scenes/Scene3';
import {Scene4} from './scenes/Scene4';
import {Scene5} from './scenes/Scene5';
import {Scene6} from './scenes/Scene6';
import {Scene7} from './scenes/Scene7';
import {Scene8} from './scenes/Scene8';
import {Scene9} from './scenes/Scene9';
import {Scene10} from './scenes/Scene10';

const COMPS: React.FC<{sc: SceneT}>[] = [Scene1, Scene2, Scene3, Scene4, Scene5, Scene6, Scene7, Scene8, Scene9, Scene10];
const WIPE: Record<number, string> = {2: C.terra, 3: C.sea, 4: C.pt, 5: C.dark, 6: C.dark, 7: C.ocre, 8: C.forest, 9: C.es, 10: C.terra};

/** Transição: folha de papel rasgada que desliza pela tela (em passos de 2 frames). */
const PaperWipe: React.FC<{color: string}> = ({color}) => {
	const f = st(useCurrentFrame(), 2);
	if (f >= 18) return null;
	const x = -2200 * Math.min(1, Math.max(0, (f - 2) / 14));
	return (
		<div style={{position: 'absolute', left: x, top: 0, width: 2200, height: 1080, filter: SHADOW}}>
			<div style={{position: 'absolute', left: 0, top: 0, width: 2080, height: 1080, background: color}} />
			<div style={{position: 'absolute', left: 2060, top: -10, width: 140, height: 1100, background: color, clipPath: 'polygon(0 0, 55% 6%, 20% 14%, 70% 24%, 30% 36%, 80% 50%, 25% 62%, 70% 74%, 30% 86%, 60% 94%, 0 100%)'}} />
			<div style={{position: 'absolute', left: 0, top: 0, width: 2080, height: 1080, backgroundImage: `url(${staticFile('textures/paper.png')})`, backgroundSize: '512px', mixBlendMode: 'multiply', opacity: 0.6}} />
		</div>
	);
};

export type VideoProps = {music: boolean};
export const Video: React.FC<VideoProps> = ({music}) => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{background: C.dark}}>
			{scenes.map((sc, i) => {
				const Comp = COMPS[i];
				return (
					<Sequence key={sc.id} from={sc.start} durationInFrames={sc.dur} premountFor={30}>
						<AbsoluteFill>
							<Comp sc={sc} />
							<Finish vignette={i === 4 || i === 5 ? 0.85 : 0.45} />
							{i > 0 && <PaperWipe color={WIPE[sc.id] ?? C.terra} />}
						</AbsoluteFill>
						<Audio src={staticFile(sc.audio)} />
					</Sequence>
				);
			})}
			<Captions />
			{music && <Audio src={staticFile('audio/musica.mp3')} loop volume={(fr) => (scenes.some((s) => fr >= s.start && fr < s.start + s.narrEnd) ? 0.06 : 0.2)} />}
		</AbsoluteFill>
	);
};
