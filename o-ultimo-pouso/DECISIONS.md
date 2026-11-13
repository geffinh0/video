# Decisões — O Último Pouso

1. **Motor**: Blender 5.3 (módulo `bpy`) com Cycles em CPU (4 núcleos, sem GPU). EEVEE por software (Mesa) foi mais lento (92 s/quadro trivial).
2. **Custo medido**: ~0,8 s por amostra por quadro 1080p + ~8 s de denoise. Render direto de 10.080 quadros levaria dias.
3. **Pipeline multiplano**: cada plano = 1 fundo (plate) em alta qualidade + camadas animadas com fundo transparente a 12 fps; câmera, chuva, neblina, tremor de vela, relâmpagos, cor, grão e barras 2,39:1 na pós (Remotion).
4. **Personagens**: modelados por código (sem artista/biblioteca de assets). Arthur aparece em contraluz, silhueta, perfil, mãos — segue a regra "nunca mostrar tudo de uma vez" e evita rosto de manequim em close.
5. **Vozes**: Kokoro-82M (Apache-2.0), vozes pt-BR: narrador `pm_santa`, Arthur `pm_alex`, Eleanor `pf_dora`, corvo = `pm_santa` processado (grave, rouco). Para o nome no corvo foi usada a grafia "Élenor..." só na síntese.
6. **Rede**: liberados `huggingface.co` e CDNs do HF no ambiente para baixar modelos open source.
7. **Sons**: sintetizados por código (sem bibliotecas externas), para não haver problema de licença.
8. **Duração**: 418 s (6,97 min), 24 fps.
