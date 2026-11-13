import React from 'react';
import {Composition} from 'remotion';
import {Film} from './Film';
import {FPS, TOTAL} from './timing';

export const RemotionRoot: React.FC = () => (
	<Composition id="OUltimoPouso" component={Film} durationInFrames={TOTAL} fps={FPS} width={1920} height={1080} />
);
