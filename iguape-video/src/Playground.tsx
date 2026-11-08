import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C} from './cutout/theme';
import {TornStrip, Label} from './cutout/Paper';
import {Puppet} from './characters/Puppet';
import {cast, soldier} from './characters/cast';
import {Caravel, Cannon, House, Church, Tree, Mangrove, Book, Fire, Canoe, FrenchShip, Crate, Gold, Smoke} from './props';
import {PoseName} from './characters/poses';
import {Table} from './Table';

const list: [string, PoseName][] = [['moschera', 'talk'], ['cosme', 'cross'], ['martim', 'point'], ['pero', 'aim'], ['indio', 'bow'], ['guia', 'walk'], ['marinheiro', 'row'], ['espanhol', 'shoot'], ['pesquisador', 'read'], ['pesquisadora', 'idle']];

export const Playground: React.FC = () => (
	<AbsoluteFill>
		<Table />
		{list.map(([k, p], i) => <Puppet key={k} x={110 + (i % 5) * 380} y={(i < 5 ? 420 : 800)} s={1.0} look={cast[k]} pose={p} seed={i + 1} />)}
		{[0, 1, 2, 3].map((i) => <Puppet key={`s${i}`} x={1480 + i * 105} y={250} s={0.6} look={soldier(i)} pose="walk" seed={30 + i} />)}
		<Caravel x={300} y={110} s={0.4} />
		<FrenchShip x={900} y={130} s={0.35} />
		<Cannon x={1250} y={100} s={0.8} fire={1} />
		<House x={1500} y={130} s={0.7} /><Church x={1700} y={150} s={0.45} />
		<Tree x={1830} y={150} s={0.6} /><Mangrove x={1380} y={150} s={0.6} />
		<Book x={60} y={160} s={0.4} open /><Fire x={600} y={100} s={0.8} /><Canoe x={700} y={130} s={0.4} /><Crate x={800} y={120} s={0.8} /><Gold x={1000} y={100} s={1.5} /><Smoke x={1100} y={100} />
		<Label x={960} y={1030} text="Playground — recortes" at={0} />
	</AbsoluteFill>
);
