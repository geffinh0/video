export type Pose = {
	torso: number; head: number;
	aL: [number, number]; aR: [number, number];
	lL: [number, number]; lR: [number, number];
	y: number; rot?: number; dx?: number;
};
const S = (t: number, f = 1, a = 1, ph = 0) => Math.sin((t * f + ph) * Math.PI * 2) * a;
const clamp = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));
// Ângulos em graus. 0 = membro pendurado; negativo = para frente (personagem olhando para a direita).
const base = (t: number): Pose => ({torso: S(t, 0.4, 1.2), head: S(t, 0.4, 2), aL: [5, 8], aR: [-5, 8], lL: [2, 0], lR: [-2, 0], y: S(t, 0.4, 1.5)});

export const poses = {
	idle: (t: number): Pose => base(t),
	talk: (t: number): Pose => ({...base(t), head: S(t, 1.6, 5), aR: [-35 + S(t, 1.1, 14), -55 + S(t, 1.1, 20)], torso: S(t, 0.8, 2)}),
	walk: (t: number): Pose => ({torso: 3, head: S(t, 1.4, 2), aL: [-S(t, 1.4, 24), -14], aR: [S(t, 1.4, 24), -14],
		lL: [S(t, 1.4, 28), 6 + Math.max(0, S(t, 1.4, 32, 0.25))], lR: [-S(t, 1.4, 28), 6 + Math.max(0, -S(t, 1.4, 32, 0.25))], y: -Math.abs(S(t, 1.4, 6))}),
	run: (t: number): Pose => ({torso: 12, head: 0, aL: [-S(t, 2.2, 55), -70], aR: [S(t, 2.2, 55), -70],
		lL: [S(t, 2.2, 50), 30 + Math.max(0, S(t, 2.2, 60, 0.25))], lR: [-S(t, 2.2, 50), 30 + Math.max(0, -S(t, 2.2, 60, 0.25))], y: -Math.abs(S(t, 2.2, 12))}),
	point: (t: number): Pose => ({...base(t), torso: 4, aR: [-88 + S(t, 1.5, 3), -4], head: -4}),
	cross: (t: number): Pose => ({...base(t), aL: [-22, -112], aR: [-30, -118], head: S(t, 0.4, 2)}),
	shake: (t: number): Pose => ({...base(t), aL: [-22, -112], aR: [-30, -118], head: S(t, 2.6, 12)}),
	handshake: (t: number): Pose => ({...base(t), aR: [-62 + S(t, 2, 6), -28 + S(t, 2, 14)], torso: 4}),
	aim: (t: number): Pose => ({...base(t), torso: 3, aR: [-84, -6], aL: [-74, -24], head: -3, y: 0}),
	shoot: (t: number): Pose => {
		const k = clamp(1 - (t % 1.6) * 6, 0, 1);
		return {...base(t), torso: 3 - k * 6, aR: [-84 + k * 10, -6], aL: [-74 + k * 8, -24], head: -3 + k * 4, y: 0};
	},
	bow: (t: number): Pose => ({...base(t), aL: [-86, -4], aR: [-72 + S(t, 0.7, 10), -112], torso: 2}),
	row: (t: number): Pose => ({torso: S(t, 0.9, 10), head: 0, aL: [-50 + S(t, 0.9, 30), -40], aR: [-50 + S(t, 0.9, 30), -40], lL: [-70, 70], lR: [-70, 70], y: 40}),
	fall: (t: number): Pose => {
		const k = clamp(t * 1.8, 0, 1);
		return {torso: k * 20, head: k * 25, aL: [-20 - k * 130, 20], aR: [20 + k * 130, -20], lL: [k * 30, k * 10], lR: [-k * 25, 20], y: k * 70, rot: k * 88, dx: k * 40};
	},
	sit: (t: number): Pose => ({...base(t), lL: [-85, 85], lR: [-85, 85], y: 52}),
	cheer: (t: number): Pose => ({...base(t), aL: [150 + S(t, 2, 12), 0], aR: [-150 + S(t, 2, 12), 0], y: -Math.abs(S(t, 2, 6))}),
	read: (t: number): Pose => ({...base(t), aL: [-45, -70], aR: [-45, -70], head: 14}),
};
export type PoseName = keyof typeof poses;
