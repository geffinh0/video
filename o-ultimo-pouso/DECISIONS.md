# Decisões — O Último Pouso

1. **Motor**: Blender 5.3 (módulo `bpy`) com Cycles em CPU (4 núcleos, sem GPU). EEVEE por software (Mesa) foi mais lento (92 s/quadro trivial).
2. **Custo medido**: ~0,8 s por amostra por quadro 1080p + ~8 s de denoise. Render direto de 10.080 quadros levaria dias.
3. **Pipeline multiplano**: cada plano = 1 fundo (plate) em alta qualidade + camadas animadas com fundo transparente a 12 fps; câmera, chuva, neblina, tremor de vela, relâmpagos, cor, grão e barras 2,39:1 na pós (Remotion).
4. **Personagens**: modelados por código (sem artista/biblioteca de assets). Arthur aparece em contraluz, silhueta, perfil, mãos — segue a regra "nunca mostrar tudo de uma vez" e evita rosto de manequim em close.
5. **Vozes**: Kokoro-82M (Apache-2.0), vozes pt-BR: narrador `pm_santa`, Arthur `pm_alex`, Eleanor `pf_dora`, corvo = `pm_santa` processado (grave, rouco). Para o nome no corvo foi usada a grafia "Élenor..." só na síntese.
6. **Rede**: liberados `huggingface.co` e CDNs do HF no ambiente para baixar modelos open source.
7. **Sons**: sintetizados por código (sem bibliotecas externas), para não haver problema de licença.
8. **Duração**: 418 s (6,97 min), 24 fps.
9. **Humanos**: rostos gerados por código parecem manequins; Arthur e Eleanor aparecem sempre em silhueta/contraluz (na camada deles as velas e arandelas não os iluminam), de costas, por cima do ombro ou em perfil escuro.
10. **Planos 2D**: foto do casal (s08), relógio (s10, s32) e retrato torto (s20) são montados no Remotion a partir das texturas (mais nítidos e controláveis que o 3D).
11. **Foto do casal**: desfocada, em sépia, com o rosto de Eleanor apagado pelo tempo (reforça o mistério e esconde o limite dos modelos).
12. **Camadas** em meia resolução (960×400) e 12 fps, ampliadas na montagem: ~4 s/quadro em vez de ~15 s.
13. **Luar**: as luzes do luar são invisíveis para câmera, reflexos e transmissão (senão estouravam através do vidro).

## 14. 30 fps em tudo
A pedido, o filme e as camadas animadas passaram de 24/12 fps para 30 fps (`roteiro/shots.json`, `blender/shots.py`, `remotion/src/timing.ts`).

## 15. Corvo com plumagem em malha
Partículas (hair + instância) ficaram lentas e sem controle de escala. As penas são geradas como uma malha única por
`raven._plumage` (amostra a superfície, deita cada pena na direção desejada). Patas com dedos e garras em skin.

## 16. Humanos: só silhueta, sobre a malha base do MakeHuman (CC0)
Rostos e roupas feitos por código não chegaram a um nível aceitável. Decisão do usuário: Arthur e Eleanor aparecem
apenas em silhueta/sombra. O contorno vem de `pouso/mh.py`, que lê SOMENTE os dados CC0 do MakeHuman/MPFB2
(malha hm08, alvos, esqueleto, pesos); nenhum código do MPFB é executado. Pivôs (empties) dirigem os ossos por
COPY_TRANSFORMS; `shots.silhouette()` troca os materiais por preto fosco sem especular.

## 17. Cenários com peças do Poly Haven (CC0) regraduadas
Móveis, texturas PBR e HDRI vêm do Poly Haven (`scripts/assets.py`, pasta ignorada no git). Cada peça passa por
`core.asset(..., tint, value, sat)` para entrar na paleta do filme. Arquitetura (escritório, corredor, mansão),
corvo, carta, retrato, luz e câmera são desenho próprio. A mansão foi redesenhada (torre com mansarda, torreão,
bay window, portão de ferro).

## 18. Render distribuído
`scripts/worker.sh <shots>` renderiza camadas em outra máquina, codifica em VP9 com alfa (`layers_enc/<shot>.webm`)
e publica no branch. `scripts/unpack_layers.sh` devolve os PNGs para a montagem. Fundos são renderizados localmente.
