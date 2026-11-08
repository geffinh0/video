import {C} from '../cutout/theme';
import {Look} from './Puppet';

export const cast: Record<string, Look> = {
	moschera: {skin: C.skin1, shirt: '#B5482F', pants: '#3E3A36', hair: '#3a2a1c', hat: 'barrete', hatColor: '#C98B2B', boots: '#4A3626', sash: C.ocre, collar: true},
	cosme: {skin: C.skin2, shirt: '#2F2B33', pants: '#2F2B33', hair: '#4a3b2f', beard: true, hat: 'hood', hatColor: '#2F2B33', cape: '#3B3441', boots: '#2B2622', item: 'scroll'},
	martim: {skin: C.skin1, shirt: '#2F4B7C', pants: '#2A2F3E', hair: '#5a4631', hat: 'none', cape: '#243C66', collar: true, item: 'sword', boots: '#3A2E26', sash: C.gold},
	pero: {skin: C.skin2, shirt: '#8A7A5A', pants: '#4B4338', hat: 'morrion', item: 'arcabuz', boots: '#3A2E26', sash: C.pt, beard: true, hair: '#3a2a1c'},
	// Povos indígenas: representação sóbria (tecido simples, cabelo liso); sem cocar de planícies norte-americanas.
	indio: {skin: C.skin3, shirt: '#8C5A36', pants: '#8C5A36', hair: '#1B1612', long: true, bare: true, item: 'bow', boots: C.skin3},
	guia: {skin: C.skin4, shirt: '#7A4A2E', pants: '#7A4A2E', hair: '#1B1612', long: true, bare: true, item: 'none', boots: C.skin4},
	marinheiro: {skin: C.skin2, shirt: C.white, pants: '#52504A', hair: '#3a2a1c', hat: 'barrete', hatColor: C.pt, sash: C.red, boots: '#4A3626'},
	espanhol: {skin: C.skin1, shirt: C.es, pants: '#3E3A36', hair: '#2a1c12', hat: 'wide', hatColor: C.wood, item: 'arcabuz', boots: '#4A3626'},
	pesquisador: {skin: C.skin3, shirt: '#E4DDCB', pants: '#3A4A5A', hair: '#241a14', hat: 'none', item: 'book', boots: '#2B2622', long: false},
	pesquisadora: {skin: C.skin2, shirt: '#7B8FA6', pants: '#3A4A5A', hair: '#2a1c12', long: true, item: 'none', boots: '#2B2622'},
};
const shirts = ['#8A7A5A', '#A3262A', '#2F4B7C', '#5E6B3A', '#7A5A3A', '#6B5A7A', '#B5801F', '#3E5E66'];
export const soldier = (i: number): Look => ({skin: [C.skin1, C.skin2, C.skin3][i % 3], shirt: shirts[i % shirts.length], pants: '#4B4338', hat: 'morrion', item: 'arcabuz', boots: '#3A2E26', sash: C.pt});
