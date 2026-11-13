"""Corredor: longo (y de 0 a 12), largura 2,2 m, retratos nas paredes, porta fechada no fim (y=12)."""
import bpy, math, random
from mathutils import Vector
from .core import *
from .core import _move

A = {}
def build(warm=False):
    c = coll("corridor"); random.seed(21)
    wp = mat_wallpaper("wallpaper_corr", (0.03, 0.025, 0.035), (0.06, 0.05, 0.065))
    wood = mat_wood("dark_wood"); floor = mat_planks("floor")
    runner = mat_noise("runner", (0.08, 0.012, 0.01), (0.18, 0.05, 0.02), 25, rough=0.95, bump=0.1)
    gold = mat("gilt", (0.35, 0.24, 0.08), 0.35, 1.0); brass = mat("brass", (0.55, 0.38, 0.15), 0.35, 1.0)
    W, Lg, Hh = 2.2, 12.0, 3.2
    box("c_floor", (W, Lg + 1, 0.05), (0, Lg / 2, -0.025), floor, coll=c)
    box("c_runner", (0.9, Lg, 0.01), (0, Lg / 2, 0.005), runner, coll=c)
    box("c_ceiling", (W, Lg + 1, 0.1), (0, Lg / 2, Hh + 0.05), mat("c_ceil", (0.02, 0.02, 0.02), 0.9), coll=c)
    for sx in (-1, 1):
        box(f"c_wall{sx}", (0.1, Lg + 1, Hh), (sx * (W / 2 + 0.05), Lg / 2, Hh / 2), wp, bevel=0, coll=c)
        box(f"c_wains{sx}", (0.12, Lg + 1, 1.0), (sx * (W / 2 + 0.04), Lg / 2, 0.5), wood, bevel=0, coll=c)
    box("c_back", (W, 0.1, Hh), (0, -0.6, Hh / 2), wp, bevel=0, coll=c)
    # parede do fim com a porta
    box("c_end_l", (0.6, 0.1, Hh), (-0.8, Lg + 0.05, Hh / 2), wp, bevel=0, coll=c)
    box("c_end_r", (0.6, 0.1, Hh), (0.8, Lg + 0.05, Hh / 2), wp, bevel=0, coll=c)
    box("c_end_t", (1.0, 0.1, Hh - 2.3), (0, Lg + 0.05, (Hh + 2.3) / 2), wp, bevel=0, coll=c)
    box("c_door", (1.0, 0.06, 2.3), (0, Lg + 0.02, 1.15), mat_wood("walnut"), coll=c)
    for zz in (0.55, 1.6): box("c_door_inset", (0.72, 0.02, 0.75), (0, Lg - 0.02, zz), wood, coll=c)
    sphere("c_door_knob", 0.035, (0.38, Lg - 0.04, 1.0), brass, coll=c)
    cyl("c_keyhole", 0.008, 0.01, (0.38, Lg - 0.015, 0.9), mat("void", (0, 0, 0), 1), rot=(math.radians(90), 0, 0), coll=c)
    A["door"] = Vector((0, Lg, 1.15))
    # luz por baixo da porta (alguém do outro lado?)
    box("c_door_gap", (0.9, 0.02, 0.012), (0, Lg + 0.06, 0.006), mat_emit("gap_light", kelvin(2200 if warm else 6000), 4 if warm else 1.5), coll=c)
    # retratos
    paint = mat_noise("painting_c", (0.02, 0.016, 0.012), (0.1, 0.08, 0.05), 2.5, rough=0.35, bump=0.05)
    A["portraits"] = []
    for i, y in enumerate([1.5, 3.5, 5.5, 7.5, 9.5]):
        for sx in (-1, 1):
            tilt = math.radians(9) if (sx == 1 and i == 3) else 0
            g = empty(f"portrait{i}{sx}", (sx * (W / 2 - 0.02), y, 1.95), (0, tilt * -sx, 0), coll=c)
            w, h = random.uniform(0.5, 0.7), random.uniform(0.65, 0.9)
            box("pf", (0.05, w + 0.12, h + 0.12), (0, 0, 0), gold, parent=g, coll=c)
            m = mat_image("eleanor_portrait", "/home/user/video/o-ultimo-pouso/assets/textures/eleanor_portrait.png", 0.4) if (sx == 1 and i == 3) else paint
            pl = box("pc", (0.055, w, h), (0, 0, 0), m, parent=g, coll=c)
            if sx == 1 and i == 3: A["eleanor_portrait"] = g
            A["portraits"].append(g)
    # arandelas (velas fracas)
    for i, y in enumerate([2.5, 6.5, 10.5]):
        for sx in (-1, 1):
            x = sx * (W / 2 - 0.08)
            cyl("sconce", 0.03, 0.12, (x, y, 1.7), brass, coll=c)
            sphere("sc_flame", 0.008, (x, y, 1.79), mat_emit("flame", kelvin(1700), 60), scale=(1, 1, 2.5), coll=c)
            light(f"sconce_l{i}{sx}", "POINT", (x - sx * 0.05, y, 1.82), 5 if not warm else 14, kelvin(1800), size=0.02, coll=c)
    world_color((0.002, 0.003, 0.005), 1.0)
    return A
