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
    bark = bark or mat_noise("bark", (0.015, 0.013, 0.012), (0.05, 0.045, 0.04), 18, rough=0.95, bump=0.6, stretch=(4, 4, 0.5))
    rnd = random.Random(seed); trees = []
    for i in range(n):
        x = center[0] + rnd.uniform(-radius, radius); y = center[1] + rnd.uniform(-radius * 0.3, radius)
        if clear and (Vector((x, y)) - Vector(clear[0])).length < clear[1]: continue
        trees.append(dead_tree(f"tree{i}", (x, y, 0), rnd.uniform(7, 14), bark, c, seed * 100 + i))
    return trees

def ground(c, size=200):
    g = mat_noise("mud", (0.006, 0.006, 0.005), (0.018, 0.017, 0.014), 0.6, rough=0.9, bump=0.5)
    o = plane("ground", (size, size), (0, 0, 0), g, coll=c)
    # relevo suave
    md = o.modifiers.new("sub", "SUBSURF"); md.subdivision_type = "SIMPLE"; md.levels = 5; md.render_levels = 5
    tx = bpy.data.textures.new("terrain", "CLOUDS"); tx.noise_scale = 18
    dp = o.modifiers.new("disp", "DISPLACE"); dp.texture = tx; dp.strength = 1.2
    return o

def mansion(c, loc=(0, 30, 0), lit_window=True):
    """Mansão vitoriana gótica: corpo principal, ala, torre com telhado agudo, empenas, chaminés, janelas."""
    stone = mat_noise("mansion_stone", (0.025, 0.026, 0.028), (0.07, 0.07, 0.075), 3, rough=0.9, bump=0.5)
    roof = mat_noise("slate", (0.012, 0.014, 0.017), (0.035, 0.04, 0.045), 12, rough=0.7, bump=0.4, stretch=(1, 1, 6))
    dark_win = mat("dark_window", (0.004, 0.005, 0.006), 0.1, 0.0)
    warm = mat_emit("warm_window", kelvin(1900), 6.0)
    root = empty("mansion", loc, coll=c); L = Vector(loc)
    def B(n, s, p, m=stone): return box(n, s, tuple(L + Vector(p)), m, bevel=0.02, coll=c)
    def roof_gable(n, w, d, h, p, rotz=0):
        me = bpy.data.meshes.new(n)
        v = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (w / 2, d / 2, 0), (-w / 2, d / 2, 0), (0, -d / 2, h), (0, d / 2, h)]
        me.from_pydata(v, [], [(0, 1, 4), (3, 5, 2), (0, 4, 5, 3), (1, 2, 5, 4), (0, 3, 2, 1)]); me.update()
        o = obj_from_mesh(n, me, roof, tuple(L + Vector(p)), (0, 0, rotz), coll=c)
        o.modifiers.new("sol", "SOLIDIFY").thickness = 0.15
        return o
    B("m_main", (16, 9, 9), (0, 0, 4.5)); roof_gable("m_roof", 16.6, 9.6, 5.5, (0, 0, 9), 0)
    B("m_wing", (7, 7, 7), (-10.5, -1, 3.5)); roof_gable("m_wroof", 7.6, 7.6, 4.0, (-10.5, -1, 7), math.radians(90))
    B("m_tower", (4, 4, 15), (8.5, -3.5, 7.5))
    cone = cyl("m_tspire", 3.0, 7, tuple(L + Vector((8.5, -3.5, 18.5))), roof, verts=4, r2=0.05, rot=(0, 0, math.radians(45)), coll=c, smooth=False)
    for i, x in enumerate([-5, 4]):
        B(f"m_chimney{i}", (1.0, 1.0, 4), (x, 1.5, 12))
    for k, x in enumerate([-3.5, 3.5]):
        B(f"m_gablefront{k}", (4, 1, 3), (x, -4.7, 9.5)); roof_gable(f"m_gable{k}", 4.6, 2.0, 2.6, (x, -4.7, 11), 0)
    B("m_porch", (5, 2.5, 0.4), (0, -5.8, 3.2), roof)
    for sx in (-2.0, 2.0): B(f"m_pillar{sx}", (0.4, 0.4, 3.2), (sx, -6.6, 1.6))
    wins = []
    for row, z in enumerate([2.5, 6.5]):
        for col, x in enumerate([-6.5, -3.5, 3.5, 6.5]):
            m = warm if (lit_window and row == 1 and col == 0) else dark_win
            w = B(f"m_win{row}{col}", (1.1, 0.2, 2.0), (x, -4.55, z), m)
            B(f"m_wtop{row}{col}", (1.3, 0.25, 0.2), (x, -4.6, z + 1.1))
            wins.append(w)
    for z in (4, 9, 13): B(f"m_twin{z}", (0.9, 0.2, 1.6), (8.5, -5.55, z), dark_win)
    if lit_window:
        light("m_win_light", "POINT", tuple(L + Vector((-6.5, -3.5, 6.5))), 400, kelvin(1900), size=0.5, coll=c)
    return root, L + Vector((-6.5, -4.65, 6.5))

def statue(c, loc=(0, 0, 0)):
    """Pedestal com urna de pedra (onde o corvo pousa). Retorna o ponto de pouso."""
    st = mat_noise("statue_stone", (0.06, 0.062, 0.06), (0.16, 0.16, 0.15), 6, rough=0.95, bump=0.8)
    moss = mat_noise("moss", (0.01, 0.018, 0.01), (0.03, 0.045, 0.025), 20, rough=1.0, bump=0.6)
    L = Vector(loc)
    box("st_base", (1.0, 1.0, 0.25), tuple(L + Vector((0, 0, 0.125))), st, bevel=0.03, coll=c)
    box("st_column", (0.7, 0.7, 1.4), tuple(L + Vector((0, 0, 0.95))), st, bevel=0.03, coll=c)
    box("st_cap", (0.9, 0.9, 0.18), tuple(L + Vector((0, 0, 1.74))), st, bevel=0.03, coll=c)
    # urna: perfil torneado (screw)
    prof = [(0.12, 0.0), (0.2, 0.05), (0.14, 0.12), (0.26, 0.3), (0.3, 0.45), (0.25, 0.6), (0.18, 0.66), (0.24, 0.7)]
    me = bpy.data.meshes.new("urn"); me.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], []); me.update()
    u = obj_from_mesh("st_urn", me, st, tuple(L + Vector((0, 0, 1.83))), coll=c)
    sc = u.modifiers.new("lathe", "SCREW"); sc.steps = 48; sc.render_steps = 48; sc.use_smooth_shade = True
    u.modifiers.new("sol", "SOLIDIFY").thickness = 0.03
    sd = u.modifiers.new("sub", "SUBSURF"); sd.levels = 1; sd.render_levels = 2
    box("st_moss", (0.92, 0.92, 0.02), tuple(L + Vector((0, 0, 1.835))), moss, bevel=0.01, coll=c)
    return L + Vector((0, 0.05, 2.53))

def night(sky=(0.006, 0.012, 0.02), moon_energy=3.0, moon_dir=(math.radians(35), 0, math.radians(150))):
    world_color(sky, 1.0)
    sun = bpy.data.lights.new("moonlight", "SUN"); sun.energy = moon_energy; sun.color = kelvin(9000); sun.angle = math.radians(2)
    o = bpy.data.objects.new("moonlight", sun); bpy.context.scene.collection.objects.link(o); o.rotation_euler = moon_dir
    return o
