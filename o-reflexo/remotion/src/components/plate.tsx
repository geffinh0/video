import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {H, W} from '../timing';
import {FrameSeq} from './fx';

// Espaço de coordenadas das imagens-base (1344x768), escalado para cobrir 1920x1080.
export const PW = 1344, PH = 768;
const S = Math.max(W / PW, H / PH);
export const PlateSpace: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
	<AbsoluteFill style={{overflow: 'hidden'}}>
		<div style={{position: 'absolute', width: PW, height: PH, left: (W - PW * S) / 2, top: (H - PH * S) / 2, transform: `scale(${S})`, transformOrigin: '0 0', ...style}}>{children}</div>
	</AbsoluteFill>
);

export const Plate: React.FC<{name: string; style?: React.CSSProperties}> = ({name, style}) => (
	<Img src={staticFile(`assets/plates/${name}.png`)} style={{position: 'absolute', left: 0, top: 0, width: PW, height: PH, ...style}} />
);

export const Seq: React.FC<{dir: string; count: number; fps: number; start?: number; style?: React.CSSProperties; hold?: number}> = (p) => (
	<div style={{position: 'absolute', left: 0, top: 0, width: PW, height: PH}}><FrameSeq {...p} /></div>
);
