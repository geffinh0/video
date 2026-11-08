import React from 'react';
import {Composition, Still} from 'remotion';
import {Playground} from './Playground';
import {Video, VideoProps} from './Video';
import {Thumbnail} from './Thumbnail';
import {totalFrames, FPS} from './timing';

export const RemotionRoot: React.FC = () => (
	<>
		<Composition id="GuerraDeIguape" component={Video as React.FC<VideoProps>} durationInFrames={totalFrames} fps={FPS} width={1920} height={1080} defaultProps={{music: false}} />
		<Still id="Thumbnail" component={Thumbnail} width={1280} height={720} />
		<Composition id="Playground" component={Playground} durationInFrames={90} fps={30} width={1920} height={1080} />
	</>
);
