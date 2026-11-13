"""Texturas 2D originais: papel envelhecido, cartas manuscritas, mostrador do relógio, manuscrito."""
import math, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "assets/textures"; F = T / "fonts"
rng = np.random.default_rng(3)
HAND = str(F / "HomemadeApple.ttf"); FELL = str(F / "IMFellEnglish.ttf")

def noise(w, h, scale):
    small = rng.random((max(2, h // scale), max(2, w // scale)))
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)) / 255.0

def aged_paper(w, h, base=(214, 196, 150), stains=True):
    a = np.zeros((h, w, 3))
    n = 0.55 * noise(w, h, 64) + 0.3 * noise(w, h, 12) + 0.15 * rng.random((h, w))
    for i, c in enumerate(base): a[..., i] = c * (0.82 + 0.25 * n)
    yy, xx = np.mgrid[0:h, 0:w]; d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a *= (1 - 0.35 * np.clip(d - 0.55, 0, 1))[..., None]          # bordas escurecidas
    if stains:
        for _ in range(7):
            cx, cy, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(40, 160) * w / 1600
            m = np.clip(1 - np.abs(np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - r) / (r * 0.12), 0, 1) * 0.12
            a *= (1 - m)[..., None] * np.array([1, 0.97, 0.9])
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def handwrite(img, lines, x, y, size, ink=(35, 25, 18), lh=1.55, shake=1.5, seed=0):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(HAND, size); r = np.random.default_rng(seed)
    for i, ln in enumerate(lines):
        cx = x + r.uniform(-6, 6); cy = y + i * size * lh
        for word in ln.split(" "):
            dy = r.uniform(-shake, shake) * 2
            d.text((cx, cy + dy), word, font=f, fill=(*ink, 255))
            cx += d.textlength(word + " ", font=f)
    return img

def letter_closed():
    im = aged_paper(1600, 1000)
    handwrite(im, ["Para Arthur.", "Quando ele voltar."], 330, 300, 78, seed=1)
    d = ImageDraw.Draw(im); d.line([(80, 500), (1520, 500)], fill=(150, 130, 95), width=3)  # dobra
    im.filter(ImageFilter.GaussianBlur(0.6)).save(T / "letter_closed.png")

BODY = ["Meu querido Arthur...", "", "Se estiver lendo estas palavras, significa", "que ele encontrou novamente o caminho até você.", "",
        "Não olhe para trás quando ouvir três batidas.", "Não abra a porta, mesmo que escute minha voz.", "",
        "E, acima de tudo... não acredite naquilo", "que você se lembra daquela noite.", "", "              Sempre sua,", "                    Eleanor"]

def letter_open(final=False):
    im = aged_paper(1600, 2200)
    handwrite(im, BODY, 140, 170, 50, seed=2)
    if final:
        handwrite(im, ["Agora é a sua vez de esperar."], 170, 1900, 62, ink=(70, 12, 10), shake=4, seed=9)
    d = ImageDraw.Draw(im); d.line([(60, 1100), (1540, 1100)], fill=(160, 140, 105), width=3)
    im.filter(ImageFilter.GaussianBlur(0.6)).save(T / ("letter_final.png" if final else "letter_open.png"))

def manuscript():
    im = aged_paper(1600, 2200, base=(222, 210, 175), stains=False)
    words = "a noite e o silêncio e a casa que respira com os mortos lembrança vela janela promessa porta memória chuva".split()
    r = np.random.default_rng(5); lines = [" ".join(r.choice(words, r.integers(5, 9))) for _ in range(26)]
    handwrite(im, lines, 120, 140, 40, ink=(30, 30, 45), seed=4)
    d = ImageDraw.Draw(im)
    for _ in range(9):  # rasuras
        x, y = r.uniform(150, 1200), r.uniform(150, 1900); d.line([(x, y), (x + r.uniform(150, 400), y + r.uniform(-8, 8))], fill=(25, 25, 35), width=6)
    im.filter(ImageFilter.GaussianBlur(0.5)).save(T / "manuscript.png")

def clock_face(h=3, m=16, name="clock_face.png"):
    S = 1600; im = aged_paper(S, S, base=(226, 214, 180), stains=False); d = ImageDraw.Draw(im); c = S / 2
    f = ImageFont.truetype(FELL, 150)
    for ring, wdt in [(0.47, 10), (0.36, 4)]:
        d.ellipse([c - S * ring, c - S * ring, c + S * ring, c + S * ring], outline=(30, 25, 20), width=wdt)
    for k in range(60):
        a = math.radians(k * 6 - 90); r1 = S * (0.45 if k % 5 else 0.43); r2 = S * 0.465
        d.line([(c + r1 * math.cos(a), c + r1 * math.sin(a)), (c + r2 * math.cos(a), c + r2 * math.sin(a))], fill=(30, 25, 20), width=8 if k % 5 == 0 else 3)
    rom = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
    for k, t in enumerate(rom):
        a = math.radians(k * 30 - 90); r = S * 0.375; w = d.textlength(t, font=f)
        d.text((c + r * math.cos(a) - w / 2, c + r * math.sin(a) - 95), t, font=f, fill=(25, 20, 15))
    def hand(angle, length, width):
        a = math.radians(angle - 90); d.line([(c, c), (c + length * math.cos(a), c + length * math.sin(a))], fill=(15, 12, 10), width=width)
    hand((h % 12) * 30 + m * 0.5, S * 0.24, 26); hand(m * 6, S * 0.37, 14)
    d.ellipse([c - 30, c - 30, c + 30, c + 30], fill=(15, 12, 10))
    im.save(T / name)

def tile_wallpaper():
    pass

letter_closed(); letter_open(); letter_open(final=True); manuscript(); clock_face(3, 16); clock_face(3, 17, "clock_face_317.png")
print(sorted(p.name for p in T.glob("*.png")))
