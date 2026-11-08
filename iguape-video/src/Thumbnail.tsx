import React from 'react';
import {AbsoluteFill} from 'remotion';
import {C, SHADOW, sans, serif} from './cutout/theme';
import {Label} from './cutout/Paper';
import {Puppet} from './characters/Puppet';
import {cast} from './characters/cast';
import {Church, Cannon, Tree} from './props';
import {Table, Finish} from './Table';
import {CoastMap, COAST} from './scenes/shared';

export const Thumbnail: React.FC = () => (
	<AbsoluteFill style={{background: C.dark}}>
		<div style={{width: 1920, height: 1080, transform: 'scale(0.66667)', transformOrigin: '0 0', position: 'absolute', left: 0, top: 0}}>
			<Table base="#1A1512" sheet="#D8C08D" sheet2="#9C8A62" />
			<CoastMap at={-100} places={['iguape', 'saoVicente']} />
			<Church x={COAST.iguape[0] + 60} y={COAST.iguape[1] + 4} s={0.5} />
			<Tree x={640} y={430} s={0.9} />
			<Cannon x={1120} y={880} s={1.1} fire={1} />
			<Puppet x={300} y={1020} s={1.55} look={cast.pero} pose="aim" seed={2} hold={20} />
			<Puppet x={1640} y={1020} s={1.55} look={cast.espanhol} pose="shoot" seed={3} flip hold={20} />
			<div style={{position: 'absolute', left: 0, right: 0, top: 36, textAlign: 'center', fontFamily: serif, fontWeight: 900, fontSize: 196, lineHeight: 0.95, color: C.white, letterSpacing: 2, WebkitTextStroke: `14px ${C.ink}`, paintOrder: 'stroke fill', filter: SHADOW, transform: 'rotate(-2deg)'}}>UMA GUERRA<br />NO BRASIL?!</div>
			<Label x={960} y={960} text="1534 – 1536" at={-100} size={110} fill={C.terra} color={C.white} rot={-2} />
			<Finish vignette={0.5} />
		</div>
	</AbsoluteFill>
);
