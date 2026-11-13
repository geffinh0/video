# O Último Pouso — curta 3D (suspense gótico)

Produção 100% por código, num container sem GPU (4 CPUs):
- **Blender 5.3** (`bpy`, Cycles CPU): cenários, personagens e animação gerados por Python em `blender/`.
- **Remotion**: montagem, câmera, chuva/neblina, cor, títulos, créditos e mixagem em `remotion/`.
- **Kokoro-82M** (Apache-2.0): vozes em português (`scripts/voices.py`).
- **Sons**: sintetizados (`scripts/sfx.py`), sem bibliotecas de terceiros.

## Pipeline
1. `roteiro/shots.json` — storyboard técnico (38 planos, 418 s): tempos, falas, sons, movimento de câmera, camadas.
2. `python3 scripts/voices.py` → `assets/audio/voices/` · `python3 scripts/sfx.py` → `assets/audio/sfx/`
3. `python3 scripts/textures.py` → cartas, relógio, manuscrito · `python3 blender/photo.py` → foto do casal
4. `scripts/render_all.sh` → para cada plano: **fundo** (`plate.png`, 48 amostras, 1920×800) e **camada animada** (`layer/####.png`, 12 fps, fundo transparente, cenário como *holdout*). Retomável.
5. `python3 scripts/manifest.py` e `cd remotion && npx remotion render OUltimoPouso ../renders/final/o-ultimo-pouso.mp4`

Prévia de um plano: `python3 blender/shots.py s12 preview` → `renders/preview/s12.png`.

## Módulos Blender (`blender/pouso/`)
`core.py` (render, materiais procedurais, luzes, câmera) · `study.py` (escritório) · `corridor.py` · `exterior.py` (floresta, mansão, estátua) · `raven.py` (corvo articulado: cabeça, bico, asas, cauda) · `human.py` (Arthur e Eleanor, rig hierárquico).
