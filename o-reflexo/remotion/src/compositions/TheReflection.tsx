import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {SCENES, f} from '../timing';
import {RecoveredArchive} from '../scenes/RecoveredArchive';
import {FirstAnomaly} from '../scenes/FirstAnomaly';
import {Observation} from '../scenes/Observation';
import {TheSmile} from '../scenes/TheSmile';
import {FinalRecording} from '../scenes/FinalRecording';
import {LastFootage} from '../scenes/LastFootage';

const LIST: [keyof typeof SCENES, React.FC][] = [
	['archive', RecoveredArchive], ['first', FirstAnomaly], ['observe', Observation],
	['smile', TheSmile], ['final', FinalRecording], ['last', LastFootage],
];

export const TheReflection: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		{LIST.map(([k, C]) => (
			<Sequence key={k} from={f(SCENES[k].from)} durationInFrames={f(SCENES[k].dur)} name={k}><C /></Sequence>
		))}
	</AbsoluteFill>
);
