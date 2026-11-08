# Arquivos reais que ainda precisam ser fornecidos

O vídeo renderiza completo sem eles: cada foto aparece como um cartão de papel com fita adesiva e o texto "FOTO REAL: ...".
Ao colocar o arquivo em `public/real/` com o nome exato abaixo, o cartão passa a mostrar a foto sozinho (basta renderizar de novo com `npm run render`).

| Arquivo esperado | Onde aparece | Termos de busca sugeridos (Wikimedia Commons) |
|---|---|---|
| `public/real/vista-aerea-iguape.jpg` | Cena 1 (abertura, vira o mapa) | "Iguape aerial view", "Iguape vista aérea", "Iguape SP panorama" |
| `public/real/centro-historico-iguape.jpg` | Cena 8 | "Centro histórico de Iguape", "Iguape historic center" |
| `public/real/igreja-matriz-ruas-antigas.jpg` | Cena 8 (duas vezes) | "Basílica do Bom Jesus de Iguape", "Iguape Igreja Matriz", "Iguape ruas antigas" |
| `public/real/por-do-sol-iguape.jpg` | Cena 10 | "Iguape pôr do sol", "Mar Pequeno Iguape sunset", "Vale do Ribeira" |

Regras: só domínio público, CC0 ou CC BY. Evite CC BY-SA, NC e ND. Anote autor, licença e URL em `out/creditos-imagens.txt`.
Formato: JPG ou PNG, de preferência horizontal e com pelo menos 1280 px de largura.

Observação: não foi possível baixar imagens durante a produção (a rede da sessão não alcançou a Wikimedia), por isso nenhuma foto foi usada.

## Opcional
- `public/audio/musica.mp3`: música de fundo sem direitos autorais. Para usar, renderize com `npx remotion render GuerraDeIguape out/guerra-de-iguape.mp4 --props='{"music":true}'`. O volume cai sozinho durante a fala.
