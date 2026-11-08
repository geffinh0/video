# A Guerra de Iguape — vídeo animado em recortes de papel (Remotion)

Resultado: `out/guerra-de-iguape.mp4` (1920×1080, 30 fps, H.264, com narração), `out/thumbnail.png`, `out/descricao.txt`, `out/creditos-imagens.txt`.

## Comandos
| Comando | O que faz |
|---|---|
| `npm run preview` | Remotion Studio (composições `GuerraDeIguape`, `Thumbnail`, `Playground`) |
| `npm run render` | Render final em `out/guerra-de-iguape.mp4` |
| `npm run tts` | Gera a narração (ElevenLabs por padrão, retomável; usa `.env`) |
| `npm run align` | Normaliza o áudio e gera `src/data/alignment.json` e `durations.json` |
| `npm run tts:test` | Teste de vozes (Gemini; ver DECISIONS.md) |
| `npx remotion still Thumbnail out/thumbnail.png` | Gera a thumbnail |

## Trocar a voz
No `.env`: `ELEVENLABS_VOICE_ID` (e `ELEVENLABS_STABILITY`, `ELEVENLABS_STYLE`, `ELEVENLABS_SPEED`). Apague `public/audio/raw/*.wav` e `tts-state.json`, rode `npm run tts` e `npm run align`, depois `npm run render`.
Para usar o Gemini: `TTS_PROVIDER=gemini` e `GEMINI_TTS_MODEL` com um modelo de voz válido.

## Trocar as fotos
Coloque os arquivos de `ASSETS_NEEDED.md` em `public/real/` e rode `npm run render`.

## Estrutura
- `src/cutout/`: kit de recortes (peças de papel com contorno e sombra dura, movimento em passos de 3 frames, câmera, rótulos).
- `src/characters/`: `Puppet` articulado, poses e elenco. `src/props/`: navios, canhão, casas, árvores, fogo etc.
- `src/scenes/Scene1..10.tsx`: as 10 cenas; elas leem os tempos reais de `src/data/alignment.json` (cada elemento entra no parágrafo da narração).
- `src/data/script.json`: roteiro condensado; `script.full.json`: roteiro original completo.
