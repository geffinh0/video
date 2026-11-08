"""npm run align: alinha texto e áudio (faster-whisper) e escreve alignment.json e durations.json."""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_common import ROOT, load_script

FPS = 30
PAUSE_PARA, PAUSE_SCENE = 0.4, 0.8


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def dur(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(out)


def silences(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "silencedetect=n=-35dB:d=0.25", "-f", "null", "-"], capture_output=True, text=True)
    return [(float(a), float(b)) for a, b in re.findall(r"silence_start: ([\d.]+)[\s\S]*?silence_end: ([\d.]+)", r.stderr)]


def whisper_words(path):
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(str(path), language="pt", word_timestamps=True)
    return [(norm(w.word), w.start, w.end) for s in segs for w in s.words if norm(w.word)]


def proportional(paras, total):
    """Método de último recurso: divide o tempo pelo número de caracteres."""
    n = sum(len(p) for p in paras)
    t, res = 0.0, []
    for p in paras:
        d = total * len(p) / n
        res.append((t, t + d))
        t += d
    return res


def align_block(wav, paras):
    total = dur(wav)
    try:
        words = whisper_words(wav)
        method = "faster-whisper"
    except Exception as e:  # noqa: BLE001
        print("  whisper falhou:", str(e)[:120])
        words, method = [], "proporcional"
    spans = []
    if words:
        # casa palavras do texto conhecido com a transcrição (ordem monotônica, janela curta)
        j = 0
        for p in paras:
            toks = [norm(t) for t in p.split() if norm(t)]
            starts, ends = [], []
            for t in toks:
                for k in range(j, min(j + 6, len(words))):
                    if words[k][0] == t:
                        starts.append(words[k][1]); ends.append(words[k][2]); j = k + 1
                        break
            if len(starts) >= max(1, len(toks) // 2):
                spans.append((starts[0], ends[-1]))
            else:
                spans.append(None)
        if any(s is None for s in spans):
            method = "proporcional"
    if not words or any(s is None for s in spans):
        spans = proportional(paras, total)
    return total, spans, method


def main():
    blocks = json.loads((ROOT / "src/data/blocks.json").read_text())
    raw = ROOT / "public/audio/raw"
    missing = [b["id"] for b in blocks if not (raw / f"{b['id']}.wav").exists()]
    if missing:
        sys.exit(f"Faltam blocos de áudio: {missing}. Rode `npm run tts` (retomável).")
    (ROOT / "public/audio").mkdir(exist_ok=True)
    timeline, t, out_blocks, methods = [], 0.0, [], set()
    prev_scene = None
    scenes = {s["id"]: {"start": None, "end": 0.0} for s in load_script()}
    for b in blocks:
        wav = raw / f"{b['id']}.wav"
        norm_wav = ROOT / f"public/audio/{b['id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11,acompressor=threshold=-18dB:ratio=2", "-ar", "24000", "-ac", "1", str(norm_wav)], check=True)
        total, spans, method = align_block(norm_wav, b["paragraphs"])
        methods.add(method)
        if prev_scene is not None:
            t += PAUSE_SCENE if b["scene"] != prev_scene else PAUSE_PARA
        out_blocks.append({"id": b["id"], "scene": b["scene"], "file": f"audio/{b['id']}.wav", "start": round(t, 3), "duration": round(total, 3),
                           "paragraphs": [{"text": p, "start": round(t + s[0], 3), "end": round(t + s[1], 3)} for p, s in zip(b["paragraphs"], spans)]})
        sc = scenes[b["scene"]]
        sc["start"] = t if sc["start"] is None else sc["start"]
        sc["end"] = t + total
        t += total
        prev_scene = b["scene"]
    d = ROOT / "src/data"
    (d / "alignment.json").write_text(json.dumps({"method": sorted(methods), "blocks": out_blocks}, indent=1, ensure_ascii=False))
    (d / "durations.json").write_text(json.dumps({"source": "audio", "fps": FPS, "total": round(t, 3),
        "scenes": {k: {"start": round(v["start"], 3), "end": round(v["end"], 3)} for k, v in scenes.items()}}, indent=1))
    print("métodos de alinhamento:", methods, "| duração total:", round(t / 60, 1), "min")


main()
