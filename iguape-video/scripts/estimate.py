"""Gera durations.estimated.json (~2,5 palavras/s) enquanto não há áudio real."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tts_common import ROOT, load_script
t, sc = 0.0, {}
for s in load_script():
    words = sum(len(p.split()) for p in s["paragraphs"])
    d = words / 2.5 + 0.4 * len(s["paragraphs"])
    sc[s["id"]] = {"start": round(t, 3), "end": round(t + d, 3)}
    t += d + 0.8
(ROOT / "src/data/durations.estimated.json").write_text(json.dumps({"source": "estimated", "fps": 30, "total": round(t, 3), "scenes": sc}, indent=1))
print(f"estimado: {t/60:.1f} min")
