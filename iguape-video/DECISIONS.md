# Decisões

1. **Projeto em `iguape-video/`** dentro do repositório `video`; skills Remotion instaladas na raiz (`.agents/`).
2. **Roteiro** em `src/data/script.json` (texto exato da seção 8), lido por TypeScript e Python.
3. **Blocos de TTS**: 17 blocos de ~800–1.300 caracteres (incluem as marcas `<short pause>`), sem atravessar cenas. `npm run tts` grava `src/data/blocks.json`.
4. **Chave da API**: só em `.env` (ignorado pelo git); passada explicitamente ao SDK, nunca impressa. A chave foi colada no chat pelo usuário: recomendável revogá-la e criar outra depois do projeto.
5. **BLOQUEIO TTS (2026-11-08)**: com a chave fornecida (prefixo `AQ.`, não `AIza`), `models.list` funciona mas não lista nenhum modelo de voz. Chamadas a `gemini-3.8-flash-tts`, `3.7/3.6/3.5/3.1-flash-tts`, `gemini-2.5-flash(-preview)-tts` retornam 404; o erro sugere "Did you mean 'gemini-3.8-flash-tts'?" mas o mesmo nome também dá 404. Hipóteses: a chave/projeto não tem acesso a TTS (ou é de outro tipo, ex.: Vertex Express), ou o nome mudou. A documentação (ai.google.dev) está bloqueada pelo proxy desta sessão, então não foi possível conferir. Ação: o projeto segue com `durations.estimated.json` (≈2,5 palavras/s). Quando o usuário informar um modelo válido em `GEMINI_TTS_MODEL` (ou outra chave), `npm run tts:test` retoma.
6. **Termos de uso**: antes de monetizar, conferir os termos de uso comercial da API do Gemini; no plano gratuito o conteúdo enviado pode ser usado pelo Google. Só o texto do roteiro é enviado.
