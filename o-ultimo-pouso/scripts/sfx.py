"""Efeitos sonoros e trilha sintetizados (originais, sem licença de terceiros).
Saída: assets/audio/sfx/<nome>.wav (48 kHz, estéreo, 16 bits)."""
import numpy as np, soundfile as sf
from pathlib import Path
from scipy import signal

SR = 48000
OUT = Path(__file__).resolve().parent.parent / "assets/audio/sfx"; OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1897)

def t(d): return np.arange(int(d * SR)) / SR
def white(d): return rng.standard_normal(int(d * SR))
def pink(d):
    w = np.fft.rfft(white(d)); f = np.fft.rfftfreq(int(d * SR), 1 / SR); f[0] = f[1]
    return np.fft.irfft(w / np.sqrt(f), int(d * SR))
def brown(d): x = np.cumsum(white(d)); return x - signal.savgol_filter(x, 4801, 1) if len(x) > 5000 else x
def bp(x, lo, hi, o=4): return signal.sosfilt(signal.butter(o, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f, o=4): return signal.sosfilt(signal.butter(o, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f, o=4): return signal.sosfilt(signal.butter(o, f, "highpass", fs=SR, output="sos"), x)
def norm(x, peak=0.9): m = np.max(np.abs(x)) or 1; return x / m * peak
def env_exp(d, tau): return np.exp(-t(d) / tau)
def fade(x, a=0.02, r=0.05):
    n = len(x); ai, ri = int(a * SR), int(r * SR)
    if ai: x[:ai] *= np.linspace(0, 1, ai)
    if ri: x[-ri:] *= np.linspace(1, 0, ri)
    return x
def reverb(x, rt=1.5, wet=0.35, damp=4000):
    ir = lp(white(rt) * np.exp(-t(rt) * 6.9 / rt), damp)
    y = signal.fftconvolve(x, ir)[: len(x)]
    return (1 - wet) * x + wet * norm(y, np.max(np.abs(x)) or 1)
def place(buf, x, at, gain=1.0):
    i = int(at * SR); j = min(len(buf), i + len(x)); buf[i:j] += x[: j - i] * gain
def stereo(l, r=None, width=0.6):
    if r is None: r = np.roll(l, int(0.011 * SR))
    m = (l + r) / 2; s = (l - r) / 2 * width
    return np.stack([m + s, m - s], 1)
def save(name, x, peak=0.85):
    if x.ndim == 1: x = stereo(x, x, 0)
    x = x / (np.max(np.abs(x)) or 1) * peak
    sf.write(OUT / f"{name}.wav", x.astype(np.float32), SR, subtype="PCM_16")
    print(name, round(len(x) / SR, 1), "s", flush=True)

# ---------- camadas contínuas ----------
def rain(d, bright=8000, drops=1400, dark=False):
    base = bp(pink(d), 300, bright, 2) * 0.6 + lp(brown(d), 200) * 0.05
    dr = np.zeros(int(d * SR))
    for at in rng.uniform(0, d - 0.01, int(drops * d / 10)):
        g = hp(white(0.006) * env_exp(0.006, 0.0012), 2500)
        place(dr, g, at, rng.uniform(0.05, 0.4))
    x = base + dr
    return lp(x, 2600) if dark else x
def wind(d, lo=180, hi=900, howl=True):
    n = int(d * SR); x = np.zeros(n); src = pink(d)
    blk = int(0.05 * SR); ph = rng.uniform(0, 6)
    cen = np.interp(np.arange(0, n, blk), [0, n], [0, 1])
    for k, i in enumerate(range(0, n, blk)):
        c = lo + (hi - lo) * (0.5 + 0.5 * np.sin(k * 0.021 + ph) * np.sin(k * 0.0073))
        seg = src[max(0, i - blk): i + blk]
        y = bp(seg, max(40, c * 0.7), c * 1.4, 2)
        x[i: i + blk] = y[-min(blk, n - i):] if len(y) >= blk else np.pad(y, (0, blk - len(y)))[:min(blk, n - i)]
    amp = 0.55 + 0.45 * np.sin(np.arange(n) / SR * 0.35 + 1) * np.sin(np.arange(n) / SR * 0.13)
    return lp(x * amp, 2500)

save("rain_ext", stereo(rain(40), rain(40)) + 0)
save("rain_int", stereo(rain(40, dark=True), rain(40, dark=True)), 0.7)
rg = rain(40, dark=True)
for at in rng.uniform(0, 39.9, 140):
    f0 = rng.uniform(1800, 3600); place(rg, np.sin(2 * np.pi * f0 * t(0.04)) * env_exp(0.04, 0.006), at, rng.uniform(0.1, 0.35))
save("rain_glass", stereo(rg, rg), 0.75)
save("rain_open", stereo(rain(30, bright=6000), rain(30, bright=6000)), 0.85)
save("wind", stereo(wind(40), wind(40)), 0.8)
save("wind_int", stereo(lp(wind(40, 120, 500), 900), lp(wind(40, 120, 500), 900)), 0.6)
save("wind_open", stereo(wind(30, 250, 1400), wind(30, 250, 1400)), 0.85)
g = wind(4, 300, 1500); save("wind_gust", fade(g * np.sin(np.pi * t(4) / 4) ** 2, 0.1, 0.5))
save("room_tone", stereo(lp(pink(30), 400) * 0.3, lp(pink(30), 400) * 0.3), 0.25)

# ---------- trovões / impactos / drones ----------
def thunder(d, near):
    x = lp(brown(d), 120 if not near else 300) * (env_exp(d, d / 3.5) * (1 - env_exp(d, 0.15 if near else 0.6)))
    if near:
        cr = hp(white(0.6), 1200) * env_exp(0.6, 0.12); x[: len(cr)] += cr * 0.4 * np.max(np.abs(x)) / (np.max(np.abs(cr)) or 1)
        for k in range(4): place(x, lp(white(0.4), 400) * env_exp(0.4, 0.1), 0.5 + k * rng.uniform(0.6, 1.2), 0.3 * np.max(np.abs(x)))
    return reverb(x, 3.0, 0.4, 1500)
save("thunder_far", thunder(8, False)); save("thunder_near", thunder(8, True))
b = np.sin(2 * np.pi * (45 * t(4) - 6 * t(4) ** 2)) * env_exp(4, 1.0) + lp(white(4), 150) * env_exp(4, 0.4) * 0.5
save("boom", reverb(b, 2.5, 0.3, 800))
save("hit", reverb(np.sin(2 * np.pi * 55 * t(1.5)) * env_exp(1.5, 0.25) + hp(white(1.5), 2000) * env_exp(1.5, 0.05) * 0.4, 1.2, 0.3))
dd = 20; dr_ = np.sin(2 * np.pi * 41.2 * t(dd)) + 0.5 * np.sin(2 * np.pi * 82.9 * t(dd)) + 0.25 * np.sin(2 * np.pi * 123.1 * t(dd) + np.sin(t(dd) * 0.7))
save("low_drone", fade(dr_ * (0.7 + 0.3 * np.sin(t(dd) * 0.4)), 2.5, 3.0), 0.7)

def cello(d, f0=65.41):
    tt = t(d); vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * tt) * np.clip(tt / 2, 0, 1)
    ph = 2 * np.pi * f0 * np.cumsum(vib) / SR
    x = sum((1 / k) * np.sin(k * ph) * (0.9 ** k) for k in range(1, 18))
    x += bp(white(d), 200, 2000, 2) * 0.03
    x = lp(x, 1400); envl = np.clip(tt / 2.5, 0, 1) * np.clip((d - tt) / 3, 0, 1)
    return reverb(x * envl, 3.5, 0.45, 2500)
save("cello", stereo(cello(12), cello(12, 65.6)), 0.7)

# ---------- relógio ----------
def clock(d, loud=False):
    x = np.zeros(int(d * SR))
    for k in range(int(d)):
        f = 2300 if k % 2 == 0 else 1700
        c = bp(white(0.03), f * 0.8, f * 1.2, 2) * env_exp(0.03, 0.004) + np.sin(2 * np.pi * f * t(0.03)) * env_exp(0.03, 0.003) * 0.5
        place(x, c, k + 0.05, 1.0)
    return reverb(x, 0.8 if loud else 1.2, 0.2 if loud else 0.35)
save("clock_tick", clock(30), 0.5); save("clock_tick_loud", clock(30, True), 0.8)
def bell(d=4.5):
    tt = t(d); f0 = 196
    return sum(a * np.sin(2 * np.pi * f0 * r * tt) * np.exp(-tt / (dec)) for r, a, dec in [(1, 1, 2.5), (2.0, 0.5, 1.8), (2.76, 0.4, 1.2), (5.4, 0.2, 0.6), (8.9, 0.1, 0.3)])
cb = np.zeros(int(8 * SR))
for k in range(3): place(cb, bell(), k * 2.2)
save("clock_bell3", reverb(cb, 2.5, 0.35))

# ---------- batidas ----------
def knock_glass():
    th = lp(white(0.08), 600) * env_exp(0.08, 0.012)
    ring = sum(np.sin(2 * np.pi * f * t(0.25)) * env_exp(0.25, 0.04) for f in (1830, 3120, 4410)) * 0.15
    x = np.zeros(int(0.3 * SR)); place(x, th, 0); place(x, ring, 0.002); return x
kg = np.zeros(int(2.2 * SR))
for k in range(3): place(kg, knock_glass(), 0.05 + k * 0.62)
save("knock_glass3", reverb(kg, 1.0, 0.3))
pg = np.zeros(int(1.2 * SR))
for k, at in enumerate([0.05, 0.22, 0.6]): place(pg, hp(knock_glass(), 900), at)
save("peck_glass", reverb(pg, 0.8, 0.25))
def knock_wood():
    return sum(np.sin(2 * np.pi * f * t(0.25)) * env_exp(0.25, d) for f, d in [(110, 0.06), (190, 0.04), (320, 0.025)]) + lp(white(0.25), 500) * env_exp(0.25, 0.01)
kw = np.zeros(int(3 * SR))
for k in range(3): place(kw, knock_wood(), 0.05 + k * 0.75)
save("knock_wood3", reverb(kw, 1.6, 0.4, 2000))
hb = np.zeros(int(10 * SR))
for k in range(10):
    for o, a in [(0, 1), (0.28, 0.7)]: place(hb, np.sin(2 * np.pi * 50 * t(0.18)) * env_exp(0.18, 0.04) * a, k + o)
save("heartbeat", lp(hb, 200))

# ---------- madeira, papel, objetos ----------
def creak(d, f_a, f_b, rough=0.3):
    n = int(d * SR); x = np.zeros(n); pos = 0.0
    while pos < d - 0.01:
        f = f_a + (f_b - f_a) * pos / d
        place(x, np.array([1.0]), pos, rng.uniform(0.6, 1.0)); pos += 1 / f * rng.uniform(1 - rough, 1 + rough)
    y = sum(bp(x, f * 0.9, f * 1.1, 2) for f in (420, 900, 1600)) + bp(x, 100, 400, 2) * 0.5
    return y * np.sin(np.pi * t(d) / d) ** 0.5
save("wood_creak", reverb(creak(2.6, 70, 130), 1.4, 0.35))
save("chair_scrape", reverb(creak(1.1, 140, 260, 0.5) + bp(white(1.1), 300, 1500) * 0.15 * np.sin(np.pi * t(1.1) / 1.1), 0.9, 0.25))
def steps(n, gap, rv, heavy=0.0):
    x = np.zeros(int((n * gap + 1.5) * SR))
    for k in range(n):
        s = lp(white(0.12), 700) * env_exp(0.12, 0.025) + np.sin(2 * np.pi * 90 * t(0.12)) * env_exp(0.12, 0.03) * 0.5
        place(x, s, 0.1 + k * gap * rng.uniform(0.95, 1.05), rng.uniform(0.7, 1.0))
        if rng.random() < 0.3: place(x, creak(0.4, 160, 200) * 0.2, 0.15 + k * gap)
    return reverb(x, rv, 0.35)
save("steps_wood", steps(4, 0.55, 1.0)); save("steps_corridor", steps(18, 0.6, 2.2)); save("steps_run", steps(10, 0.3, 1.2))
def rustle(d, dens=60):
    x = np.zeros(int(d * SR))
    for at in rng.uniform(0, d - 0.05, int(dens * d)): place(x, hp(white(0.03), 2500) * env_exp(0.03, 0.006), at, rng.uniform(0.2, 1))
    return x * np.sin(np.pi * t(d) / d)
save("paper", reverb(rustle(2.2), 0.7, 0.2)); save("paper_fall", reverb(rustle(1.4, 30) + lp(white(1.4), 1500) * 0.05 * np.sin(np.pi * t(1.4) / 1.4), 0.9, 0.3))
sc = np.zeros(int(8 * SR))
for at in np.arange(0.2, 7.5, 0.18): place(sc, hp(white(0.12), 3000) * np.sin(np.pi * t(0.12) / 0.12) * rng.uniform(0.3, 1), at + rng.uniform(-0.04, 0.04))
save("pen", sc, 0.4)
dr = np.zeros(int(3.2 * SR))
for at in [0.1, 0.55, 1.0, 1.35]: place(dr, knock_wood() * 0.6, at); place(dr, creak(0.25, 160, 220), at + 0.02, 0.6)
place(dr, creak(0.9, 120, 180, 0.15) + lp(white(0.9), 900) * 0.1, 1.8)
save("drawer_force", reverb(dr, 1.0, 0.3))
cp = lp(white(0.6), 1200) * np.sin(np.pi * t(0.6) / 0.6) ** 2
save("candle_out", reverb(cp, 0.6, 0.3), 0.6)
br = np.zeros(int(6 * SR))
for k in range(4):
    seg = bp(white(1.2), 300, 1800, 2) * np.sin(np.pi * t(1.2) / 1.2) * (1 + 0.4 * np.sin(2 * np.pi * 9 * t(1.2)))
    place(br, seg, 0.2 + k * 1.4, 0.8 if k % 2 == 0 else 0.5)
save("breath", br, 0.5)
cf = np.zeros(int(2 * SR)); place(cf, sum(np.sin(2 * np.pi * f * t(0.6)) * env_exp(0.6, 0.12) for f in (1240, 2970, 4630)) * 0.4, 0); place(cf, knock_wood(), 0.35)
save("candle_fall", reverb(cf, 1.0, 0.3))
gb = np.zeros(int(3 * SR)); place(gb, hp(white(0.3), 1500) * env_exp(0.3, 0.06), 0)
for at in rng.uniform(0.02, 1.6, 90): place(gb, np.sin(2 * np.pi * rng.uniform(2500, 7000) * t(0.15)) * env_exp(0.15, 0.02), at, rng.uniform(0.05, 0.3))
save("glass_break", reverb(gb, 1.2, 0.3))
wh = lp(white(1.0), 2500) * np.sin(np.pi * t(1.0) / 1.0) ** 3
save("whoosh", reverb(wh, 0.8, 0.3), 0.6)
wi = lp(white(2.0), 900) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 5.5 * t(2.0)))) * env_exp(2.0, 0.9)
save("wings", reverb(wi, 0.8, 0.25))

# ---------- corvo, choro, piano, pássaros ----------
def caw(d=0.38, f0=520):
    tt = t(d); fm = f0 * (1 + 0.08 * np.sin(2 * np.pi * 31 * tt)) * (1 - 0.15 * tt / d)
    src = signal.sawtooth(2 * np.pi * np.cumsum(fm) / SR) + hp(white(d), 1500) * 0.4
    y = bp(src, 900, 1500, 2) + bp(src, 2200, 3000, 2) * 0.6
    return np.tanh(3 * y) * np.sin(np.pi * tt / d) ** 0.6
cw = np.zeros(int(3 * SR)); place(cw, caw(), 0.1); place(cw, caw(0.42, 500), 0.75)
save("raven_caw", reverb(cw, 2.0, 0.4, 3000))
def sob(d, f0):
    tt = t(d); f = f0 * (1.15 - 0.3 * tt / d) * (1 + 0.03 * np.sin(2 * np.pi * 6 * tt))
    src = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * 0.5 + bp(white(d), 500, 3000, 2) * 0.25
    y = bp(src, 700, 1100, 2) + bp(src, 1100, 1400, 2) * 0.6 + bp(src, 2400, 2900, 2) * 0.3
    return y * np.sin(np.pi * tt / d) ** 1.5
cr = np.zeros(int(8 * SR))
for at, d, f0 in [(0.2, 0.9, 330), (1.3, 0.5, 300), (1.9, 1.2, 290), (3.6, 0.6, 320), (4.4, 1.4, 280)]: place(cr, sob(d, f0), at)
save("crying", reverb(lp(cr, 1800), 2.8, 0.6, 1500), 0.6)
def piano_note(f, d=3.0):
    tt = t(d); B = 0.0004
    return sum((1 / k) * np.sin(2 * np.pi * f * k * np.sqrt(1 + B * k * k) * tt) * np.exp(-tt * (0.8 + 0.6 * k)) for k in range(1, 9))
pn = np.zeros(int(12 * SR))
for at, n in [(0.2, 57), (0.9, 60), (1.6, 64), (2.6, 62), (3.4, 60), (4.4, 59), (5.5, 57), (6.3, 52), (7.4, 57), (8.6, 56)]:
    place(pn, piano_note(440 * 2 ** ((n - 69) / 12)), at, 0.8)
save("piano", reverb(lp(pn, 2200), 3.0, 0.5, 2000), 0.6)
bd = lp(pink(20), 300) * 0.05
for at in rng.uniform(0.5, 19, 18):
    d = rng.uniform(0.08, 0.2); f = rng.uniform(3200, 5200)
    place(bd, np.sin(2 * np.pi * np.cumsum(f * (1 + 0.3 * np.sin(2 * np.pi * 25 * t(d)))) / SR) * np.sin(np.pi * t(d) / d), at, rng.uniform(0.05, 0.15))
save("birds_far", reverb(bd, 1.8, 0.5), 0.4)
