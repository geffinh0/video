# O REFLEXO — plano de produção

## Ambiente (analisado em 14/11/2026)
- 4 núcleos de CPU, 15 GB de RAM, sem GPU, ~17 GB livres em disco. O ambiente reinicia a cada ~30 min:
  todo trabalho longo precisa ser retomável (salvar por quadro/bloco).
- Rede: Hugging Face liberado; GitHub (clone) funciona; sites de banco de vídeo não estão liberados.
- Já instalados: Remotion 4 (projeto anterior), ffmpeg, Kokoro TTS (vozes pt-BR, Apache-2.0), numpy/scipy.
- **Geração de vídeo por IA (Wan, LTX, Hunyuan…): inviável aqui** — exigem GPU; em CPU levariam dias por segundo.
  Não vou simular isso. O movimento real vem de animação facial por keypoints (abaixo) e de técnicas de found footage.

## Ferramentas abertas escolhidas
| Função | Ferramenta | Licença |
|---|---|---|
| Imagens (protagonista, banheiro, mão) | Stable Diffusion XL 1.0 + LCM-LoRA (4–8 passos, roda em CPU) | CreativeML OpenRAIL++-M |
| Animação do rosto (piscar, olhar, sorriso, cabeça) | LivePortrait (KlingTeam/KwaiVGI) — edição de expressão por keypoints, sem vídeo-guia | MIT (código e pesos) |
| Detecção de rosto | não uso o insightface (licença não comercial): o recorte do rosto é conhecido porque eu gero a imagem; uso só o `landmark.onnx` do LivePortrait | MIT |
| Voz (sussurro) | Kokoro-82M, voz pf_dora + cadeia ffmpeg | Apache-2.0 |
| Sons | sintetizados em numpy/scipy (sem bibliotecas de terceiros) | próprio |
| Montagem e efeitos | Remotion + React + TypeScript (SVG/Canvas/CSS) | Remotion (uso individual gratuito) |

## Estratégia do reflexo (o coração do filme)
- **Uma identidade só.** A protagonista nasce de UM retrato-mestre gerado. Todo plano de rosto (real e reflexo)
  é animado pelo LivePortrait a partir desse mesmo retrato → aparência idêntica garantida; a diferença é só comportamento.
- **Duas trilhas independentes por plano:** "real" e "reflexo" são renderizados separadamente com curvas de animação
  próprias (piscar, direção do olhar, sorriso, giro de cabeça). O reflexo é espelhado e composto dentro da máscara
  do espelho, com tinta do vidro, reflexo especular, sujeira e embaçado. Assim o atraso, o olhar para a câmera e o
  sorriso são movimentos reais do rosto, não um efeito de espelhamento.
- **Câmera de segurança:** taxa de quadros baixa real (3–5 fps), como em CCTV de verdade. A entrada/saída da
  protagonista é feita com poses geradas (mesma roupa/cabelo, img2img a partir do retrato) exibidas nessa cadência,
  com ruído, compressão e ângulo alto — que também escondem pequenas diferenças entre poses.
- **Mão no vidro e "AGORA É MINHA VEZ":** mão gerada como camada própria (SDXL), aproximada do vidro em Remotion;
  as letras são reveladas por traço SVG animado na máscara de embaçado (o vidro "limpa" onde o dedo passa).
  Fica honesto: é composição em camadas, sem dedos articulados.

## Arquitetura
```
o-reflexo/
  gen/            scripts Python: retrato, cenários, poses, animação LivePortrait, sons, voz
  assets/         imagens, sequências PNG (rosto real / reflexo), áudio (versionados quando pequenos)
  remotion/src/
    Root.tsx
    compositions/TheReflection.tsx
    scenes/ RecoveredArchive, FirstAnomaly, Observation, TheSmile, FinalRecording, LastFootage
    components/ VHSOverlay, SecurityCam (timestamp+lowfps+compressão), PhoneCam (tremor+autofoco+exposição),
                TrackingDistortion, MirrorComposite, FogWriting, Glitch, AudioLayer
```

## Lista de assets
1. Retrato-mestre da protagonista (frontal, luz de banheiro) + 2 ângulos (¾ esq./dir.).
2. Banheiro: plano CCTV alto (vazio), plano de celular frente ao espelho, piso (câmera caída).
3. Poses CCTV: entrando, diante do espelho, saindo (4–6 imagens).
4. Sequências LivePortrait: S02 (piscar real × piscar atrasado), S03 (olha a porta × reflexo olha a câmera),
   S04 (séria × sorriso lento), S05 (sussurro × olhar fixo), S05 fim e S06 (reflexo sozinho sorrindo).
5. Mão aberta (camada com alfa).
6. Sons: ventilação, zumbido elétrico 60 Hz, ruído de sala, chiado VHS, estalos, respiração, queda do celular,
   grave discreto, interferência digital; voz sussurrada da fala.

## Plano de produção (etapas com checagem)
1. Instalar dependências e testar em CPU: 1 retrato SDXL + 1 animação curta LivePortrait (piscar/sorrir).
   **Checkpoint com você: aprovar o rosto da protagonista antes de produzir o resto.**
2. Cenários e poses; máscaras do espelho.
3. Animações faciais de todas as sequências (retomável por quadro).
4. Sons e voz.
5. Remotion: componentes de dispositivo, cenas, ritmo, áudio sincronizado.
6. Prévia → revisão (continuidade, legibilidade, sincronia, artefatos) → render final.

Duração-alvo: ~2:30 (4.500 quadros a 30 fps).
