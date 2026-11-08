import React, {useEffect, useMemo, useState} from 'react';
import {Img, cancelRender, continueRender, delayRender, staticFile} from 'remotion';
import {C, SHADOW, sans, serif} from './theme';
import {P, ell, rect, rough, toPath} from './noise';
import {Enter} from './motion';

/** Peça de papel em SVG: contorno claro de recorte + preenchimento chapado com borda irregular (seed fixo). */
export const CutPath: React.FC<{pts: P[]; fill: string; seed?: number; amp?: number; outline?: string | null; sw?: number; opacity?: number}> = ({pts, fill, seed = 1, amp = 2.2, outline = C.outline, sw = 7, opacity = 1}) => {
	const d = useMemo(() => toPath(rough(pts, seed, amp)), [JSON.stringify(pts), seed, amp]); // eslint-disable-line react-hooks/exhaustive-deps
	return <path d={d} fill={fill} stroke={outline ?? 'none'} strokeWidth={outline ? sw : 0} strokeLinejoin="round" paintOrder="stroke" opacity={opacity} />;
};

/** Linhas de detalhe (janelas, tábuas). */
export const Ink: React.FC<{d: string; w?: number; o?: number; c?: string}> = ({d, w = 2.5, o = 0.45, c = C.ink}) => (
	<path d={d} stroke={c} strokeWidth={w} fill="none" opacity={o} strokeLinecap="round" />
);

/** Contêiner de peça posicionada: svg 1x1 com overflow visível e sombra dura. */
export const Piece: React.FC<{x: number; y: number; s?: number; flip?: boolean; rot?: number; shadow?: boolean; children: React.ReactNode; z?: number}> = ({x, y, s = 1, flip, rot = 0, shadow = true, children, z}) => (
	<svg width={1} height={1} style={{position: 'absolute', left: x, top: y, overflow: 'visible', filter: shadow ? SHADOW : undefined, zIndex: z}}>
		<g transform={`rotate(${rot}) scale(${flip ? -s : s} ${s})`}>{children}</g>
	</svg>
);

/** Folha/cartão retangular de papel com texto opcional. */
export const Sheet: React.FC<{x: number; y: number; w: number; h: number; fill?: string; rot?: number; seed?: number; amp?: number; children?: React.ReactNode; tape?: boolean}> = ({x, y, w, h, fill = C.parch2, rot = 0, seed = 3, amp = 3, children, tape}) => (
	<div style={{position: 'absolute', left: x, top: y, width: w, height: h, transform: `rotate(${rot}deg)`, filter: SHADOW}}>
		<svg width={w} height={h} style={{position: 'absolute', overflow: 'visible'}}>
			<CutPath pts={rect(w, h)} fill={fill} seed={seed} amp={amp} />
		</svg>
		{children}
		{tape && <Tape x={w / 2 - 55} y={-18} rot={-4} />}
	</div>
);

export const Tape: React.FC<{x: number; y: number; rot?: number; w?: number}> = ({x, y, rot = 0, w = 110}) => (
	<div style={{position: 'absolute', left: x, top: y, width: w, height: 34, background: 'rgba(235,205,120,0.78)', transform: `rotate(${rot}deg)`, boxShadow: '1px 2px 0 rgba(43,38,34,0.18)'}} />
);

/** Etiqueta de papel que entra com quique. */
export const Label: React.FC<{x: number; y: number; text: string; sub?: string; at: number; until?: number; rot?: number; fill?: string; color?: string; size?: number; kind?: 'drop' | 'left' | 'right' | 'up' | 'pop'; seed?: number; serifFont?: boolean}> = ({
	x, y, text, sub, at, until, rot = -2, fill = C.parch2, color = C.ink, size = 44, kind = 'drop', seed = 7, serifFont,
}) => {
	const w = Math.max(text.length, (sub ?? '').length * 0.62) * size * 0.54 + 52;
	const h = size * 1.45 + (sub ? size * 0.78 : 0);
	return (
		<Enter at={at} until={until} kind={kind} seed={seed}>
			<Sheet x={x - w / 2} y={y - h / 2} w={w} h={h} fill={fill} rot={rot} seed={seed}>
				<div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color, textAlign: 'center', lineHeight: 1.1}}>
					<div style={{fontFamily: serifFont ? serif : sans, fontWeight: 800, fontSize: size}}>{text}</div>
					{sub && <div style={{fontFamily: sans, fontWeight: 700, fontSize: size * 0.5, opacity: 0.8, marginTop: 4}}>{sub}</div>}
				</div>
			</Sheet>
		</Enter>
	);
};

/** Cartão de foto: usa public/real/<file> se existir; senão mostra o quadro de substituição (fita adesiva + texto). */
export const PhotoCard: React.FC<{x: number; y: number; w?: number; h?: number; rot?: number; desc: string; file?: string; seed?: number}> = ({x, y, w = 560, h = 380, rot = -3, desc, file, seed = 11}) => {
	const [found, setFound] = useState(false);
	const [handle] = useState(() => (file ? delayRender(`foto ${file}`) : null));
	useEffect(() => {
		if (!file || handle === null) return;
		fetch(staticFile(`real/${file}`), {method: 'HEAD'})
			.then((r) => setFound(r.ok && (r.headers.get('content-type') ?? '').startsWith('image/')))
			.catch(() => setFound(false))
			.finally(() => continueRender(handle));
	}, [file, handle]);
	return (
		<Sheet x={x} y={y} w={w} h={h} rot={rot} seed={seed} fill={C.white} tape>
			<div style={{position: 'absolute', left: 22, top: 22, right: 22, bottom: 22, background: '#CFC6AE', border: found ? 'none' : `3px dashed ${C.ink}55`, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: found ? 0 : 24, boxSizing: 'border-box', overflow: 'hidden'}}>
				{found && file ? <Img src={staticFile(`real/${file}`)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'sepia(0.18) saturate(0.92)'}} />
					: <div style={{fontFamily: sans, fontWeight: 800, fontSize: 30, color: C.ink, opacity: 0.75, lineHeight: 1.2}}>FOTO REAL:<br />{desc}</div>}
			</div>
		</Sheet>
	);
};

/** Borda rasgada horizontal (faixa de papel) para montar fundos em camadas. */
export const TornStrip: React.FC<{y: number; h: number; fill: string; seed?: number; amp?: number; x?: number; w?: number; top?: boolean}> = ({y, h, fill, seed = 5, amp = 16, x = -80, w = 2080, top = true}) => {
	const pts = useMemo(() => {
		const a: P[] = [];
		const n = Math.ceil(w / 38);
		for (let i = 0; i <= n; i++) a.push([i * 38, (top ? 0 : h) + (Math.sin(i * 1.7 + seed) * 0.5 + Math.sin(i * 0.43 + seed * 2)) * amp * 0.5 + ((i * 7919 + seed * 31) % 11 - 5) * (amp / 8)]);
		if (top) { a.push([w, h], [0, h]); } else { a.push([w, 0], [0, 0]); }
		return a;
	}, [w, h, fill, seed, amp, top]);
	return (
		<svg width={w} height={h + 40} style={{position: 'absolute', left: x, top: y, overflow: 'visible', filter: 'drop-shadow(0px -4px 0 rgba(43,38,34,0.22))'}}>
			<path d={toPath(pts)} fill={fill} stroke={C.outline} strokeWidth={5} paintOrder="stroke" strokeLinejoin="round" />
		</svg>
	);
};

export const Circle: React.FC<{x: number; y: number; r: number; fill: string; seed?: number}> = ({x, y, r, fill, seed = 2}) => (
	<Piece x={x} y={y}><CutPath pts={ell(r, r, 0, 0, 16)} fill={fill} seed={seed} /></Piece>
);
