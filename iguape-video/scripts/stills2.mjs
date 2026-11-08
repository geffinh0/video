// Uso: node scripts/stills2.mjs "1:0,3;2:1,4" [offset-s]  -> out/stills/sNN-pK.jpg (bundle único)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
const al = JSON.parse(fs.readFileSync('src/data/alignment.json', 'utf8'));
const off = Number(process.argv[3] ?? 2);
const plan = process.argv[2].split(';').map((x) => { const [s, l] = x.split(':'); return [Number(s), l.split(',').map(Number)]; });
const serveUrl = await bundle({entryPoint: 'src/index.ts', webpackOverride: (c) => c});
const comp = await selectComposition({serveUrl, id: 'GuerraDeIguape', browserExecutable: '/opt/pw-browsers/chromium'});
fs.mkdirSync('out/stills', {recursive: true});
for (const [scene, ks] of plan) {
	const b = al.blocks.find((x) => x.scene === scene);
	for (const k of ks) {
		const p = b.paragraphs[Math.min(k, b.paragraphs.length - 1)];
		const frame = Math.round(b.start * 30) + Math.round((p.start - b.start) * 30 + off * 30);
		await renderStill({composition: comp, serveUrl, frame, output: `out/stills/s${String(scene).padStart(2, '0')}-p${k}.jpg`, imageFormat: 'jpeg', jpegQuality: 70, browserExecutable: '/opt/pw-browsers/chromium'});
		console.log(`s${scene} p${k} f${frame}`);
	}
}
