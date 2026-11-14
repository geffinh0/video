import React from 'react';

// Vidro do espelho desenhado por cima da imagem-base: moldura fina, brilho diagonal e leve escurecimento.
// Faz o "reflexo" ser lido como reflexo (e não como outra pessoa no cômodo).
export const MirrorGlass: React.FC<{x: number; y: number; w: number; h: number; frame?: string; sheen?: number}> = ({x, y, w, h, frame = 'rgba(215,224,220,0.5)', sheen = 0.22}) => (
	<div style={{position: 'absolute', left: x, top: y, width: w, height: h}}>
		<div style={{position: 'absolute', inset: 0, background: 'rgba(10,20,18,0.12)', mixBlendMode: 'multiply'}} />
		<div style={{position: 'absolute', inset: 0, background: `linear-gradient(115deg, rgba(255,255,255,0) 18%, rgba(255,255,255,${sheen}) 26%, rgba(255,255,255,0) 34%, rgba(255,255,255,0) 60%, rgba(255,255,255,${sheen * 0.6}) 66%, rgba(255,255,255,0) 71%)`, mixBlendMode: 'screen'}} />
		<div style={{position: 'absolute', inset: 0, border: `2px solid ${frame}`, boxShadow: '0 0 6px rgba(0,0,0,0.6), inset 0 0 10px rgba(0,0,0,0.35)'}} />
	</div>
);
