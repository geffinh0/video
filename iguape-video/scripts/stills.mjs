// Uso: node scripts/stills.mjs <cena> <paragrafo,paragrafo,...>  -> out/stills/sNN-pK.jpg
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
const al = JSON.parse(fs.readFileSync('src/data/alignment.json', 'utf8'));
const [scene, list] = [Number(process.argv[2]), process.argv[3].split(',').map(Number)];
const b = al.blocks.find((x) => x.scene === scene);
fs.mkdirSync('out/stills', {recursive: true});
for (const k of list) {
	const p = b.paragraphs[Math.min(k, b.paragraphs.length - 1)];
	const off = Number(process.argv[4] ?? 1.8);
	const f = Math.round(b.start * 30) + Math.round((p.start - b.start) * 30 + off * 30);
	execFileSync('npx', ['remotion', 'still', 'GuerraDeIguape', `out/stills/s${String(scene).padStart(2, '0')}-p${k}.jpg`, `--frame=${f}`, '--image-format=jpeg', '--jpeg-quality=70'], {stdio: 'ignore'});
	console.log(`s${scene} p${k} frame ${f}`);
}
