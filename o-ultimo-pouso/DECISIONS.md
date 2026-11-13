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
