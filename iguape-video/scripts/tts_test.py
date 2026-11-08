"""npm run tts:test: 3 trechos x 3 vozes (Kore, Charon, Puck) em out/teste-voz/ (max. 9 pedidos)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_common import *  # noqa: F401,F403
import tts_provider

VOICES = ["Kore", "Charon", "Puck"]


def excerpts():
    sc = {s["id"]: s["paragraphs"] for s in load_script()}
    return {
        "cena01-abertura": (sc[1][0:3], STYLE),
        "cena05-acao": (sc[5][12:17], STYLE_TENSE),
        "cena10-encerramento": (sc[10][-3:], STYLE),
    }


def main():
    cfg = load_env()
    if not cfg["has_key"]:
        sys.exit("GEMINI_API_KEY ausente. Copie .env.example para .env e preencha.")
    out = ROOT / "out/teste-voz"
    out.mkdir(parents=True, exist_ok=True)
    lim = Limiter(cfg)
    for name, (paras, style) in excerpts().items():
        text = f"\n\n{PAUSE}\n\n".join(pronuncia(p) for p in paras)
        for v in VOICES:
            f = out / f"{name}__{v}.wav"
            if f.exists():
                continue
            print(f"gerando {f.name}", flush=True)
            try:
                wav = call_with_retry(lim, tts_provider.synthesize, text, v, style, cfg["model"])
            except QuotaError:
                print(LIMIT_MSG.replace("npm run tts", "npm run tts:test"))
                return
            f.write_bytes(wav)
    print("Pronto. Ouça os arquivos em out/teste-voz/ e defina GEMINI_VOICE no .env.")


main()
