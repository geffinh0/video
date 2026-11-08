import {loadFont as loadSerif} from '@remotion/google-fonts/Alegreya';
import {loadFont as loadSans} from '@remotion/google-fonts/NunitoSans';

export const serif = loadSerif('normal', {weights: ['700', '900']}).fontFamily;
export const sans = loadSans('normal', {weights: ['700', '800']}).fontFamily;

export const C = {
	parch: '#EAD9B5', parch2: '#F1E4C4', sand: '#D8C08D', ocre: '#C98B2B', terra: '#B5482F',
	sea: '#1F5C66', sea2: '#2A7380', forest: '#3D5A3A', forest2: '#547A4E', ink: '#2B2622',
	pt: '#2F4B7C', es: '#A3262A', ind: '#B7873A', outline: '#F6EDD6', dark: '#1D1A17',
	wood: '#7B5233', wood2: '#9A6B40', stone: '#8A8478', gold: '#E0B22E', red: '#C0392B',
	skin1: '#E8B98F', skin2: '#C98B5E', skin3: '#9A6240', skin4: '#7A4A2E', white: '#F4ECD8',
};
export const SHADOW = 'drop-shadow(7px 9px 0 rgba(43,38,34,0.27))';
export const W = 1920;
export const H = 1080;
