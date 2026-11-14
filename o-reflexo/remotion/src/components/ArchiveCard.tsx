import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {FPS} from '../timing';
import {OSD, SliceGlitch, VHS} from './fx';

// Identificação do arquivo recuperado: texto de sistema digitado sobre preto com ruído analógico.
export const ArchiveCard: React.FC<{lines: string[]; dur: number; corrupt?: number}> = ({lines, dur, corrupt = 0}) => {
	const fr = useCurrentFrame(); const t = fr / FPS;
	const chars = Math.floor(t * 38);
	let used = 0;
	const shown = lines.map((l) => {const s = l.slice(0, Math.max(0, chars - used)); used += l.length + 4; return s;});
	const cursor = Math.floor(t * 2.5) % 2 === 0;
	const fadeOut = t > dur - 0.25;
	const body = (
		<AbsoluteFill style={{background: '#050505'}}>
			<div style={{position: 'absolute', left: 160, top: 360}}>
				{shown.map((s, i) => (
					<OSD key={i} style={{position: 'relative', fontSize: 40, marginBottom: 18, color: i === lines.length - 1 && corrupt > 0 && random(`cc${fr}`) < 0.3 ? '#ff4040' : '#d8d8cc'}}>
						{s}{i === shown.findIndex((x, k) => x.length < lines[k].length) || (i === lines.length - 1 && shown[i].length === lines[i].length) ? (cursor ? '█' : ' ') : ''}
					</OSD>
				))}
			</div>
		</AbsoluteFill>
	);
	return (
		<AbsoluteFill style={{opacity: fadeOut ? 0 : 1}}>
			<VHS strength={0.9} tracking={0.4 + corrupt} seed="card">
				<SliceGlitch amount={corrupt * (random(`cg${Math.floor(t * 8)}`) < 0.5 ? 0.6 : 0.1)} seed="card">{body}</SliceGlitch>
			</VHS>
		</AbsoluteFill>
	);
};
