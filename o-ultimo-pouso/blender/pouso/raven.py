"""O Corvo: modelo procedural articulado. Escala real (~60 cm do bico à cauda).
Hierarquia: root -> body, neck(head pivot) -> head, beak_up, beak_low(pivot), eyes; wing_L/R pivots; tail pivot."""
import bpy, math
from mathutils import Vector
from .core import *
from .core import _move, _bsdf, _n

def mat_feather(name="raven_feather"):
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, (0.003, 0.003, 0.004), 0.58, spec=0.18, coat=0.0); b = _bsdf(m); L = m.node_tree.links
    if "Specular Tint" in b.inputs: b.inputs["Specular Tint"].default_value = (0.42, 0.4, 0.85, 1)
    if "Coat Tint" in b.inputs: b.inputs["Coat Tint"].default_value = (0.55, 0.5, 0.95, 1)
    b.inputs["Coat Roughness"].default_value = 0.35
    tc = _n(m, "ShaderNodeTexCoord")
    mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 2.6, 1.0); L.new(tc.outputs["Object"], mp.inputs[0])
    vo = _n(m, "ShaderNodeTexVoronoi", Scale=55.0); L.new(mp.outputs[0], vo.inputs["Vector"])
    bp = _n(m, "ShaderNodeBump", Strength=0.3, Distance=0.002); L.new(vo.outputs["Distance"], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    nz = _n(m, "ShaderNodeTexNoise", Scale=40.0, Detail=4.0); L.new(tc.outputs["Object"], nz.inputs["Vector"])
    rr = _n(m, "ShaderNodeMapRange", **{"To Min": 0.45, "To Max": 0.7}); L.new(nz.outputs["Fac"], rr.inputs[0]); L.new(rr.outputs[0], b.inputs["Roughness"])
    return m

def _skin_body(name, verts, edges, radii, mtl, coll_):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, edges, []); me.update()
    o = bpy.data.objects.new(name, me); coll_.objects.link(o)
    o.modifiers.new("skin", "SKIN")
    for v, r in zip(me.skin_vertices[0].data, radii): v.radius = r
    me.skin_vertices[0].data[0].use_root = True
    sd = o.modifiers.new("sub", "SUBSURF"); sd.levels = 2; sd.render_levels = 3
    o.data.materials.append(mtl)
    for p in o.data.polygons: p.use_smooth = True
    return o

def _feather_fan(name, n, length, spread, width, mtl, coll_, parent, plane="YZ", droop=0.0):
    """Leque de penas sobrepostas. plane=YZ: painel vertical (asa dobrada contra o corpo); XY: horizontal (cauda)."""
    me = bpy.data.meshes.new(name); verts = []; faces = []
    for i in range(n):
        a = math.radians(-spread / 2 + spread * i / max(1, n - 1))
        ln = length * (0.7 + 0.3 * math.sin(math.pi * (i + 0.5) / n))
        if plane == "YZ": d = Vector((0, -math.cos(a), -math.sin(a) - droop)); nrm = Vector((0, -d.z, d.y)).normalized() * width
        else: d = Vector((math.sin(a), -math.cos(a), -droop)); nrm = Vector((d.y, -d.x, 0)).normalized() * width
        d.normalize(); b = len(verts); off = Vector((0.0015 * i, 0, 0)) if plane == "YZ" else Vector((0, 0, 0.0015 * i))
        base = off + d * 0.01
        verts += [base - nrm * 0.5, base + nrm * 0.5, base + d * ln * 0.88 + nrm * 0.42, base + d * ln, base + d * ln * 0.88 - nrm * 0.42]
        faces.append([b, b + 1, b + 2, b + 3, b + 4])
    me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    o = bpy.data.objects.new(name, me); coll_.objects.link(o); o.parent = parent
    o.modifiers.new("sol", "SOLIDIFY").thickness = 0.0025
    o.data.materials.append(mtl)
    for p in o.data.polygons: p.use_smooth = True
    return o

WING_REST = lambda sx: (math.radians(28), math.radians(-sx * 4), math.radians(sx * 3))
WING_OPEN = lambda sx: (math.radians(0), math.radians(-sx * 30), math.radians(sx * 95))

def _fuzz(o, mtl_hair, count=2500, length=0.012):
    """Penugem curta (hair) para quebrar o aspecto liso. Usado só nos closes."""
    ps = o.modifiers.new("fuzz", "PARTICLE_SYSTEM").particle_system.settings
    ps.type = "HAIR"; ps.count = count; ps.hair_length = length; ps.use_advanced_hair = True
    ps.child_type = "INTERPOLATED"; ps.child_percent = 6; ps.rendered_child_count = 6
    ps.root_radius = 0.0012; ps.tip_radius = 0.0; ps.radius_scale = 1.0
    ps.normal_factor = 0.6; ps.tangent_factor = 0.0; ps.factor_random = 0.2
    ps.use_hair_bspline = False; ps.display_step = 2; ps.render_step = 2
    ps.child_length = 1.0; ps.clump_factor = 0.6; ps.roughness_1 = 0.002
    o.data.materials.append(mtl_hair); ps.material = len(o.data.materials)

def _plumage(o, mtl, count, size, seed=1, lay=(0.0, -1.0, -0.25), rand=0.25, lift=0.22):
    """Cobre a malha com penas de contorno sobrepostas, deitadas na direção `lay` (espaço do pai).
    Gera uma malha única (rápida de renderizar), filha do mesmo pivô de `o`."""
    import random as Rn
    r = Rn.Random(seed)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); eo = o.evaluated_get(dg); me = eo.to_mesh()
    M = o.matrix_local.copy(); me.calc_loop_triangles()
    tris = []; acc = 0.0
    for t in me.loop_triangles:
        ps = [M @ me.vertices[i].co for i in t.vertices]
        ar = ((ps[1] - ps[0]).cross(ps[2] - ps[0])).length * 0.5
        if ar > 1e-10: acc += ar; tris.append((acc, ps))
    eo.to_mesh_clear()
    layv = Vector(lay).normalized(); verts = []; faces = []
    P = [(0.0, 0.10), (0.3, 0.44), (0.65, 0.5), (0.9, 0.3), (1.0, 0.02)]
    import bisect
    keys = [t[0] for t in tris]
    for _ in range(count):
        ps = tris[min(len(tris) - 1, bisect.bisect(keys, r.random() * acc))][1]
        u, v = r.random(), r.random()
        if u + v > 1: u, v = 1 - u, 1 - v
        p = ps[0] + (ps[1] - ps[0]) * u + (ps[2] - ps[0]) * v
        n = (ps[1] - ps[0]).cross(ps[2] - ps[0]).normalized()
        d = layv - n * layv.dot(n)
        if d.length < 0.15: continue
        d.normalize(); sd = n.cross(d).normalized()
        d = (d + sd * r.uniform(-0.18, 0.18)).normalized(); sd = n.cross(d).normalized()
        L = size * (1 + r.uniform(-rand, rand)); W = L * 0.52; k = len(verts)
        for x, w in P:
            c0 = p + d * (x * L) + n * (0.0012 + lift * L * math.sin(x * 2.2) * 0.55)
            verts += [c0 - sd * (w * W) - n * (w * W * 0.25), c0 + n * (0.004 * L / 0.04), c0 + sd * (w * W) - n * (w * W * 0.25)]
        for i in range(len(P) - 1):
            a = k + i * 3; faces += [(a, a + 3, a + 4, a + 1), (a + 1, a + 4, a + 5, a + 2)]
    fm = bpy.data.meshes.new(o.name + "_plumage"); fm.from_pydata([tuple(v) for v in verts], [], faces); fm.update()
    for pl in fm.polygons: pl.use_smooth = True
    fm.materials.append(mtl)
    fo = bpy.data.objects.new(o.name + "_plumage", fm); o.users_collection[0].objects.link(fo); fo.parent = o.parent
    return fo

def build(loc=(0, 0, 0), rot_z=0.0, scale=1.0, name="raven", coll_name="raven", fuzz=False):
    """Corvo pousado: pés em z=0, frente em +y. ~45 cm de altura em pé."""
    c = coll(coll_name)
    fe = mat_feather(); beak = mat("raven_beak", (0.01, 0.01, 0.012), 0.38, coat=0.25)
    eye = mat("raven_eye", (0.002, 0.0015, 0.0015), 0.02, coat=1.0)
    leg = mat("raven_leg", (0.008, 0.008, 0.008), 0.55)
    hair = bpy.data.materials.get("raven_hair") or mat("raven_hair", (0.004, 0.004, 0.006), 0.45, coat=0.2)
    root = empty(name, loc, (0, 0, rot_z), coll=c); root.scale = (scale,) * 3
    body = _skin_body(name + "_body",
        [(0, -0.15, 0.09), (0, -0.05, 0.125), (0, 0.04, 0.185), (0, 0.072, 0.25), (0, 0.08, 0.285)],
        [(0, 1), (1, 2), (2, 3), (3, 4)],
        [(0.03, 0.022), (0.072, 0.064), (0.078, 0.07), (0.058, 0.054), (0.046, 0.044)], fe, c)
    body.parent = root
    if fuzz: _fuzz(body, hair)
    neck = empty(name + "_neck", (0, 0.075, 0.27), parent=root, coll=c)
    head = _skin_body(name + "_headmesh",
        [(0, -0.01, -0.02), (0, 0.005, 0.025), (0, 0.025, 0.055), (0, 0.055, 0.058), (0, 0.075, 0.05)],
        [(0, 1), (1, 2), (2, 3), (3, 4)],
        [(0.046, 0.044), (0.044, 0.046), (0.042, 0.046), (0.034, 0.034), (0.024, 0.022)], fe, c)
    head.parent = neck
    if fuzz: _fuzz(head, hair, 1200, 0.009)
    upb = _skin_body(name + "_beak_up", [(0, 0.07, 0.06), (0, 0.11, 0.058), (0, 0.145, 0.048), (0, 0.162, 0.03)], [(0, 1), (1, 2), (2, 3)],
        [(0.019, 0.017), (0.013, 0.013), (0.007, 0.008), (0.0015, 0.0015)], beak, c)
    upb.parent = neck
    jaw = empty(name + "_jaw", (0, 0.07, 0.045), parent=neck, coll=c)
    lob = _skin_body(name + "_beak_low", [(0, 0.0, 0.0), (0, 0.04, -0.002), (0, 0.072, -0.006)], [(0, 1), (1, 2)],
        [(0.015, 0.009), (0.01, 0.006), (0.0015, 0.0015)], beak, c)
    lob.parent = jaw
    # cerdas nasais e penas da garganta (lâminas pontudas)
    _feather_fan(name + "_nasal", 5, 0.04, 30, 0.012, fe, c, neck, plane="XY", droop=-0.1).location = (0, 0.105, 0.072)
    for sx in (-1, 1):
        sphere(f"{name}_eye{sx}", 0.0082, (sx * 0.032, 0.058, 0.062), eye, seg=24, parent=neck, coll=c)
    wings = []
    for sx in (-1, 1):
        sh = empty(f"{name}_wing{sx}", (sx * 0.05, 0.055, 0.22), parent=root, coll=c)
        cov = sphere(f"{name}_wingcov{sx}", 0.06, (sx * 0.002, -0.08, -0.012), fe, scale=(0.3, 1.9, 0.85), parent=sh, coll=c)
        if fuzz: _fuzz(cov, hair, 600, 0.008)
        fan = _feather_fan(f"{name}_primaries{sx}", 10, 0.30, 34, 0.03, fe, c, sh, plane="YZ", droop=0.05)
        fan.location = (sx * 0.006, -0.07, -0.01)
        sh.rotation_euler = WING_REST(sx)
        wings.append(sh)
    tl = empty(name + "_tail", (0, -0.15, 0.09), (math.radians(-28), 0, 0), parent=root, coll=c)
    _feather_fan(name + "_tailfan", 9, 0.19, 24, 0.028, fe, c, tl, plane="XY")
    for sx in (-1, 1):
        x = sx * 0.03; V = [(x, -0.02, 0.10), (x, -0.012, 0.062), (x, 0.004, 0.013)]; E = [(0, 1), (1, 2)]; Rr = [(0.017, 0.015), (0.0075, 0.0075), (0.0058, 0.0058)]
        for a in (-30, 0, 30):
            sa, ca = math.sin(math.radians(a)), math.cos(math.radians(a)); k = len(V)
            V += [(x + sa * 0.026, 0.004 + ca * 0.026, 0.0065), (x + sa * 0.05, 0.004 + ca * 0.05, 0.0055), (x + sa * 0.064, 0.004 + ca * 0.064, 0.0005)]
            E += [(2, k), (k, k + 1), (k + 1, k + 2)]; Rr += [(0.0048, 0.0042), (0.0038, 0.0034), (0.0008, 0.0008)]
        k = len(V); V += [(x, -0.02, 0.006), (x, -0.036, 0.0005)]; E += [(2, k), (k, k + 1)]; Rr += [(0.0042, 0.0038), (0.0008, 0.0008)]
        lg = _skin_body(f"{name}_leg{sx}", V, E, Rr, leg, c); lg.parent = root
        th = sphere(f"{name}_thigh{sx}", 0.026, (x, -0.022, 0.098), fe, scale=(0.85, 1.0, 1.45), parent=root, coll=c)
        _plumage(th, fe, 120, 0.03, seed=7 + sx, lay=(0.0, -0.3, -1.0))
    _plumage(body, fe, 2400, 0.036, seed=1, lift=0.12)
    _plumage(head, fe, 900, 0.016, seed=2, lay=(0.0, -1.0, -0.1), lift=0.10)
    for w in wings:
        cv = [ch for ch in w.children if "wingcov" in ch.name][0]
        _plumage(cv, fe, 420, 0.05, seed=4, lay=(0.0, -1.0, -0.15), rand=0.35, lift=0.08)
    # penas eriçadas da garganta
    hk = _feather_fan(name + "_hackles", 7, 0.05, 70, 0.014, fe, c, neck, plane="XY", droop=0.9); hk.location = (0, 0.035, 0.012)
    return dict(root=root, neck=neck, jaw=jaw, wings=wings, tail=tl)

def rest_pose(rv):
    for sx, w in zip((-1, 1), rv["wings"]): w.rotation_euler = WING_REST(sx)

# ---------------- animação ----------------
def key(o, frame, rot=None, loc=None):
    if rot is not None: o.rotation_euler = rot; o.keyframe_insert("rotation_euler", frame=frame)
    if loc is not None: o.location = loc; o.keyframe_insert("location", frame=frame)

def snappy(o):
    """Movimentos de pássaro: segura a pose e muda rápido (interpolação constante entre chaves próximas)."""
    if o.animation_data and o.animation_data.action:
        try:
            for fc in o.animation_data.action.fcurves:
                for k in fc.keyframe_points: k.interpolation = "BEZIER"; k.easing = "EASE_IN_OUT"
        except AttributeError:
            pass

def head_moves(rv, fps, dur, seed=0, start=0.0, calm=1.0):
    """Micro movimentos de cabeça: viradas curtas e rápidas com pausas (como um corvo real)."""
    import random as R
    r = R.Random(seed); n = rv["neck"]; t = start
    key(n, int(t * fps), rot=(0, 0, 0))
    while t < dur:
        hold = r.uniform(0.6, 1.8) / calm; mv = r.uniform(0.08, 0.16)
        t += hold; key(n, int(t * fps), rot=n.rotation_euler.copy())
        t += mv
        tgt = (math.radians(r.uniform(-12, 10)), math.radians(r.uniform(-18, 18)) * calm, math.radians(r.uniform(-35, 35)) * calm)
        key(n, int(t * fps), rot=tgt)
    snappy(n)

def speak(rv, fps, at, length, opens=None):
    """Abre e fecha o bico durante a fala."""
    j = rv["jaw"]; f0 = int(at * fps)
    key(j, max(0, f0 - int(0.17 * fps)), rot=(0, 0, 0))
    k = 0; t = 0.0
    while t < length:
        a = math.radians(14 if k % 2 == 0 else 3); t += 0.11 if k % 2 == 0 else 0.13
        key(j, f0 + int(t * fps), rot=(a, 0, 0)); k += 1
    key(j, f0 + int((length + 0.12) * fps), rot=(0, 0, 0))

def spread_wings(rv, fps, at, dur=0.6, hold=None):
    f0 = int(at * fps); f1 = int((at + dur) * fps)
    for sx, w in zip((-1, 1), rv["wings"]):
        key(w, f0, rot=w.rotation_euler.copy())
        key(w, f1, rot=WING_OPEN(sx))
        if hold:
            key(w, f1 + int(hold * fps * 0.5), rot=(0, math.radians(-sx * 22), math.radians(sx * 92)))
            key(w, f1 + int(hold * fps), rot=WING_OPEN(sx))

def flap(rv, fps, at, n=6, period=0.22):
    f = int(at * fps)
    for sx, w in zip((-1, 1), rv["wings"]):
        w.rotation_euler = WING_REST(sx); w.keyframe_insert("rotation_euler", frame=max(0, f - int(0.17 * fps)))
    for k in range(n):
        for sx, w in zip((-1, 1), rv["wings"]):
            key(w, f + int(k * period * fps), rot=(0, math.radians(-sx * 55), math.radians(sx * 95)))
            key(w, f + int((k + 0.5) * period * fps), rot=(0, math.radians(sx * 25), math.radians(sx * 95)))

def breathe(rv, fps, dur):
    b = rv["root"]; s = b.scale.copy()
    for k in range(int(dur / 1.2) + 2):
        b.scale = (s.x, s.y, s.z * (1.0 + (0.012 if k % 2 else 0))); b.keyframe_insert("scale", frame=int(k * 1.2 * fps / 2))
