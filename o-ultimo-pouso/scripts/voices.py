"""Gera todas as falas com Kokoro (open source, Apache-2.0) e aplica o tratamento de cada personagem.
Saída: assets/audio/voices/<id>.wav (48 kHz, mono) e assets/audio/voices/durations.json"""
import json, subprocess, sys
from pathlib import Path
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "assets/voices/models"
OUT = ROOT / "assets/audio/voices"; OUT.mkdir(parents=True, exist_ok=True)
VOICE = {"N": ("pm_santa", 0.80), "A": ("pm_alex", 0.84), "E": ("pf_dora", 0.82), "C": ("pm_santa", 0.80)}
# filtros ffmpeg por personagem / efeito
FX = {
    "N": "lowpass=f=9000,acompressor=threshold=-20dB:ratio=2,aecho=0.8:0.6:40:0.15",
    "A": "acompressor=threshold=-20dB:ratio=2,aecho=0.8:0.5:30:0.12",
    "E": "highpass=f=120,aecho=0.8:0.7:60|120:0.25|0.15",
    "C": "asetrate=24000*0.88,aresample=24000,acrusher=bits=12:mix=0.10,highpass=f=90,aecho=0.8:0.5:40:0.18",
    "distante": "lowpass=f=2800,aecho=0.8:0.85:120|240:0.45|0.3,volume=0.6",
    "memoria": "lowpass=f=4000,aecho=0.8:0.8:90|180:0.4|0.25",
    "porta": "lowpass=f=1600,aecho=0.8:0.7:50:0.3,volume=0.8",
}

def main():
    data = json.loads((ROOT / "roteiro/falas.json").read_text())["lines"]
    k = Kokoro(str(M / "kokoro-v1.0.onnx"), str(M / "voices-pt.npz"))
    durs = {}
    for ln in data:
        voice, speed = VOICE[ln["who"]]
        a, sr = k.create(ln.get("say", ln["text"]), voice=voice, speed=speed, lang="pt-br")
        raw = OUT / f"_{ln['id']}.wav"; sf.write(raw, a, sr)
        chain = FX[ln["who"]] + ("," + FX[ln["fx"]] if ln.get("fx") else "")
        dst = OUT / f"{ln['id']}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", chain + ",loudnorm=I=-18:TP=-2", "-ar", "48000", "-ac", "1", str(dst)], check=True)
        raw.unlink()
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)]))
        durs[ln["id"]] = round(d, 3)
        print(ln["id"], durs[ln["id"]], "s", flush=True)
    (OUT / "durations.json").write_text(json.dumps(durs, indent=1))

main()
