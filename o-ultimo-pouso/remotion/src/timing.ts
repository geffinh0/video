import data from './data/shots.json';

export const FPS = 30;
export const LAYER_FPS = 30;
export type Shot = {
	id: string; seq: number; dur: number; set: string; desc: string;
	lines?: [string, number][]; sfx?: [string, number, number][];
	move?: {zoom?: [number, number]; pan?: [[number, number], [number, number]]};
	layers?: string[]; flash?: number[]; blackout?: [number, number]; warm?: boolean; rack?: [number, number];
	rainGlass?: boolean; inserts?: string[];
};
let acc = 0;
export const SHOTS = (data.shots as Shot[]).map((s) => {
	const from = acc; const frames = Math.round(s.dur * FPS); acc += frames;
	return {...s, from, frames};
});
export const TOTAL = acc;
export const EXTERIOR = new Set(['forest', 'mansion', 'statue', 'window_ext']);
export const INTERIOR_CANDLE = new Set(['study_wide', 'study_desk', 'photo', 'arthur_profile', 'clock', 'window_int', 'ots_window', 'raven_sill', 'raven_eye', 'arthur_recoil', 'drawer', 'letter_closed', 'letter_read', 'letter_window', 'door_deep', 'corridor', 'portrait', 'door_present', 'study_return', 'raven_chair', 'raven_beak', 'arthur_face', 'wrist', 'raven_wings']);
