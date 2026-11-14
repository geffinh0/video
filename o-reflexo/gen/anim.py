"""Renderiza as sequências de rosto animado de cada plano (LivePortrait por keypoints).
Cada plano: imagem-base + rostos (caixa + curvas de animação próprias) + fps + duração.
Saída: renders/frames/<plano>/NNNN.jpg (quadro inteiro). Retomável: pula quadros existentes; cache por parâmetros.
Uso: python3 gen/anim.py <plano> [<plano> ...]"""
import os, sys, json, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
from scipy.io import wavfile
from face import Face
from src.utils.crop import paste_back

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PL = f"{ROOT}/assets/plates"; OUT = f"{ROOT}/renders/frames"; AUD = f"{ROOT}/assets/audio"

# ---------- curvas ----------
def bump(t, c, w):            # pulso suave centrado em c, largura total w
    x = (t - c) / (w / 2); return max(0.0, 1 - x * x) ** 1.5 if abs(x) < 1 else 0.0
def blinks(t, times, w=0.24, depth=1.0):
    return min(1.0, sum(bump(t, c, w) for c in times)) * depth
def ease(t, a, b):
    x = min(1, max(0, (t - a) / (b - a))); return x * x * (3 - 2 * x)
def hold(t, segs):            # segs: [(t0, t1, valor_de, valor_ate)] interpolados com ease, fora deles 0
    v = 0.0
    for a, b, v0, v1 in segs:
        if a <= t: v = v0 + (v1 - v0) * ease(t, a, b)
    return v
def wobble(t, seed, amp, sp=0.4):   # micro movimento natural de cabeça
    r = np.random.default_rng(seed); ph = r.uniform(0, 6.28, 3); fr = r.uniform(0.6, 1.4, 3) * sp
    return amp * sum(math.sin(2 * math.pi * f * t + p) for f, p in zip(fr, ph)) / 3
_env = {}
def speech(t, name, at, gain=1.0):  # abertura de boca a partir do envelope do áudio da fala
    if name not in _env:
        sr, a = wavfile.read(f"{AUD}/{name}.wav"); a = a.astype(np.float32); a = a.mean(1) if a.ndim > 1 else a
        hop = sr // 30; e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2)) for i in range(0, len(a), hop)]); e = e / (e.max() + 1e-6)
        _env[name] = e
    e = _env[name]; i = int((t - at) * 30)
    return float(np.clip(e[i] * 1.3 - 0.12, 0, 1)) * gain if 0 <= i < len(e) else 0.0

# ---------- planos ----------
# Cada rosto: dict(box=(x0,y0,x1,y1), fn=lambda t: dict(blink=, smile=, gaze=(x,y), mouth=, yaw=, pitch=, roll=, brow=))
SHOTS = {}

def shot(name, plate, fps, dur, faces):
    SHOTS[name] = dict(plate=plate, fps=fps, dur=dur, faces=faces)

def render(name):
    S = SHOTS[name]; d = f"{OUT}/{name}"; os.makedirs(d, exist_ok=True)
    base = cv2.cvtColor(cv2.imread(f"{PL}/{S['plate']}.png"), cv2.COLOR_BGR2RGB)
    n = int(round(S["dur"] * S["fps"]))
    a, b = (int(x) for x in os.environ.get("RANGE", f"0:{n}").split(":"))
    todo = [i for i in range(max(0, a), min(n, b)) if not os.path.exists(f"{d}/{i:04d}.jpg")]
    if not todo: print("SKIP", name); return
    F = [Face(base, f["box"]) for f in S["faces"]]
    cache = [dict() for _ in F]; t0 = time.time()
    for i in todo:
        t = i / S["fps"]; img = base.copy()
        for k, (fc, f) in enumerate(zip(S["faces"], F)):
            p = fc["fn"](t); p.setdefault("gaze", (0.0, 0.0))
            key = tuple(round(float(v), 3) if not isinstance(v, tuple) else tuple(round(float(x), 2) for x in v) for v in (p.get("blink", 0), p.get("smile", 0), p["gaze"], p.get("mouth", 0), p.get("yaw", 0), p.get("pitch", 0), p.get("roll", 0), p.get("brow", 0)))
            if key not in cache[k]: cache[k][key] = f.frame(crop_only=True, **p)
            img = paste_back(cache[k][key], f.M_c2o, img, f.mask_ori)
        cv2.imwrite(f"{d}/{i:04d}.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
        if i % 15 == 0: print(name, i, "/", n, round(time.time() - t0), "s", flush=True)
    if "RANGE" not in os.environ: json.dump(dict(count=n, fps=S["fps"]), open(f"{d}/info.json", "w"))
    print("DONE", name, round(time.time() - t0), "s", flush=True)

import shots_def  # noqa: E402  (define os planos chamando shot(...))
shots_def.define(shot, dict(bump=bump, blinks=blinks, ease=ease, hold=hold, wobble=wobble, speech=speech))

if __name__ == "__main__":
    for nm in (sys.argv[1:] or list(SHOTS)): render(nm)
