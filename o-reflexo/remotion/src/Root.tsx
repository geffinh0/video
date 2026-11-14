import React from 'react';
import {Composition} from 'remotion';
import {FPS, H, TOTAL, W} from './timing';
import {TheReflection} from './compositions/TheReflection';

export const RemotionRoot: React.FC = () => (
	<Composition id="OReflexo" component={TheReflection} durationInFrames={TOTAL} fps={FPS} width={W} height={H} />
);
