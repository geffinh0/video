# O Último Pouso — progresso

- [x] Decisões: Blender 3D procedural (filme inteiro), 1080p, vozes open source (Kokoro)
- [x] Falas geradas (34 falas, 81 s) — `scripts/voices.py`
- [x] Roteiro técnico / storyboard: `roteiro/shots.json` (38 planos, 6,97 min)
- [x] Efeitos sonoros sintetizados (42 sons, `scripts/sfx.py`)
- [x] Blender: núcleo, escritório, corredor, exterior, corvo, Arthur, Eleanor, insertos, foto do casal
- [ ] Render dos fundos e camadas (`scripts/render_all.sh`, em andamento; retomável)
- [x] Montagem no Remotion (camadas, câmera, chuva, neblina, cor, título, créditos, mixagem)
- [ ] Render final `renders/final/o-ultimo-pouso.mp4`


## Estado final (14/11)
- Filme completo renderizado: `renders/final/o-ultimo-pouso.mp4` (alta qualidade, 273 MB) e `o-ultimo-pouso-leve.mp4` (72 MB, crf 22).
- 418 s, 1920x1080, 30 fps, AAC 48 kHz. 34 fundos + 21 camadas animadas (7.890 quadros).
- Render final em blocos de 20 s (`scripts/render_final.sh`), retomável: o ambiente reinicia a cada ~30 min.
- Humanos só em silhueta (decisão do usuário); corvo, cenários e mansão refeitos; assets CC0 do Poly Haven e malha MakeHuman.
