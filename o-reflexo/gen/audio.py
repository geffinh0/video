"""Paisagem sonora sintetizada (numpy/scipy) + falas (Kokoro-82M, Apache-2.0). Saída: assets/audio/*.wav (48 kHz).
Nada de música: só ambiente, dispositivo, corpo e o sobrenatural pontual."""
import os, subprocess
import numpy as np
from scipy import signal
from scipy.io import wavfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/assets/audio"; os.makedirs(OUT, exist_ok=True)
SR = 48000; rng = np.random.default_rng(47)

def save(name, x, gain=1.0):
    x = np.asarray(x, np.float64); x = x / (np.max(np.abs(x)) + 1e-9) * 0.89 * gain
    if x.ndim == 1: x = np.stack([x, x], 1)
    wavfile.write(f"{OUT}/{name}.wav", SR, (x * 32767).astype(np.int16)); print("ok", name)

def t(sec): return np.arange(int(sec * SR)) / SR
def bp(x, lo, hi, o=4): return signal.sosfilt(signal.butter(o, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f, o=4): return signal.sosfilt(signal.butter(o, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f, o=4): return signal.sosfilt(signal.butter(o, f, "highpass", fs=SR, output="sos"), x)
def pink(n):
    w = rng.standard_normal(n); f = np.fft.rfft(w); k = np.arange(len(f)); k[0] = 1
    return np.fft.irfft(f / np.sqrt(k), n)
def env(n, a, r):
    e = np.ones(n); A = int(a * SR); R = int(r * SR)
    if A: e[:A] = np.linspace(0, 1, A)
    if R: e[-R:] *= np.linspace(1, 0, R)
    return e
def loopable(x, fade=1.0):
    F = int(fade * SR); y = x[:-F].copy(); y[:F] = y[:F] * np.linspace(0, 1, F) + x[-F:] * np.linspace(1, 0, F); return y

def room_tone():
    n = len(t(41)); x = lp(pink(n), 900) * 0.6 + bp(rng.standard_normal(n), 2000, 5000) * 0.02
    save("room_tone", loopable(x), 0.5)

def fan():
    T = t(41); n = len(T); x = bp(pink(n), 120, 2400) * (1 + 0.08 * np.sin(2 * np.pi * 7.3 * T))
    x += 0.12 * np.sin(2 * np.pi * 97 * T) * (1 + 0.3 * np.sin(2 * np.pi * 0.4 * T))
    save("fan", loopable(x), 0.6)

def hum():
    T = t(41); x = sum(a * np.sin(2 * np.pi * f * T) for f, a in ((60, 1), (120, 0.6), (180, 0.35), (240, 0.2), (360, 0.12)))
    buzz = bp(rng.standard_normal(len(T)), 2500, 7000) * (np.sin(2 * np.pi * 120 * T) > 0.92) * 0.6
    flick = np.ones(len(T))
    for s in rng.uniform(1, 39, 6):     # tremidas da lâmpada fluorescente
        i = int(s * SR); L = int(rng.uniform(0.05, 0.25) * SR); flick[i:i + L] *= rng.uniform(0.2, 0.6)
    save("hum", loopable((x * 0.5 + buzz) * flick), 0.5)

def vhs_hiss():
    T = t(31); n = len(T); x = hp(rng.standard_normal(n), 3000) * 0.5 + bp(pink(n), 300, 3000) * 0.3
    x += 0.04 * np.sin(2 * np.pi * 15734 * T)       # whine da linha horizontal
    x *= 1 + 0.15 * np.sin(2 * np.pi * 0.7 * T)
    save("vhs_hiss", loopable(x), 0.6)

def cctv_tone():
    T = t(31); x = hp(rng.standard_normal(len(T)), 6000) * 0.2 + 0.05 * np.sin(2 * np.pi * 9800 * T) + lp(pink(len(T)), 400) * 0.3
    save("cctv_tone", loopable(x), 0.4)

def phone_room():
    T = t(41); x = lp(pink(len(T)), 2500) * 0.5 + hp(rng.standard_normal(len(T)), 5000) * 0.05   # ruído de microfone de celular
    save("phone_room", loopable(x), 0.45)

def clicks():
    n = len(t(1.2)); x = np.zeros(n)
    for k in range(5): i = int(rng.uniform(0, 1.1) * SR); L = 300; x[i:i + L] += rng.standard_normal(L) * np.exp(-np.arange(L) / 40)
    save("clicks", hp(x, 800))

def breath(name, dur, inhale=True, shaky=False):
    T = t(dur); n = len(T); x = bp(rng.standard_normal(n), 400 if inhale else 250, 3500 if inhale else 2200)
    e = np.sin(np.pi * np.clip(T / dur, 0, 1)) ** (1.5 if inhale else 1)
    if shaky: e *= 1 + 0.35 * np.sin(2 * np.pi * 9 * T + rng.uniform(0, 6))
    save(name, x * e, 0.6)

def breathing_loop():
    seq = []
    for k in range(9):
        d1, d2 = rng.uniform(0.7, 1.1), rng.uniform(0.9, 1.4)
        for d, lo, hi in ((d1, 400, 3500), (d2, 250, 2200)):
            T = t(d); x = bp(rng.standard_normal(len(T)), lo, hi) * np.sin(np.pi * T / d) ** 1.3 * (1 + 0.3 * np.sin(2 * np.pi * 8 * T))
            seq.append(x); seq.append(np.zeros(int(rng.uniform(0.1, 0.35) * SR)))
    save("breathing", np.concatenate(seq), 0.7)

def phone_drop():
    n = len(t(2.5)); x = np.zeros(n)
    for k, (s, a) in enumerate(((0.0, 1.0), (0.21, 0.45), (0.33, 0.25), (0.42, 0.12))):
        i = int(s * SR); L = int(0.25 * SR); T = np.arange(L) / SR
        hit = (bp(rng.standard_normal(L), 300, 6000) * 0.7 + np.sin(2 * np.pi * (180 + 60 * k) * T) * 0.6 + np.sin(2 * np.pi * 2300 * T) * 0.25) * np.exp(-T * 28) * a
        x[i:i + L] += hit
    x[int(0.5 * SR):int(1.6 * SR)] += bp(rng.standard_normal(int(1.1 * SR)), 1500, 5000) * np.exp(-np.arange(int(1.1 * SR)) / SR * 6) * 0.08
    save("phone_drop", x)

def low_drone(name="low_drone", dur=20):
    T = t(dur); x = np.sin(2 * np.pi * 34 * T + 0.5 * np.sin(2 * np.pi * 0.11 * T)) + 0.5 * np.sin(2 * np.pi * 51.3 * T) + 0.3 * lp(pink(len(T)), 120)
    save(name, x * env(len(T), dur * 0.4, dur * 0.3), 0.7)

def interference(name, dur, seed):
    r = np.random.default_rng(seed); T = t(dur); n = len(T); x = np.zeros(n); i = 0
    while i < n:
        L = int(r.uniform(0.02, 0.18) * SR); kind = r.integers(0, 3)
        if kind == 0: seg = np.sign(np.sin(2 * np.pi * r.uniform(200, 2000) * np.arange(L) / SR))
        elif kind == 1: seg = r.standard_normal(L)
        else: seg = np.round(r.standard_normal(L) * 3) / 3
        x[i:i + L] = seg[:n - i] * r.uniform(0.3, 1); i += L + int(r.uniform(0, 0.08) * SR)
    save(name, hp(x, 150) * env(n, 0.005, 0.05), 0.75)

def glass_squeak():
    T = t(3.2); f = 900 + 500 * np.sin(2 * np.pi * 0.6 * T) + 200 * rng.standard_normal(len(T)).cumsum() / SR
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * (np.sin(2 * np.pi * 11 * T) > 0.4))
    x = bp(x, 600, 4000) * env(len(T), 0.2, 0.3) + bp(rng.standard_normal(len(T)), 2000, 6000) * 0.15
    save("glass_squeak", x, 0.35)

def sub_hit():
    T = t(3); x = np.sin(2 * np.pi * (48 - 14 * T) * T) * np.exp(-T * 1.4) + lp(rng.standard_normal(len(T)), 200) * np.exp(-T * 5) * 0.5
    save("sub_hit", x, 0.8)

def tape_in():
    T = t(2.5); f = 60 + 400 * np.clip(T / 1.2, 0, 1); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + hp(rng.standard_normal(len(T)), 1500) * 0.6
    save("tape_in", x * env(len(T), 0.05, 0.4), 0.6)

def voices():
    from kokoro_onnx import Kokoro
    K = f"{ROOT}/../o-ultimo-pouso/assets/voices/models"
    k = Kokoro(f"{K}/kokoro-v1.0.onnx", f"{K}/voices-pt.npz")
    lines = {
        "v_denovo": ("Tá... de novo.", 0.85, "phone"),
        "v_camera": ("Isso é a câmera. Só pode ser a câmera.", 0.9, "phone"),
        "v_nao": ("Não... não.", 0.75, "phone"),
        "v_ouvindo": ("Eu sei que você está me ouvindo.", 0.72, "whisper"),
    }
    for name, (txt, sp, fx) in lines.items():
        a, sr = k.create(txt, voice="pf_dora", speed=sp, lang="pt-br")
        raw = f"{OUT}/{name}_raw.wav"; wavfile.write(raw, sr, (np.asarray(a) * 32767).astype(np.int16))
        chain = {"phone": "highpass=f=220,lowpass=f=5200,acompressor=threshold=-20dB:ratio=4,volume=0.9",
                 "whisper": "highpass=f=380,lowpass=f=6500,afftdn=nf=-30,acompressor=threshold=-25dB:ratio=6,volume=0.55,aecho=0.6:0.3:18:0.15"}[fx]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", chain + ",aresample=48000", "-ac", "2", f"{OUT}/{name}.wav"], check=True)
        os.remove(raw); print("ok", name)

if __name__ == "__main__":
    room_tone(); fan(); hum(); vhs_hiss(); cctv_tone(); phone_room(); clicks()
    breath("breath_in", 1.1, True); breath("breath_out_shaky", 1.6, False, True); breath("gasp", 0.45, True); breathing_loop()
    phone_drop(); low_drone(); interference("glitch_a", 1.2, 1); interference("glitch_b", 2.5, 2); interference("glitch_c", 0.6, 3)
    glass_squeak(); sub_hit(); tape_in(); voices()
