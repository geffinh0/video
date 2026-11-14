"""Monta as imagens-base compostas (espelhos) a partir das imagens geradas."""
import os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = f"{ROOT}/assets/plates"
L = lambda n: Image.open(f"{P}/{n}.png").convert("RGB")

def soft_mask(size, box, feather):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rectangle(box, fill=255); return m.filter(ImageFilter.GaussianBlur(feather))

# S02: Clara de perfil (real, à esquerda) + o espelho à direita com o reflexo (a mesma pessoa, espelhada)
a = L("s02_a"); W, H = a.size; mx0 = 985; gw = W - mx0
fl = a.transpose(Image.FLIP_LEFT_RIGHT)
back = fl.crop((0, 0, gw, H)).filter(ImageFilter.GaussianBlur(3))                      # parede refletida
person = fl.crop((330, 0, 1150, 768)); sc = 0.55; GH = 560
person = person.resize((int(person.width * sc), int(person.height * sc)), Image.LANCZOS)
glass = back.copy()
pm = soft_mask(person.size, (40, 50, person.width - 40, person.height + 80), 32)
glass.paste(person, (gw - person.width + 70, GH - person.height), pm)
glass = glass.crop((0, 0, gw, GH))
glass = ImageEnhance.Brightness(glass).enhance(0.7); glass = ImageEnhance.Color(glass).enhance(0.85).filter(ImageFilter.GaussianBlur(0.8))
comp = a.copy(); comp.paste(glass, (mx0, 0))
sp = Image.new("L", (gw, GH), 0); d = ImageDraw.Draw(sp)
for k in range(4): d.line([(20 + k * 90, 0), (190 + k * 90, GH)], fill=14, width=40)
comp.paste(Image.new("RGB", sp.size, (230, 235, 230)), (mx0, 0), sp.filter(ImageFilter.GaussianBlur(30)))
comp.paste(Image.new("RGB", (16, H), (34, 62, 54)), (mx0 - 8, 0)); comp.paste(Image.new("RGB", (gw, 12), (34, 62, 54)), (mx0, GH))
below = ImageEnhance.Brightness(a.crop((mx0, GH + 12, W, H))).enhance(0.55); comp.paste(below, (mx0, GH + 12))
comp.save(f"{P}/s02_comp.png"); print("s02_comp")

# S04: rosto-mestre em close extremo (o reflexo encostado ao vidro)
c = Image.open(f"{ROOT}/assets/img/test_clara.png").convert("RGB").resize((1344, 1344), Image.LANCZOS)
c.crop((0, 230, 1344, 998)).save(f"{P}/s04_comp.png"); print("s04_comp")

# S06: o mesmo quadro da observação, mas sem a pessoa real — só o reflexo fica
m2, e = L("cctv_mirror2"), L("cctv_empty")
s06 = Image.composite(e, m2, soft_mask(m2.size, (812, 130, 1000, 760), 10)); s06.save(f"{P}/s06_comp.png"); print("s06_comp")
