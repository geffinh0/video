"""npm run tts: gera os blocos de narração; retomável e respeitando a cota diária."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_common import *  # noqa: F401,F403
import tts_provider


def main():
    cfg = load_env()
    if not cfg["has_key"]:
        sys.exit("GEMINI_API_KEY ausente. Copie .env.example para .env e preencha.")
    raw = ROOT / "public/audio/raw"
    raw.mkdir(parents=True, exist_ok=True)
    blocks = make_blocks()
    (ROOT / "src/data/blocks.json").write_text(json.dumps(blocks, indent=2, ensure_ascii=False))
    lim = Limiter(cfg)
    pending = 0
    for b in blocks:
        h = block_hash(b["text"], cfg["voice"], b["style"], cfg["model"])
        f = raw / f"{b['id']}.wav"
        if f.exists() and lim.state["done"].get(b["id"]) == h:
            continue
        pending += 1
        print(f"[{b['id']}] cena {b['scene']} ({len(b['text'])} chars)", flush=True)
        try:
            wav = call_with_retry(lim, tts_provider.synthesize, b["text"], cfg["voice"], b["style"], cfg["model"])
        except QuotaError:
            print(LIMIT_MSG)
            return
        f.write_bytes(wav)
        lim.state["done"][b["id"]] = h
        save_state(lim.state)
    print("Todos os blocos prontos. Rode `npm run align`." if not pending or True else "")


main()
