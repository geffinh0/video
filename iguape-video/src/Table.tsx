import React from 'react';
import {AbsoluteFill, staticFile} from 'remotion';
import {C} from './cutout/theme';
import {TornStrip} from './cutout/Paper';

/** Mesa de papel: base escura + folhas em camadas com bordas rasgadas. */
export const Table: React.FC<{base?: string; sheet?: string; sheet2?: string}> = ({base = C.dark, sheet = C.parch, sheet2 = C.sand}) => (
	<AbsoluteFill style={{background: base}}>
		<div style={{position: 'absolute', left: 60, top: 50, width: 1800, height: 980, background: sheet2, transform: 'rotate(-0.6deg)', filter: 'drop-shadow(8px 10px 0 rgba(0,0,0,0.3))'}} />
		<div style={{position: 'absolute', left: 90, top: 80, width: 1740, height: 930, background: sheet, transform: 'rotate(0.4deg)'}} />
	</AbsoluteFill>
);

/** Overlay global de textura de papel (multiply) e vinheta. */
export const Finish: React.FC<{vignette?: number}> = ({vignette = 0.5}) => (
	<>
		<AbsoluteFill style={{backgroundImage: `url(${staticFile('textures/paper.png')})`, backgroundSize: '512px 512px', mixBlendMode: 'multiply', opacity: 0.55, pointerEvents: 'none'}} />
		<AbsoluteFill style={{backgroundImage: `url(${staticFile('textures/vignette.png')})`, backgroundSize: '100% 100%', opacity: vignette, pointerEvents: 'none'}} />
	</>
);
