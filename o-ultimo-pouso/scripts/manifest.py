"""Lista o que já foi renderizado (fundos e quadros de camada) para a montagem usar só o que existe."""
import json, os
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sc = R / "renders/scenes"; out = {}
if sc.exists():
    for d in sorted(sc.iterdir()):
        lay = d / "layer"
        out[d.name] = {"plate": (d / "plate.png").exists(), "layer": len(list(lay.glob("*.png"))) if lay.exists() else 0}
(R / "remotion/src/data/manifest.json").write_text(json.dumps(out, indent=1))
import shutil
shutil.copy(R / "roteiro/shots.json", R / "remotion/src/data/shots.json")
shutil.copy(R / "assets/audio/voices/durations.json", R / "remotion/src/data/voices.json")
print(sum(1 for v in out.values() if v["plate"]), "fundos;", sum(v["layer"] for v in out.values()), "quadros de camada")
