import React from 'react';
import {Sequence, interpolate, staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {FPS} from '../timing';

// Um som posicionado no tempo da cena (segundos). `bed` = ambiente longo com fades; `loop` repete.
export type Snd = {name: string; at: number; dur?: number; vol?: number; fadeIn?: number; fadeOut?: number; loop?: boolean; rate?: number};

const LEN: Record<string, number> = {room_tone: 40, fan: 40, hum: 40, vhs_hiss: 30, cctv_tone: 30, phone_room: 40, breathing: 23.2, low_drone: 20};

export const Sounds: React.FC<{list: Snd[]}> = ({list}) => (
	<>
		{list.map((s, i) => {
			const len = s.dur ?? LEN[s.name] ?? 3;
			const frames = Math.max(1, Math.round(len * FPS));
			const fi = Math.round((s.fadeIn ?? 0) * FPS), fo = Math.round((s.fadeOut ?? 0) * FPS);
			const v = s.vol ?? 1;
			return (
				<Sequence key={i} from={Math.round(s.at * FPS)} durationInFrames={frames} layout="none">
					<Audio
						src={staticFile(`assets/audio/${s.name}.wav`)}
						loop={s.loop ?? (LEN[s.name] !== undefined && len > LEN[s.name] - 0.2)}
						playbackRate={s.rate ?? 1}
						volume={(f) => v * Math.min(fi ? interpolate(f, [0, fi], [0, 1], {extrapolateRight: 'clamp'}) : 1, fo ? interpolate(f, [frames - fo, frames], [1, 0], {extrapolateLeft: 'clamp'}) : 1)}
					/>
				</Sequence>
			);
		})}
	</>
);
