"""Teste rápido: renderiza quadros-chave de cada plano para conferir as caixas e expressões."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv2
import anim
from face import Face
from src.utils.crop import paste_back
os.makedirs("renders/test_shots", exist_ok=True)
keys = {"s02": [0.5, 9.0, 12.5, 21.5, 26.5], "s03": [3, 8], "s04": [1.0, 7.0, 12.0, 16.0], "s05": [4.0, 11.0, 20.0], "s05_floor": [0.5, 6.0], "s06": [1, 11]}
for nm in (sys.argv[1:] or keys):
    S = anim.SHOTS[nm]; base = cv2.cvtColor(cv2.imread(f"assets/plates/{S['plate']}.png"), cv2.COLOR_BGR2RGB)
    F = [Face(base, f["box"]) for f in S["faces"]]
    for u in keys[nm]:
        img = base.copy()
        for fc, f in zip(S["faces"], F):
            p = fc["fn"](u); img = paste_back(f.frame(crop_only=True, **p), f.M_c2o, img, f.mask_ori)
        cv2.imwrite(f"renders/test_shots/{nm}_{u}.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print("ok", nm, flush=True)
