import React from 'react';
import {Sequence, interpolate, staticFile} from 'remotion';
import {Audio} from '@remotion/media';
import {FPS, SHOTS} from './timing';
import voices from './data/voices.json';

const BEDS = new Set(['rain_ext', 'rain_int', 'rain_glass', 'rain_open', 'wind', 'wind_int', 'wind_open', 'room_tone', 'clock_tick', 'clock_tick_loud', 'low_drone']);
const SFX_LEN: Record<string, number> = {rain_ext: 40, rain_int: 40, rain_glass: 40, rain_open: 30, wind: 40, wind_int: 40, wind_open: 30, room_tone: 30, clock_tick: 30, clock_tick_loud: 30, low_drone: 20};

type Seg = {name: string; from: number; to: number; vol: number};
const beds: Seg[] = []; const shots: Seg[] = [];
for (const s of SHOTS) {
	for (const [name, at, vol] of s.sfx ?? []) {
		if (name === 'silence_drop') continue;
		if (BEDS.has(name) && at === 0) {
			const prev = [...beds].reverse().find((b) => b.name === name);
			if (prev && prev.to === s.from) { prev.to = s.from + s.frames; prev.vol = (prev.vol + vol) / 2; }
			else beds.push({name, from: s.from, to: s.from + s.frames, vol});
		} else shots.push({name, from: s.from + Math.round(at * FPS), to: s.from + s.frames, vol});
	}
}
const V = voices as Record<string, number>;

export const Sound: React.FC = () => (
	<>
		{beds.map((b, i) => {
			const len = b.to - b.from; const fade = Math.min(18, Math.floor(len / 3));
			return (
				<Sequence key={`b${i}`} from={b.from} durationInFrames={len} layout="none">
					<Audio src={staticFile(`audio/sfx/${b.name}.wav`)} loop={len / FPS > (SFX_LEN[b.name] ?? 30) - 0.5} volume={(f) => b.vol * 0.7 * interpolate(f, [0, fade, len - fade, len], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
				</Sequence>
			);
		})}
		{shots.map((x, i) => (
			<Sequence key={`s${i}`} from={x.from} durationInFrames={Math.max(1, x.to - x.from + Math.round(1.5 * FPS))} layout="none">
				<Audio src={staticFile(`audio/sfx/${x.name}.wav`)} volume={x.vol * 0.8} />
			</Sequence>
		))}
		{SHOTS.flatMap((s) => (s.lines ?? []).map(([id, at]) => (
			<Sequence key={`v${s.id}${id}`} from={s.from + Math.round(at * FPS)} durationInFrames={Math.ceil((V[id] + 0.6) * FPS)} layout="none">
				<Audio src={staticFile(`audio/voices/${id}.wav`)} volume={1.0} />
			</Sequence>
		)))}
	</>
);
