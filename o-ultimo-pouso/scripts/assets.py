#!/usr/bin/env python3
"""Baixa os assets livres (CC0) usados no filme.
- Poly Haven (polyhaven.com, CC0): modelos glTF, texturas PBR e HDRIs -> assets/polyhaven/
- MakeHuman / MPFB2 (CC0 nos dados): malha base, rig e pesos    -> vendor/mpfb2/ (só os dados são lidos)
Uso: python3 scripts/assets.py   (idempotente: pula o que já existe)"""
import json, os, subprocess, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PH = f"{ROOT}/assets/polyhaven"
MODELS = [
    "vintage_grandfather_clock_01", "mantel_clock_01", "ArmChair_01", "GothicCabinet_01", "GothicCommode_01",
    "gothic_statue", "marble_bust_01", "brass_candleholders", "wooden_candlestick", "vintage_oil_lamp",
    "Chandelier_01", "Chandelier_03", "fancy_picture_frame_01", "fancy_picture_frame_02", "hanging_picture_frame_01",
    "hanging_picture_frame_02", "hanging_picture_frame_03", "standing_picture_frame_01", "ornate_mirror_01",
    "book_encyclopedia_set_01", "wooden_bookshelf_worn", "vintage_cabinet_01",
    "ClassicConsole_01", "large_castle_door", "large_iron_gate", "dead_tree_trunk", "dead_tree_trunk_02",
    "tree_stump_01", "boulder_01", "rock_moss_set_01", "antique_ceramic_vase_01", "brass_vase_01", "WoodenChair_01",
    "dining_chair_02", "side_table_tall_01", "gothic_coffee_table", "round_spectacles",
]
TEXTURES = ["wood_floor_deck", "dark_wood", "wood_table_001", "plastered_wall", "forest_ground_04", "bark_brown_02",
            "castle_brick_02_red", "fabric_pattern_07", "velour_velvet", "worn_planks", "slate_floor_02"]
HDRIS = ["moonless_golf", "satara_night_no_lamps", "kloppenheim_02"]


def get(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0: return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "asset-fetch"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dst + ".part", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)
    os.replace(dst + ".part", dst)


def files(asset):
    req = urllib.request.Request(f"https://api.polyhaven.com/files/{asset}", headers={"User-Agent": "asset-fetch"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def model(a, res="1k"):
    d = f"{PH}/models/{a}"
    if os.path.exists(f"{d}/.done"): return
    g = files(a)["gltf"]; g = g.get(res) or g[sorted(g)[0]]; g = g["gltf"]
    get(g["url"], f"{d}/{a}.gltf")
    for rel, inc in g.get("include", {}).items(): get(inc["url"], f"{d}/{rel}")
    open(f"{d}/.done", "w").write("ok")


def texture(a, res="1k"):
    d = f"{PH}/textures/{a}"
    if os.path.exists(f"{d}/.done"): return
    f = files(a)
    for key, name in (("Diffuse", "diff"), ("nor_gl", "nor"), ("Rough", "rough"), ("Displacement", "disp")):
        if key in f and res in f[key]:
            e = f[key][res]; e = e.get("jpg") or e.get("png")
            get(e["url"], f"{d}/{name}.{e['url'].rsplit('.', 1)[-1]}")
    open(f"{d}/.done", "w").write("ok")


def hdri(a, res="1k"):
    get(files(a)["hdri"][res]["hdr"]["url"], f"{PH}/hdris/{a}.hdr")


def main():
    for kind, lst, fn in (("modelo", MODELS, model), ("textura", TEXTURES, texture), ("hdri", HDRIS, hdri)):
        for a in lst:
            try: fn(a); print("ok", kind, a, flush=True)
            except Exception as e: print("FALHOU", kind, a, repr(e)[:120], flush=True)
    v = f"{ROOT}/vendor/mpfb2"
    if not os.path.exists(f"{v}/src/mpfb/data/3dobjs/base.obj"):
        os.makedirs(f"{ROOT}/vendor", exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--depth", "1", "https://github.com/makehumancommunity/mpfb2.git", v], check=False)
    print("mpfb2 dados:", os.path.exists(f"{v}/src/mpfb/data/3dobjs/base.obj"))


if __name__ == "__main__":
    main()
