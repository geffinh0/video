"""Exterior: floresta de árvores mortas, mansão vitoriana, estátua de pedra. Noite, neblina, luar."""
import bpy, math, random
from mathutils import Vector
from .core import *
from .core import _move, _bsdf, _n

def _branch(name, p0, d, length, r, depth, mtl, c, rnd, parts):
    p1 = p0 + d * length
    parts.append((p0, p1, r))
    if depth == 0: return
    for k in range(rnd.randint(2, 3)):
        nd = (d + Vector((rnd.uniform(-0.9, 0.9), rnd.uniform(-0.9, 0.9), rnd.uniform(-0.2, 0.5)))).normalized()
        _branch(name, p0 + d * length * rnd.uniform(0.6, 1.0), nd, length * rnd.uniform(0.5, 0.75), r * 0.55, depth - 1, mtl, c, rnd, parts)

def dead_tree(name, loc, height, mtl, c, seed, depth=4):
    """Árvore morta: tronco + galhos recursivos, malha única (skin)."""
    rnd = random.Random(seed); parts = []
    _branch(name, Vector(loc), Vector((rnd.uniform(-0.08, 0.08), rnd.uniform(-0.08, 0.08), 1)).normalized(), height * 0.45, height * 0.025, depth, mtl, c, rnd, parts)
    verts, edges, radii = [], [], []
    for p0, p1, r in parts:
        i = len(verts); verts += [tuple(p0), tuple(p1)]; edges.append((i, i + 1)); radii += [(r, r), (r * 0.6, r * 0.6)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts, edges, []); me.update()
    o = bpy.data.objects.new(name, me); c.objects.link(o)
    o.modifiers.new("skin", "SKIN")
    for v, rr in zip(me.skin_vertices[0].data, radii): v.radius = rr
    for k in range(0, len(verts), 2): me.skin_vertices[0].data[k].use_root = True
    o.data.materials.append(mtl)
    return o

def forest(c, center=(0, 0), radius=40, n=60, seed=5, clear=None, bark=None):
    bark = bark or mat_pbr("bark", "bark_brown_02", 0.6, tint=(0.5, 0.48, 0.46), value=0.3, sat=0.4, bump=2.0)
    rnd = random.Random(seed); trees = []
    for i in range(n):
        x = center[0] + rnd.uniform(-radius, radius); y = center[1] + rnd.uniform(-radius * 0.3, radius)
        if clear and (Vector((x, y)) - Vector(clear[0])).length < clear[1]: continue
        trees.append(dead_tree(f"tree{i}", (x, y, 0), rnd.uniform(7, 14), bark, c, seed * 100 + i))
    return trees

def ground(c, size=200):
    g = mat_pbr("mud", "forest_ground_04", 0.35, tint=(0.5, 0.52, 0.5), value=0.28, sat=0.5, bump=2.5)
    o = plane("ground", (size, size), (0, 0, 0), g, coll=c)
    # relevo suave
    md = o.modifiers.new("sub", "SUBSURF"); md.subdivision_type = "SIMPLE"; md.levels = 5; md.render_levels = 5
    tx = bpy.data.textures.new("terrain", "CLOUDS"); tx.noise_scale = 18
    dp = o.modifiers.new("disp", "DISPLACE"); dp.texture = tx; dp.strength = 1.2
    return o

def mansion(c, loc=(0, 30, 0), lit_window=True):
    """Mansão Blackwood (desenho próprio): vitoriana gótica assimétrica. Corpo principal com empena íngreme e
    águas-furtadas, torre central com mansarda e gradil de ferro, torreão redondo com cone, ala com bay window,
    chaminés altas, janelas ogivais. Frente em -y. Retorna (raiz, posição da janela acesa)."""
    stone = mat_pbr("mansion_stone", "castle_brick_02_red", 0.22, tint=(0.5, 0.52, 0.56), value=0.3, sat=0.25, bump=2.0)
    trim = mat_pbr("mansion_trim", "plastered_wall", 0.4, tint=(0.5, 0.52, 0.55), value=0.3, sat=0.2)
    roof = mat_pbr("slate", "slate_floor_02", 0.3, tint=(0.4, 0.45, 0.55), value=0.2, sat=0.4, bump=2.0)
    iron = mat("mansion_iron", (0.006, 0.007, 0.008), 0.5, 0.8)
    dark_win = mat("dark_window", (0.004, 0.005, 0.006), 0.08, 0.0)
    warm = mat_emit("warm_window", kelvin(1900), 6.0)
    root = empty("mansion", loc, coll=c); L = Vector(loc)
    def B(n, sz, p, m=stone, bev=0.02): return box(n, sz, tuple(L + Vector(p)), m, bevel=bev, coll=c)
    def gable(n, w, d, h, p, rotz=0):
        me = bpy.data.meshes.new(n)
        v = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (w / 2, d / 2, 0), (-w / 2, d / 2, 0), (0, -d / 2, h), (0, d / 2, h)]
        me.from_pydata(v, [], [(0, 1, 4), (3, 5, 2), (0, 4, 5, 3), (1, 2, 5, 4), (0, 3, 2, 1)]); me.update()
        o = obj_from_mesh(n, me, roof, tuple(L + Vector(p)), (0, 0, rotz), coll=c)
        o.modifiers.new("sol", "SOLIDIFY").thickness = 0.18
        return o
    def taper(n, r0, r1, h, p, verts=4, m=None, rz=45):
        return cyl(n, r0, h, tuple(L + Vector(p)), m or roof, verts=verts, r2=r1, rot=(0, 0, math.radians(rz)), coll=c, smooth=verts > 8)
    def gwin(n, x, y, z, w, h, lit=False, rz=0.0):
        """Janela ogival voltada para -y (ou girada): vidro, moldura de pedra, pinázios de ferro, peitoril."""
        g = empty(n, tuple(L + Vector((x, y, z))), (0, 0, rz), coll=c)
        pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h * 0.62)] + [(w / 2 * math.cos(t), h * 0.62 + h * 0.38 * math.sin(t) ** 0.8) for t in [math.pi * k / 16 for k in range(1, 16)]] + [(-w / 2, h * 0.62)]
        me = bpy.data.meshes.new(n); me.from_pydata([(px, 0, pz) for px, pz in pts], [], [list(range(len(pts)))]); me.update()
        gl = obj_from_mesh(n + "_gl", me, warm if lit else dark_win, (0, -0.02, 0), parent=g, coll=c)
        me2 = bpy.data.meshes.new(n + "f"); me2.from_pydata([(px * 1.12, 0, pz * 1.04 - 0.02 * h) for px, pz in pts], [], [list(range(len(pts)))]); me2.update()
        fr = obj_from_mesh(n + "_fr", me2, trim, (0, -0.06, 0), parent=g, coll=c); fr.modifiers.new("w", "WIREFRAME").thickness = 0.16 * w
        box(n + "_mul", (0.05 * w + 0.03, 0.05, h * 0.92), (0, -0.05, h * 0.46), iron, parent=g, coll=c, bevel=0)
        box(n + "_tr", (w, 0.05, 0.05), (0, -0.05, h * 0.5), iron, parent=g, coll=c, bevel=0)
        box(n + "_sill", (w * 1.3, 0.3, 0.12), (0, -0.1, -0.08), trim, parent=g, coll=c)
        return g
    def cresting(n, x0, x1, y, z, step=0.45, h=0.5):
        k = 0; x = x0
        while x <= x1:
            cyl(f"{n}{k}", 0.025, h, tuple(L + Vector((x, y, z + h / 2))), iron, verts=5, r2=0.004, coll=c); x += step; k += 1
        box(n + "_rail", (x1 - x0, 0.04, 0.04), tuple(L + Vector(((x0 + x1) / 2, y, z + 0.12))), iron, bevel=0, coll=c)
    # --- corpo principal ---
    B("m_main", (14, 9, 9), (0, 0, 4.5)); B("m_plinth", (14.4, 9.4, 0.9), (0, 0, 0.45), trim)
    B("m_band1", (14.3, 9.3, 0.25), (0, 0, 4.6), trim); B("m_cornice", (14.6, 9.6, 0.35), (0, 0, 9.05), trim)
    gable("m_roof", 14.8, 9.9, 6.8, (0, 0, 9.2), math.radians(90)); cresting("m_crest", -4.6, 4.6, 0, 15.95)
    for k, x in enumerate([-4.6, -1.6, 4.4]):       # águas-furtadas
        B(f"m_dormer{k}", (1.5, 2.2, 1.9), (x, -3.6, 10.7)); gable(f"m_dormroof{k}", 1.9, 2.4, 1.5, (x, -3.6, 11.65), 0)
        gwin(f"m_dormwin{k}", x, -4.72, 10.0, 0.8, 1.5)
    # --- torre central (entrada), mansarda, gradil e agulha ---
    tx, ty = 1.2, -5.6
    B("m_tower", (4.6, 4.6, 16.5), (tx, ty, 8.25)); B("m_tband", (4.9, 4.9, 0.3), (tx, ty, 12.2), trim); B("m_tcorn", (5.1, 5.1, 0.4), (tx, ty, 16.6), trim)
    taper("m_mansard", 3.55, 2.3, 3.6, (tx, ty, 18.6)); B("m_mtop", (3.4, 3.4, 0.2), (tx, ty, 20.5), trim)
    for sy in (-1, 1): cresting(f"m_tcrest{sy}", tx - 1.6, tx + 1.6, ty + sy * 1.6, 20.6, 0.4, 0.7)
    taper("m_spire", 0.5, 0.02, 3.5, (tx, ty, 22.3), verts=6, m=iron, rz=0)
    for z, hh in ((5.2, 2.6), (9.2, 2.6), (13.4, 2.4)): gwin(f"m_twin{z}", tx, ty - 2.32, z, 1.3, hh)
    gwin("m_mwin", tx, ty - 3.0, 17.4, 0.9, 1.6)
    asset("large_castle_door", tuple(L + Vector((tx, ty - 2.25, 0.75))), 0.0, 1.0, coll=c, tint=(0.5, 0.45, 0.42), value=0.35, sat=0.6, key="m_door")
    B("m_porchroof", (6.2, 3.2, 0.3), (tx, ty - 3.6, 4.35), trim); gable("m_porchgable", 6.4, 3.4, 1.8, (tx, ty - 3.6, 4.5), math.radians(90))
    for sx in (-2.7, 2.7):
        cyl(f"m_col{sx}", 0.22, 3.6, tuple(L + Vector((tx + sx, ty - 4.9, 2.55))), trim, verts=16, coll=c); B(f"m_colbase{sx}", (0.6, 0.6, 0.35), (tx + sx, ty - 4.9, 0.92), trim)
    for i in range(5): B(f"m_step{i}", (6.0 - i * 0.25, 0.55, 0.15), (tx, ty - 5.7 - (4 - i) * 0.5, 0.075 + i * 0.15), trim)
    # --- ala esquerda com empena frontal e bay window ---
    wx = -10.2
    B("m_wing", (6.6, 8, 7.6), (wx, -1.2, 3.8)); B("m_wplinth", (7.0, 8.4, 0.9), (wx, -1.2, 0.45), trim); B("m_wcorn", (7.0, 8.4, 0.3), (wx, -1.2, 7.65), trim)
    gable("m_wroof", 7.2, 8.6, 5.2, (wx, -1.2, 7.8), 0); gwin("m_wgablewin", wx, -5.3, 8.3, 0.9, 1.9)
    taper("m_bay", 1.9, 1.9, 6.4, (wx, -5.4, 3.2), verts=8, m=stone, rz=22.5); taper("m_bayroof", 2.15, 0.05, 2.4, (wx, -5.4, 7.6), verts=8, rz=22.5)
    for k, ang in enumerate((-45, 0, 45)):
        for z in (1.6, 4.3):
            gwin(f"m_baywin{k}{z}", wx + math.sin(math.radians(ang)) * 1.78, -5.4 - math.cos(math.radians(ang)) * 1.78, z, 0.85, 1.9, rz=math.radians(ang))
    # --- torreão redondo à direita com "chapéu de bruxa" ---
    rx, ry = 7.6, -4.0
    cyl("m_turret", 2.0, 13.5, tuple(L + Vector((rx, ry, 6.75))), stone, verts=24, coll=c); cyl("m_turcorn", 2.25, 0.4, tuple(L + Vector((rx, ry, 13.6))), trim, verts=24, coll=c)
    taper("m_turroof", 2.5, 0.03, 7.0, (rx, ry, 17.2), verts=24, rz=0); taper("m_turfinial", 0.06, 0.005, 1.6, (rx, ry, 21.4), verts=6, m=iron, rz=0)
    for z in (3.0, 7.0, 10.6): gwin(f"m_turwin{z}", rx, ry - 1.98, z, 0.8, 1.8)
    # --- janelas do corpo principal (a de cima à esquerda fica acesa) ---
    lit_pos = None
    for row, z in enumerate([1.8, 5.6]):
        for col, x in enumerate([-5.4, -2.7, 4.6]):
            lit = lit_window and row == 1 and col == 0
            gwin(f"m_win{row}{col}", x, -4.52, z, 1.2, 2.5, lit=lit)
            if lit: lit_pos = L + Vector((x, -4.65, z + 1.2))
    # --- chaminés ---
    for i, (x, y, h) in enumerate([(-5.2, 1.8, 8.5), (3.6, 1.5, 9.5), (-11.5, 0.5, 6.5)]):
        zb = 9.0 if i < 2 else 7.6
        B(f"m_chim{i}", (1.1, 1.1, h), (x, y, zb + h / 2)); B(f"m_chimcap{i}", (1.4, 1.4, 0.3), (x, y, zb + h + 0.15), trim)
        for sx in (-0.28, 0.28): cyl(f"m_pot{i}{sx}", 0.2, 0.7, tuple(L + Vector((x + sx, y, zb + h + 0.65))), trim, verts=10, r2=0.15, coll=c)
    # --- portão de ferro com pilares e mureta com lanças ---
    asset("large_iron_gate", tuple(L + Vector((tx, -19.0, 0))), 0.0, 1.15, coll=c, tint=(0.4, 0.42, 0.45), value=0.4, key="m_gate")
    for sx in (-1, 1):
        B(f"m_gatepost{sx}", (0.8, 0.8, 4.0), (tx + sx * 2.15, -19.0, 2.0)); taper(f"m_gatecap{sx}", 0.75, 0.05, 0.9, (tx + sx * 2.15, -19.0, 4.45), m=trim)
        for k in range(10):
            xx = tx + sx * (3.3 + k * 1.6)
            B(f"m_fencewall{sx}{k}", (1.6, 0.45, 1.0), (xx, -19.0, 0.5))
            for j in range(4): cyl(f"m_spike{sx}{k}{j}", 0.025, 1.4, tuple(L + Vector((xx - 0.6 + j * 0.4, -19.0, 1.7))), iron, verts=5, r2=0.004, coll=c)
    if lit_window and lit_pos is not None:
        light("m_win_light", "POINT", tuple(lit_pos + Vector((0, 1.2, 0))), 400, kelvin(1900), size=0.5, coll=c)
    return root, (lit_pos if lit_pos is not None else L + Vector((-5.4, -4.65, 6.8)))

def statue(c, loc=(0, 0, 0)):
    """Estátua gótica coroada sobre pedestal coberto de musgo (onde o corvo pousa). Retorna o ponto de pouso."""
    st = mat_pbr("statue_stone", "castle_brick_02_red", 0.5, tint=(0.55, 0.57, 0.55), value=0.4, sat=0.15, bump=1.5)
    moss = mat_noise("moss", (0.01, 0.018, 0.01), (0.03, 0.045, 0.025), 20, rough=1.0, bump=0.6)
    L = Vector(loc); ph = 0.85
    box("st_base", (1.5, 1.5, 0.25), tuple(L + Vector((0, 0, 0.125))), st, bevel=0.03, coll=c)
    box("st_column", (1.15, 1.15, ph - 0.37), tuple(L + Vector((0, 0, 0.25 + (ph - 0.37) / 2))), st, bevel=0.03, coll=c)
    box("st_cap", (1.35, 1.35, 0.12), tuple(L + Vector((0, 0, ph - 0.06))), st, bevel=0.03, coll=c)
    box("st_moss", (1.36, 1.36, 0.02), tuple(L + Vector((0, 0, ph + 0.005))), moss, bevel=0.01, coll=c)
    r, obs = asset("gothic_statue", tuple(L + Vector((0.05, -0.3, ph))), math.radians(180), 0.72, coll=c, tint=(0.6, 0.66, 0.62), value=0.45, sat=0.5, key="gstatue")
    bpy.context.view_layer.update()
    o = [x for x in obs.values() if x.type == "MESH"][0]; M = o.matrix_world
    zs = sorted(((M @ v.co) for v in o.data.vertices), key=lambda p: -p.z)[:40]
    top = sum(zs, Vector((0, 0, 0))) / len(zs)
    return Vector((top.x, top.y, max(p.z for p in zs) - 0.012))

def scatter(c, around=(0, 0), seed=3):
    """Troncos caídos, tocos e pedras perto da câmera (primeiro plano da floresta)."""
    rnd = random.Random(seed)
    for i, (nm, sc) in enumerate([("dead_tree_trunk_02", 1.0), ("tree_stump_01", 1.0), ("boulder_01", 0.8), ("dead_tree_trunk", 1.3), ("tree_stump_01", 0.8), ("boulder_01", 0.5)]):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(4, 11)
        asset(nm, (around[0] + math.cos(a) * d, around[1] + math.sin(a) * d, 0.02), rnd.uniform(0, 6.28), sc, coll=c, tint=(0.5, 0.52, 0.5), value=0.35, sat=0.5, key=f"sc{i}")

def night(sky=(0.006, 0.012, 0.02), moon_energy=3.0, moon_dir=(math.radians(35), 0, math.radians(150))):
    try: world_hdri("satara_night_no_lamps", 2.2, 1.0, tint=(0.5, 0.72, 1.0))
    except Exception: world_color(sky, 1.0)
    sun = bpy.data.lights.new("moonlight", "SUN"); sun.energy = moon_energy; sun.color = kelvin(9000); sun.angle = math.radians(2)
    o = bpy.data.objects.new("moonlight", sun); bpy.context.scene.collection.objects.link(o); o.rotation_euler = moon_dir
    return o
