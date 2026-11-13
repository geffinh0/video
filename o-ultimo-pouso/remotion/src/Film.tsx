import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {SHOTS} from './timing';
import {ShotView} from './Shot';
import {Sound} from './Sound';

export const Film: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		{SHOTS.map((s) => (
			<Sequence key={s.id} from={s.from} durationInFrames={s.frames} name={`${s.id} ${s.desc.slice(0, 40)}`}>
				<ShotView s={s} />
			</Sequence>
		))}
		<Sound />
	</AbsoluteFill>
);
