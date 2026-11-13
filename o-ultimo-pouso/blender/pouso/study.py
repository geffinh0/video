"""Escritório de Arthur Blackwood (cenário principal). Coordenadas em metros.
Sala: x∈[-3,3], y∈[-2.6,2.6], z∈[0,3.4]. Janela gótica na parede x=-3; porta na parede do fundo y=+2.6."""
import bpy, math, random
from mathutils import Vector
from .core import *
from .core import _move

TEX = None
ROOM = dict(x0=-3.0, x1=3.0, y0=-2.6, y1=2.6, h=3.4)
A = {}  # âncoras importantes (posições de câmera/atores)

def _pointed_arch(w, h_rect, h_arch, n=12):
    """Contorno de janela gótica (retângulo + arco ogival) no plano YZ, base em z=0, centrada em y=0."""
    pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h_rect)]
    r = w  # arco ogival: dois arcos de raio = largura
    for i in range(1, n + 1):
        a = math.radians(180) - math.acos(0.5) * i / n
        pts.append((-w / 2 + r * math.cos(math.pi - (math.pi - a)) + w, h_rect + r * math.sin(math.pi - a) * (h_arch / (r * math.sin(math.acos(0.5))))))
    pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h_rect)]
    for i in range(1, n):
        t = i / n; ang = math.acos(0.5) * t          # do lado direito subindo até o topo
        pts.append((w / 2 - r + r * math.cos(ang), h_rect + r * math.sin(ang) * h_arch / (r * math.sin(math.acos(0.5)))))
    pts.append((0, h_rect + h_arch))
    for i in range(n - 1, 0, -1):
        t = i / n; ang = math.acos(0.5) * t
        pts.append((-(w / 2 - r + r * math.cos(ang)), h_rect + r * math.sin(ang) * h_arch / (r * math.sin(math.acos(0.5)))))
    pts.append((-w / 2, h_rect))
    return pts

def _poly_mesh(name, pts2d, plane="YZ", depth=0.0):
    me = bpy.data.meshes.new(name)
    if plane == "YZ": v = [(0, p[0], p[1]) for p in pts2d]
    else: v = [(p[0], p[1], 0) for p in pts2d]
    me.from_pydata(v, [], [list(range(len(v)))]); me.update()
    return me

def build(tex_dir, with_arthur_chair=True):
    global TEX; TEX = tex_dir
    c = coll("study")
    R = ROOM
    wood = mat_pbr("dark_wood", "dark_wood", 1.2, tint=(0.55, 0.42, 0.36), value=0.55, sat=0.8, rough=0.85)
    wood2 = mat_pbr("walnut", "wood_table_001", 1.5, tint=(0.75, 0.5, 0.4), value=0.6, sat=0.85, rough=0.7)
    paper_wall = mat_wallpaper("wallpaper")
    floor = mat_pbr("floor", "wood_floor_deck", 0.7, tint=(0.6, 0.48, 0.42), value=0.4, sat=0.55, rough=0.8)
    ceil = mat_pbr("ceiling", "plastered_wall", 0.5, tint=(0.5, 0.48, 0.44), value=0.35, sat=0.5)
    def piece(name, loc, rot_z=0.0, scale=1.0, part=None, parent=None, **kw):
        """Peça do Poly Haven regraduada. part: mantém só o objeto com esse nome e o centraliza."""
        r, obs = asset(name, loc, rot_z, scale, coll=c, parent=parent, **kw)
        if part:
            for k, o in obs.items():
                if k == part: o.location = (0, 0, 0)
                else: bpy.data.objects.remove(o)
            obs = {part: obs[part]}
        return r, obs
    brass = mat("brass", (0.55, 0.38, 0.15), 0.35, 1.0)
    stone = mat_noise("stone", (0.08, 0.08, 0.085), (0.2, 0.2, 0.21), 5, rough=0.85, bump=0.4)
    # piso, teto, rodapé
    box("floor", (R["x1"] - R["x0"], R["y1"] - R["y0"], 0.05), (0, 0, -0.025), floor, coll=c)
    box("ceiling", (R["x1"] - R["x0"], R["y1"] - R["y0"], 0.1), (0, 0, R["h"] + 0.05), ceil, coll=c)
    for i, y in enumerate([-1.6, -0.2, 1.2]):
        box(f"beam{i}", (6.0, 0.22, 0.25), (0, y, R["h"] - 0.12), wood, coll=c)
    # paredes (x+, y-, y+ com recorte da porta; x- com recorte da janela)
    wy, wh = 0.5, 1.15  # janela: centro y, largura
    sill, h_rect, h_arch = 0.95, 1.35, 0.75
    def wall(name, size, loc):
        box(name, size, loc, paper_wall, bevel=0, coll=c)
        box(name + "_wains", (size[0] + (0.02 if size[0] < 0.2 else 0), size[1] + (0.02 if size[1] < 0.2 else 0), 1.05), (loc[0], loc[1], 0.525), wood, coll=c)
    wall("wall_xp", (0.1, 5.2, R["h"]), (R["x1"] + 0.05, 0, R["h"] / 2))
    wall("wall_ym", (6.0, 0.1, R["h"]), (0, R["y0"] - 0.05, R["h"] / 2))
    # fundo com porta (x 1.1..2.1)
    dx0, dx1, dh = 1.1, 2.1, 2.35
    wall("wall_yp_a", (dx0 - R["x0"], 0.1, R["h"]), ((R["x0"] + dx0) / 2, R["y1"] + 0.05, R["h"] / 2))
    wall("wall_yp_b", (R["x1"] - dx1, 0.1, R["h"]), ((dx1 + R["x1"]) / 2, R["y1"] + 0.05, R["h"] / 2))
    box("wall_yp_top", (dx1 - dx0, 0.1, R["h"] - dh), ((dx0 + dx1) / 2, R["y1"] + 0.05, (R["h"] + dh) / 2), paper_wall, bevel=0, coll=c)
    # parede da janela: blocos ao redor da abertura
    xw = R["x0"] - 0.05; top = sill + h_rect + h_arch
    box("wall_xm_a", (0.1, (wy - wh / 2) - R["y0"], R["h"]), (xw, (R["y0"] + wy - wh / 2) / 2, R["h"] / 2), paper_wall, bevel=0, coll=c)
    box("wall_xm_b", (0.1, R["y1"] - (wy + wh / 2), R["h"]), (xw, (R["y1"] + wy + wh / 2) / 2, R["h"] / 2), paper_wall, bevel=0, coll=c)
    box("wall_xm_low", (0.1, wh, sill), (xw, wy, sill / 2), wood, bevel=0, coll=c)
    box("wall_xm_top", (0.1, wh, R["h"] - top + 0.02), (xw, wy, (R["h"] + top) / 2), paper_wall, bevel=0, coll=c)
    # tímpano do arco: duas cunhas preenchendo os cantos acima do retângulo
    arch = _pointed_arch(wh, 0, h_arch)
    for side in (-1, 1):
        pts = [(side * wh / 2, 0), (side * wh / 2, h_arch + 0.02)] + [p for p in arch if p[0] * side >= -1e-6 and p[1] > 0][::(-1 if side > 0 else 1)]
        me = _poly_mesh(f"tymp{side}", [(side * wh / 2, h_arch + 0.02), (0, h_arch + 0.02)] + sorted([p for p in arch if p[0] * side >= -1e-6 and p[1] >= 0], key=lambda p: -p[1] if side > 0 else -p[1]))
        o = obj_from_mesh(f"tymp{side}", me, paper_wall, (xw + 0.04, wy, sill + h_rect), coll=c)
        o.modifiers.new("s", "SOLIDIFY").thickness = 0.1
    # vidro, caixilho e chumbo
    gl = obj_from_mesh("window_glass", _poly_mesh("glass", _pointed_arch(wh, h_rect, h_arch)), mat_glass_rain(), (R["x0"] - 0.02, wy, sill), coll=c)
    fr = obj_from_mesh("window_frame", _poly_mesh("frame", _pointed_arch(wh + 0.12, h_rect, h_arch + 0.06)), wood, (R["x0"] - 0.03, wy, sill - 0.03), coll=c)
    fr.modifiers.new("w", "WIREFRAME").thickness = 0.07
    lead = mat("lead", (0.02, 0.02, 0.022), 0.5, 0.6)
    for yy in (-wh / 6, wh / 6): box("mullion", (0.03, 0.025, h_rect + h_arch * 0.7), (R["x0"] - 0.01, wy + yy, sill + (h_rect + h_arch * 0.7) / 2), lead, coll=c)
    for zz in (0.45, 0.9, 1.35): box("transom", (0.03, wh, 0.02), (R["x0"] - 0.01, wy, sill + zz), lead, coll=c)
    box("sill_in", (0.3, wh + 0.2, 0.06), (R["x0"] + 0.1, wy, sill - 0.03), wood, coll=c)
    box("sill_out", (0.45, wh + 0.35, 0.1), (R["x0"] - 0.25, wy, sill - 0.08), stone, coll=c)
    A["window"] = Vector((R["x0"], wy, sill + 0.8)); A["sill_out"] = Vector((R["x0"] - 0.22, wy, sill - 0.03))
    # exterior: noite, árvores mortas em silhueta, luar
    night = mat_emit("night_sky", (0.012, 0.03, 0.045), 1.0)
    plane("night_bg", (0.1, 1), (-9, 0.5, 2), night, rot=(0, math.radians(90), 0), coll=c).scale = (1, 30, 14)
    ink = mat("silhouette", (0.003, 0.004, 0.005), 0.9)
    for i in range(7):
        y = random.uniform(-4, 5); x = random.uniform(-8.5, -5)
        cyl(f"tree_trunk{i}", random.uniform(0.08, 0.18), 7, (x, y, 2.5), ink, verts=8, r2=0.03, coll=c)
        for k in range(4):
            br = cyl(f"tree_br{i}{k}", 0.04, random.uniform(1.2, 2.5), (x, y + random.uniform(-0.6, 0.6), random.uniform(2.5, 5)), ink, rot=(random.uniform(-1, 1), random.uniform(-0.6, 0.6), 0), verts=6, r2=0.005, coll=c)
    mo = light("moon", "AREA", (R["x0"] - 2.2, wy + 0.4, 3.6), 380, kelvin(9500), size=1.6, coll=c); mo.rotation_euler = (0, math.radians(-55), 0)
    mr = light("moon_rim", "AREA", (-6, 3.5, 2.5), 300, kelvin(11000), size=3, coll=c); mr.rotation_euler = (0, math.radians(-90), 0)
    for o_ in (mo, mr): o_.visible_camera = False; o_.visible_glossy = False; o_.visible_transmission = False
    # cortinas (veludo vinho) com dobras
    velvet = mat_pbr("velvet", "velour_velvet", 3.0, tint=(0.32, 0.02, 0.04), value=0.3, sat=1.0)
    for side in (-1, 1):
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=40, y_subdivisions=12, size=1)
        cu = bpy.context.object; cu.name = f"curtain{side}"; cu.scale = (0.5, 3.0, 1)
        bpy.ops.object.transform_apply(scale=True)
        cu.rotation_euler = (math.radians(90), 0, math.radians(90)); cu.location = (R["x0"] + 0.12, wy + side * (wh / 2 + 0.22), 1.75)
        wv = cu.modifiers.new("folds", "WAVE"); wv.use_normal = True; wv.use_x = True; wv.use_y = False; wv.height = 0.045; wv.width = 0.12; wv.narrowness = 1.2; wv.speed = 0
        cu.modifiers.new("sol", "SOLIDIFY").thickness = 0.01
        bpy.ops.object.shade_smooth(); cu.data.materials.append(velvet); _move(cu, c)
    cyl("curtain_rod", 0.018, 2.0, (R["x0"] + 0.12, wy, 3.12), brass, rot=(math.radians(90), 0, 0), coll=c)
    # tapete
    rug = mat_pbr("rug", "fabric_pattern_07", 1.6, tint=(0.55, 0.12, 0.1), value=0.45, sat=0.9)
    box("rug", (3.6, 2.6, 0.012), (0.1, 0.1, 0.006), rug, coll=c)
    # escrivaninha
    D = empty("desk", (0, 0.15, 0), coll=c); A["desk"] = Vector((0, 0.15, 0.78))
    box("desk_top", (1.7, 0.85, 0.05), (0, 0.15, 0.78), wood2, bevel=0.01, coll=c)
    for sx in (-1, 1):
        box(f"desk_ped{sx}", (0.45, 0.78, 0.74), (sx * 0.6, 0.15, 0.38), wood2, coll=c)
        for k in range(3):
            box(f"desk_drw_front{sx}{k}", (0.4, 0.015, 0.2), (sx * 0.6, 0.15 - 0.395, 0.14 + k * 0.23), wood, coll=c)
            sphere(f"desk_knob{sx}{k}", 0.015, (sx * 0.6, 0.15 - 0.41, 0.14 + k * 0.23), brass, coll=c)
    box("desk_back", (0.75, 0.03, 0.7), (0, 0.15 + 0.38, 0.4), wood2, coll=c)
    # gaveta central (animável: abre em -y)
    dr = empty("drawer", (0, -0.27, 0.69), coll=c); A["drawer"] = dr
    box("drawer_front", (0.7, 0.02, 0.12), (0, -0.01, 0), wood, parent=dr, coll=c)
    box("drawer_box", (0.66, 0.5, 0.09), (0, 0.24, -0.005), wood2, parent=dr, coll=c)
    sphere("drawer_knob", 0.018, (0, -0.03, 0), brass, parent=dr, coll=c)
    # papéis e manuscrito
    man = mat_image("manuscript", f"{TEX}/manuscript.png", 0.8)
    for i in range(5):
        box(f"paperstack{i}", (0.22, 0.3, 0.003), (0.45 + random.uniform(-0.02, 0.02), 0.32, 0.806 + i * 0.004), man, rot=(0, 0, random.uniform(-0.1, 0.1)), bevel=0, coll=c)
    pg = box("manuscript_page", (0.24, 0.33, 0.002), (-0.05, -0.02, 0.807), man, rot=(0, 0, 0.08), bevel=0, coll=c)
    A["page"] = pg.location.copy()
    # tinteiro e pena
    inkg = mat("ink_glass", (0.02, 0.03, 0.05), 0.05, transmission=0.6)
    cyl("inkwell", 0.035, 0.05, (0.22, 0.12, 0.83), inkg, coll=c)
    quill = mat("quill", (0.75, 0.72, 0.68), 0.6, sss=0.2)
    q = sphere("quill", 0.1, (0.3, 0.1, 0.9), quill, scale=(0.12, 0.6, 0.02), seg=24, coll=c); q.rotation_euler = (0.9, 0.2, 0.4)
    # castiçais e velas (chama emissiva + luz)
    wax = mat("wax", (0.85, 0.8, 0.68), 0.5, sss=0.5)
    flame = mat_emit("flame", kelvin(1700), 60)
    A["candles"] = []
    for i, (x, y) in enumerate([(0.62, 0.42), (-0.55, 0.45)]):
        piece("brass_candleholders", (x, y, 0.805), rot_z=i * 1.3, scale=0.62 if i == 0 else 0.5, part="brass_candleholder_01", tint=(0.8, 0.62, 0.4), value=0.8, key=f"cstick{i}")
        top = 0.805 + 0.366 * (0.62 if i == 0 else 0.5) - 0.012
        hgt = 0.16 if i == 0 else 0.09
        cyl(f"candle{i}", 0.014, hgt, (x, y, top + hgt / 2), wax, coll=c)
        for k in range(3): sphere(f"drip{i}{k}", 0.006, (x + 0.012 * math.cos(k * 2.1), y + 0.012 * math.sin(k * 2.1), top + hgt * (0.35 + 0.2 * k)), wax, scale=(1, 1, 2.2), seg=10, coll=c)
        fz = top + hgt + 0.022
        fl = sphere(f"flame{i}", 0.009, (x, y, fz), flame, scale=(1, 1, 2.8), seg=16, coll=c)
        L = light(f"candle_light{i}", "POINT", (x, y, fz + 0.02), 45 if i == 0 else 30, kelvin(1800), size=0.015, coll=c)
        A["candles"].append((fl, L))
    # livros na mesa (enciclopédia envelhecida) e óculos de Arthur
    piece("book_encyclopedia_set_01", (-0.78, 0.2, 0.805), rot_z=math.radians(78), scale=0.85, tint=(0.6, 0.42, 0.35), value=0.55, sat=0.7, key="deskbooks")
    piece("round_spectacles", (0.2, -0.12, 0.807), rot_z=math.radians(200), tint=(0.9, 0.8, 0.6), key="spectacles")
    # porta-retrato (foto aplicada depois)
    frm = mat("frame_silver", (0.4, 0.38, 0.35), 0.3, 1.0)
    pf = empty("photo_frame", (-0.35, 0.38, 0.8), (math.radians(-12), 0, math.radians(15)), coll=c)
    box("photo_border", (0.17, 0.012, 0.22), (0, 0, 0.11), frm, parent=pf, coll=c)
    box("photo_back", (0.03, 0.12, 0.012), (0, 0.05, 0.08), frm, rot=(math.radians(60), 0, 0), parent=pf, coll=c)
    import os
    ph = f"{TEX}/photo_couple.png"
    if os.path.exists(ph):
        box("photo_img", (0.14, 0.004, 0.19), (0, -0.008, 0.11), mat_image("photo_couple", ph, 0.35), parent=pf, coll=c, bevel=0)
    A["photo_frame"] = pf
    # cadeiras
    if with_arthur_chair:
        ch = empty("arthur_chair", (0, -0.75, 0), coll=c); A["arthur_chair"] = ch
        piece("dining_chair_02", (0, 0.02, 0), rot_z=math.radians(180), scale=1.0, parent=ch, tint=(0.4, 0.2, 0.16), value=0.5, sat=0.8, key="ach")
    ech = empty("eleanor_chair", (0, 1.05, 0), coll=c); A["eleanor_chair"] = Vector((0, 1.05, 0.48))
    piece("ArmChair_01", (0, 0.05, 0), rot_z=0.0, scale=1.0, parent=ech, tint=(0.42, 0.035, 0.06), value=0.55, sat=1.0, rough=1.1, key="ech")
    # estantes de livros (parede x+ e fundo à esquerda)
    def shelf(x, y, w, rot_z, n_sh=6):
        g = empty(f"shelf_{x}_{y}", (x, y, 0), (0, 0, rot_z), coll=c)
        box("sh_back", (w, 0.03, 3.0), (0, 0.18, 1.5), wood, parent=g, coll=c)
        for sx in (-1, 1): box("sh_side", (0.04, 0.38, 3.0), (sx * w / 2, 0, 1.5), wood, parent=g, coll=c)
        for k in range(n_sh):
            z = 0.12 + k * 0.48
            box("sh_board", (w, 0.38, 0.03), (0, 0, z), wood, parent=g, coll=c)
            xx = -w / 2 + 0.05
            while xx < w / 2 - 0.08:
                bw = random.uniform(0.03, 0.07); bh = random.uniform(0.25, 0.4)
                col = random.choice([(0.12, 0.03, 0.02), (0.04, 0.06, 0.04), (0.1, 0.07, 0.04), (0.05, 0.04, 0.06), (0.15, 0.1, 0.05)])
                m = mat_noise(f"book_{col}", col, tuple(min(1, v * 1.8) for v in col), 25, rough=0.65)
                box("bk", (bw, 0.26, bh), (xx + bw / 2, 0.02, z + 0.015 + bh / 2), m, rot=(0, random.uniform(-0.04, 0.04) if random.random() < 0.2 else 0, 0), parent=g, coll=c)
                xx += bw + random.uniform(0.0, 0.01)
                if random.random() < 0.06: xx += 0.15
        return g
    shelf(2.78, -0.9, 1.6, math.radians(90))
    shelf(2.78, 0.9, 1.6, math.radians(90))
    piece("GothicCabinet_01", (-0.95, 2.02, 0), rot_z=0.0, tint=(0.5, 0.33, 0.27), value=0.5, sat=0.75, key="gcabinet")
    piece("brass_candleholders", (-0.95, 2.0, 2.36), rot_z=0.4, scale=0.8, part="brass_candleholder_03", tint=(0.7, 0.55, 0.35), value=0.7, key="candelabra")
    # canto da janela: cômoda gótica com lampião, busto de mármore e vaso
    piece("GothicCommode_01", (-2.68, -1.55, 0), rot_z=math.radians(90), tint=(0.5, 0.33, 0.27), value=0.5, sat=0.75, key="commode")
    piece("vintage_oil_lamp", (-2.66, -1.2, 1.21), tint=(0.8, 0.65, 0.45), value=0.7, key="oillamp")
    piece("marble_bust_01", (-2.68, -1.85, 1.21), rot_z=math.radians(70), tint=(0.75, 0.74, 0.7), value=0.6, sat=0.4, key="bust")
    piece("side_table_tall_01", (2.55, 2.2, 0), tint=(0.45, 0.3, 0.25), value=0.5, key="sidetable")
    piece("antique_ceramic_vase_01", (2.55, 2.2, 0.76), tint=(0.5, 0.55, 0.6), value=0.6, sat=0.6, key="vase")
    piece("Chandelier_03", (0.0, 0.3, R["h"] - 0.12), scale=1.25, tint=(0.6, 0.5, 0.35), value=0.6, key="chandelier")
    piece("ornate_mirror_01", (0.5, R["y1"] - 0.02, 2.0), rot_z=0.0, scale=1.5, tint=(0.75, 0.6, 0.35), value=0.6, key="mirror")
    # relógio de pêndulo (canto do fundo, perto da janela)
    ck = empty("clock", (-2.35, 2.28, 0), (0, 0, 0), coll=c); A["clock"] = ck
    _, cko = piece("vintage_grandfather_clock_01", (0, 0, 0), scale=1.08, parent=ck, tint=(0.55, 0.36, 0.3), value=0.55, sat=0.8, key="gclock")
    for nm, dlt in (("vintage_grandfather_clock_01_HourHand", 140.5), ("vintage_grandfather_clock_01_MinuteHand", -114.0)):
        h = cko[nm]; h.rotation_mode = "XYZ"; h.rotation_euler = (0, math.radians(dlt), 0)
    A["clock_hands"] = (cko["vintage_grandfather_clock_01_HourHand"], cko["vintage_grandfather_clock_01_MinuteHand"])
    cf = empty("ck_face", (0, -0.14, 1.732 * 1.08), parent=ck, coll=c)
    A["clock_face"] = cf
    bpy.data.materials.get("clock_face") or mat_image("clock_face", f"{TEX}/clock_face.png", 0.6)
    pv = empty("pendulum", (0, 0.0, 1.5), parent=ck, coll=c); A["pendulum"] = pv
    cyl("pend_rod", 0.006, 0.75, (0, 0, -0.38), brass, parent=pv, coll=c)
    cyl("pend_bob", 0.075, 0.02, (0, 0, -0.76), brass, rot=(math.radians(90), 0, 0), parent=pv, coll=c)
    # porta do fundo (animável: dobradiça em x=dx0)
    jamb = wood
    box("door_frame_l", (0.08, 0.16, dh), (dx0 - 0.04, R["y1"], dh / 2), jamb, coll=c)
    box("door_frame_r", (0.08, 0.16, dh), (dx1 + 0.04, R["y1"], dh / 2), jamb, coll=c)
    box("door_frame_t", (dx1 - dx0 + 0.16, 0.16, 0.1), ((dx0 + dx1) / 2, R["y1"], dh + 0.05), jamb, coll=c)
    hinge = empty("door_hinge", (dx0, R["y1"] + 0.02, 0), coll=c); A["door"] = hinge
    box("door_panel", (dx1 - dx0, 0.05, dh), ((dx1 - dx0) / 2, 0, dh / 2), wood2, parent=hinge, coll=c)
    for zz in (0.55, 1.6):
        box("door_inset", (0.7, 0.01, 0.75), ((dx1 - dx0) / 2, -0.03, zz), wood, parent=hinge, coll=c)
    sphere("door_knob", 0.03, (dx1 - dx0 - 0.1, -0.06, 1.0), brass, parent=hinge, coll=c)
    hinge.rotation_euler = (0, 0, math.radians(-18))  # entreaberta
    box("corridor_void", (2.0, 0.1, 3.0), ((dx0 + dx1) / 2, R["y1"] + 1.2, 1.5), mat("void", (0.0, 0.0, 0.0), 1.0), coll=c)
    light("corridor_faint", "POINT", ((dx0 + dx1) / 2, R["y1"] + 0.8, 2.0), 14, kelvin(7000), size=0.3, coll=c)
    # quadros na parede
    paint = mat_noise("painting", (0.02, 0.018, 0.012), (0.09, 0.07, 0.04), 2.5, rough=0.4, bump=0.05)
    gold = mat("gilt", (0.35, 0.24, 0.08), 0.35, 1.0)
    for i, (y, z, sc, nm) in enumerate([(-1.55, 2.25, 1.5, "fancy_picture_frame_02"), (-0.55, 2.3, 1.0, "fancy_picture_frame_01")]):
        _, fo = piece(nm, (R["x0"] + 0.02, y, z), rot_z=math.radians(90), scale=sc, tint=(0.7, 0.55, 0.3), value=0.6, key=f"pframe{i}")
        cv = fo.get(nm + "_canvas")
        if cv: cv.data.materials.clear(); cv.data.materials.append(paint)
    # preenchimento muito fraco (para não perder totalmente as sombras)
    world_color((0.004, 0.006, 0.01), 1.0)
    return A
