"""Humanos procedurais (Arthur, Eleanor) com rig hierárquico: cada membro gira em um pivô (empty).
Origem nos pés, frente em +y. Altura ~1,80 m (Arthur)."""
import bpy, bmesh, math, random
from mathutils import Vector, noise
from .core import *
from .core import _move, _bsdf, _n

def capsule(name, p0, p1, r0, r1, mtl, coll_, parent, seg=2):
    """Segmento orgânico entre dois pontos (skin modifier), em coordenadas locais do pai."""
    me = bpy.data.meshes.new(name); me.from_pydata([p0, p1], [(0, 1)], []); me.update()
    o = bpy.data.objects.new(name, me); coll_.objects.link(o); o.parent = parent
    o.modifiers.new("skin", "SKIN")
    sv = me.skin_vertices[0].data; sv[0].radius = (r0, r0); sv[1].radius = (r1, r1); sv[0].use_root = True
    sd = o.modifiers.new("sub", "SUBSURF"); sd.levels = 1; sd.render_levels = seg
    o.data.materials.append(mtl)
    for p in o.data.polygons: p.use_smooth = True
    return o

def chain(name, pts, radii, mtl, coll_, parent):
    me = bpy.data.meshes.new(name); me.from_pydata(pts, [(i, i + 1) for i in range(len(pts) - 1)], []); me.update()
    o = bpy.data.objects.new(name, me); coll_.objects.link(o); o.parent = parent
    o.modifiers.new("skin", "SKIN")
    for v, r in zip(me.skin_vertices[0].data, radii): v.radius = r
    me.skin_vertices[0].data[0].use_root = True
    sd = o.modifiers.new("sub", "SUBSURF"); sd.levels = 1; sd.render_levels = 2
    o.data.materials.append(mtl)
    for p in o.data.polygons: p.use_smooth = True
    return o

def mat_skin(name, tone=(0.62, 0.47, 0.4), pale=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    t = tuple(min(1, c + pale) for c in tone)
    m = mat(name, t, 0.48, sss=0.25); b = _bsdf(m); L = m.node_tree.links
    tc = _n(m, "ShaderNodeTexCoord")
    nz = _n(m, "ShaderNodeTexNoise", Scale=220.0, Detail=3.0); L.new(tc.outputs["Object"], nz.inputs["Vector"])
    bp = _n(m, "ShaderNodeBump", Strength=0.08, Distance=0.0005); L.new(nz.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def mat_stubble(name, tone):
    """Pele com barba por fazer: escurece a metade inferior do rosto (coordenada Z do objeto)."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, tone, 0.5, sss=0.2); b = _bsdf(m); L = m.node_tree.links
    tc = _n(m, "ShaderNodeTexCoord"); sep = _n(m, "ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sep.inputs[0])
    mr = _n(m, "ShaderNodeMapRange", **{"From Min": -0.045, "From Max": -0.005, "To Min": 1.0, "To Max": 0.0}); L.new(sep.outputs["Z"], mr.inputs[0])
    front = _n(m, "ShaderNodeMapRange", **{"From Min": -0.02, "From Max": 0.05, "To Min": 0.0, "To Max": 1.0}); L.new(sep.outputs["Y"], front.inputs[0])
    mul = _n(m, "ShaderNodeMath", operation="MULTIPLY"); L.new(mr.outputs[0], mul.inputs[0]); L.new(front.outputs[0], mul.inputs[1])
    nz = _n(m, "ShaderNodeTexNoise", Scale=900.0, Detail=2.0); L.new(tc.outputs["Object"], nz.inputs["Vector"])
    mul2 = _n(m, "ShaderNodeMath", operation="MULTIPLY"); L.new(mul.outputs[0], mul2.inputs[0]); L.new(nz.outputs["Fac"], mul2.inputs[1])
    mx = _n(m, "ShaderNodeMix", data_type="RGBA"); L.new(mul2.outputs[0], mx.inputs[0])
    mx.inputs[6].default_value = (*tone, 1); mx.inputs[7].default_value = (0.05, 0.04, 0.035, 1)
    L.new(mx.outputs[2], b.inputs["Base Color"])
    return m

def sculpt_head(name, skin, coll_, parent, gender="m", seed=1):
    """Cabeça esculpida por deslocamento de vértices de uma esfera. Origem no centro do crânio, frente em +y."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, segments=64, ring_count=48)
    o = bpy.context.object; o.name = name
    sx_, sy_, sz_ = (0.78, 0.92, 1.12) if gender == "m" else (0.74, 0.88, 1.08)
    for v in o.data.vertices:
        x, y, z = v.co.x * sx_, v.co.y * sy_, v.co.z * sz_
        fy = max(0.0, y) / 0.092      # frente do rosto
        # mandíbula e queixo: estreita embaixo, projeta o queixo
        if z < 0:
            k = min(1, -z / 0.11)
            x *= 1 - 0.32 * k ** 1.3 * (1 if gender == "m" else 1.15)
            y += 0.012 * k * fy
            if z < -0.07: y += 0.008 * fy
        # testa achatada atrás / nuca
        if y < -0.03 and z < -0.02: y *= 0.9
        # órbitas oculares
        for ex in (-0.034, 0.034):
            d = math.sqrt((x - ex) ** 2 + (z - 0.012) ** 2)
            if y > 0.04 and d < 0.026: y -= 0.011 * (1 - d / 0.026) ** 1.5
        # arcada supraciliar
        if y > 0.04 and 0.022 < z < 0.042 and abs(x) < 0.055: y += 0.009 * (1 if gender == "m" else 0.4)
        # lábios
        if abs(x) < 0.02 and -0.062 < z < -0.042 and y > 0.05: y += 0.005 * (1 - abs(z + 0.052) / 0.01) * (1 - abs(x) / 0.02)
        # queixo marcado
        if abs(x) < 0.025 and -0.1 < z < -0.075 and y > 0.03: y += 0.008 * (1 if gender == "m" else 0.5)
        # maçãs do rosto
        for cx in (-0.045, 0.045):
            d = math.sqrt((x - cx) ** 2 + (z + 0.012) ** 2)
            if y > 0.02 and d < 0.03: y += 0.006 * (1 - d / 0.03); x += math.copysign(0.004, cx) * (1 - d / 0.03)
        # bochechas fundas (cansaço)
        for cx in (-0.04, 0.04):
            d = math.sqrt((x - cx) ** 2 + (z + 0.045) ** 2)
            if y > 0.02 and d < 0.025: y -= 0.006 * (1 - d / 0.025)
        # nariz
        if abs(x) < 0.017 and -0.036 < z < 0.024 and y > 0.055:
            kz = 1 - abs(z + 0.012) / 0.024; kx = 1 - abs(x) / 0.016
            y += 0.034 * max(0, kz) ** 0.7 * kx ** 1.3 * (1 if gender == "m" else 0.7) * (0.6 + 0.4 * (1 - (z + 0.035) / 0.055))
        # boca (leve sulco)
        if abs(x) < 0.022 and -0.06 < z < -0.05 and y > 0.05: y -= 0.003
        v.co = Vector((x, y, z))
    bpy.ops.object.shade_smooth()
    o.data.materials.append(skin)
    _move(o, coll_); o.parent = parent
    # orelhas
    for sx in (-1, 1):
        e = sphere(f"{name}_ear{sx}", 0.03, (sx * 0.078, -0.005, 0.0), skin, scale=(0.3, 0.6, 1.0), seg=16, parent=o, coll=coll_)
    return o

def eyes(name, coll_, parent, iris=(0.12, 0.09, 0.06), y=0.068, z=0.012, gap=0.034):
    white = mat("eye_white", (0.75, 0.72, 0.68), 0.15, coat=1.0)
    irm = mat(f"{name}_iris", iris, 0.3, coat=1.0)
    pup = mat("eye_pupil", (0.0, 0.0, 0.0), 0.1, coat=1.0)
    lids = []; skin = parent.data.materials[0]
    for sx in (-1, 1):
        e = empty(f"{name}_eye{sx}", (sx * gap, y - 0.012, z), parent=parent, coll=coll_)
        sphere(f"{name}_ball{sx}", 0.012, (0, 0, 0), white, seg=24, parent=e, coll=coll_)
        cyl(f"{name}_iris{sx}", 0.0055, 0.002, (0, 0.0115, 0), irm, rot=(math.radians(90), 0, 0), verts=24, parent=e, coll=coll_)
        cyl(f"{name}_pupil{sx}", 0.0025, 0.002, (0, 0.0123, 0), pup, rot=(math.radians(90), 0, 0), verts=16, parent=e, coll=coll_)
        lid = empty(f"{name}_lid{sx}", (sx * gap, y - 0.012, z), parent=parent, coll=coll_)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.0128, segments=24, ring_count=12)
        cap = bpy.context.object; cap.name = f"{name}_lidmesh{sx}"
        bm = bmesh.new(); bm.from_mesh(cap.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.002], context="VERTS"); bm.to_mesh(cap.data); bm.free()
        bpy.ops.object.shade_smooth(); cap.data.materials.append(skin); _move(cap, coll_); cap.parent = lid
        lid.rotation_euler = (math.radians(-35), 0, 0)  # aberto (gire para +X ~ +55 para fechar)
        lids.append(lid)
    return lids

def build(kind="arthur", loc=(0, 0, 0), rot_z=0.0, coll_name=None):
    """Retorna dict de pivôs: root, hips(pelvis), spine, neck, head, sh_L/R, el_L/R, wr_L/R, hip_L/R, kn_L/R, lids."""
    random.seed(7 if kind == "arthur" else 9)
    c = coll(coll_name or kind)
    if kind == "arthur":
        coat = mat_noise("coat_black", (0.012, 0.012, 0.014), (0.03, 0.028, 0.032), 60, rough=0.7, bump=0.05)
        trous = mat_noise("trousers", (0.015, 0.014, 0.016), (0.03, 0.028, 0.03), 80, rough=0.8, bump=0.03)
        shirt = mat("shirt", (0.55, 0.52, 0.47), 0.6, sss=0.1)
        skin = mat_skin("skin_arthur", (0.55, 0.42, 0.36), pale=0.03)
        face = mat_stubble("face_arthur", (0.55, 0.42, 0.36))
        hair_c = (0.012, 0.009, 0.007); H = 1.0
    else:
        coat = mat_noise("dress", (0.02, 0.018, 0.022), (0.06, 0.055, 0.06), 140, rough=0.6, bump=0.3)
        trous = coat; shirt = mat_noise("lace", (0.12, 0.11, 0.1), (0.4, 0.38, 0.34), 300, rough=0.7, bump=0.4)
        skin = mat_skin("skin_eleanor", (0.66, 0.52, 0.46), pale=0.06); face = skin
        hair_c = (0.008, 0.006, 0.005); H = 0.93
    hairm = mat_noise(f"hair_{kind}", hair_c, tuple(v * 3 for v in hair_c), 400, rough=0.45, bump=0.6, stretch=(1, 1, 8))
    root = empty(kind, loc, (0, 0, rot_z), coll=c)
    hips = empty(f"{kind}_hips", (0, 0, 0.98 * H), parent=root, coll=c)
    spine = empty(f"{kind}_spine", (0, 0, 0.08 * H), parent=hips, coll=c)
    # tronco (sobrecasaca / corpete)
    chain(f"{kind}_torso", [(0, 0, -0.06), (0, 0.005, 0.1), (0, 0.0, 0.3), (0, -0.005, 0.42)],
          [(0.17, 0.11), (0.15, 0.1), (0.2, 0.12), (0.2, 0.1)] if kind == "arthur" else [(0.15, 0.1), (0.12, 0.085), (0.16, 0.1), (0.14, 0.09)], coat, c, spine)
    if kind == "arthur":
        # colarinho branco e gravata escura
        cyl(f"{kind}_collar", 0.055, 0.05, (0, 0.012, 0.47), shirt, parent=spine, coll=c)
        box(f"{kind}_cravat", (0.07, 0.02, 0.09), (0, 0.075, 0.4), mat("cravat", (0.01, 0.01, 0.012), 0.5), parent=spine, coll=c, bevel=0.01)
        box(f"{kind}_shirtfront", (0.08, 0.01, 0.16), (0, 0.098, 0.3), shirt, parent=spine, coll=c, bevel=0.004)
        # aba da sobrecasaca (saia até o joelho)
        for sx in (-1, 1):
            t = chain(f"{kind}_coattail{sx}", [(sx * 0.07, -0.06, 0.0), (sx * 0.09, -0.09, -0.28), (sx * 0.1, -0.1, -0.5)], [(0.1, 0.03), (0.11, 0.02), (0.1, 0.012)], coat, c, hips)
        chain(f"{kind}_coatfront", [(0, 0.04, 0.02), (0, 0.06, -0.12)], [(0.17, 0.08), (0.15, 0.05)], coat, c, hips)
    else:
        cyl(f"{kind}_collar", 0.05, 0.08, (0, 0.0, 0.46), shirt, parent=spine, coll=c)
        sk = cyl(f"{kind}_skirt", 0.48, 0.98, (0, 0, -0.5), coat, r2=0.16, verts=48, parent=hips, coll=c)
        wv = sk.modifiers.new("folds", "WAVE"); wv.use_normal = True; wv.height = 0.015; wv.width = 0.09; wv.speed = 0
    neck = empty(f"{kind}_neck", (0, 0.0, 0.47), parent=spine, coll=c)
    capsule(f"{kind}_neckm", (0, 0, -0.03), (0, 0.01, 0.08), 0.052 if kind == "arthur" else 0.042, 0.048 if kind == "arthur" else 0.038, skin, c, neck)
    head_p = empty(f"{kind}_headp", (0, 0.02, 0.17), parent=neck, coll=c)
    head = sculpt_head(f"{kind}_head", face, c, head_p, "m" if kind == "arthur" else "f")
    lids = eyes(kind, c, head, iris=(0.1, 0.08, 0.06) if kind == "arthur" else (0.06, 0.08, 0.1))
    # cabelo: casca deslocada por ruído (mechas), cobre o crânio
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.104, segments=48, ring_count=32)
    hr = bpy.context.object; hr.name = f"{kind}_hair"
    for v in hr.data.vertices:
        x, y, z = v.co.x * 0.82, v.co.y * 0.96, v.co.z * 1.13
        keep = (z > 0.02 - (0.07 if y < 0 else 0)) or (kind == "eleanor")
        if kind == "eleanor" and y > 0.05 and z < 0.06: keep = False
        if not keep: z = max(z, 0.0); y = min(y, 0.0) if z <= 0 else y
        n = noise.noise(Vector((x * 35, y * 35, z * 22))) * 0.012 + noise.noise(Vector((x * 90, y * 90, z * 90))) * 0.004
        bulk = 1.08 if kind == 'arthur' else 1.02
        v.co = Vector((x * bulk * (1 + n * 7), y * bulk * (1 + n * 7), z * bulk + abs(n) * 1.5))
    bm = bmesh.new(); bm.from_mesh(hr.data)
    cut = [v for v in bm.verts if (v.co.z < 0.015 and v.co.y > -0.02 and kind == "arthur") or (kind == "eleanor" and v.co.y > 0.055 and v.co.z < 0.07)]
    bmesh.ops.delete(bm, geom=cut, context="VERTS"); bm.to_mesh(hr.data); bm.free()
    bpy.ops.object.shade_smooth(); hr.data.materials.append(hairm); _move(hr, c); hr.parent = head
    rnd = random.Random(11 if kind == "arthur" else 12)
    for k in range(70 if kind == "arthur" else 30):
        th = rnd.uniform(0, 2 * math.pi); ph = rnd.uniform(0.15, 1.35 if kind == "arthur" else 0.9)
        dirv = Vector((math.sin(ph) * math.cos(th) * 0.82, math.sin(ph) * math.sin(th) * 0.95, math.cos(ph) * 1.1))
        if kind == "arthur" and dirv.y > 0.06 and dirv.z < 0.05: continue
        base = dirv * 0.1
        out = (dirv * 0.35 + Vector((rnd.uniform(-0.3, 0.3), rnd.uniform(-0.6, -0.1), -0.9))).normalized() * rnd.uniform(0.025, 0.045)
        chain(f"{kind}_lock{k}", [tuple(base * 0.9), tuple(base + out * 0.5), tuple(base + out)], [(0.014, 0.01), (0.01, 0.007), (0.002, 0.002)], hairm, c, head)
    if kind == "eleanor":
        # cabelo longo caindo pelas costas e cobrindo o rosto de lado
        chain(f"{kind}_hairlong", [(0, -0.06, 0.03), (0, -0.09, -0.15), (0, -0.07, -0.42)], [(0.09, 0.06), (0.1, 0.05), (0.08, 0.03)], hairm, c, head)
    # braços
    piv = {}
    for side, sx in (("L", -1), ("R", 1)):
        sh = empty(f"{kind}_sh{side}", (sx * (0.2 if kind == "arthur" else 0.17), 0, 0.38), parent=spine, coll=c)
        capsule(f"{kind}_upper{side}", (0, 0, 0.04), (0, 0, -0.31 * H), 0.068, 0.056, coat, c, sh)
        el = empty(f"{kind}_el{side}", (0, 0, -0.29 * H), parent=sh, coll=c)
        capsule(f"{kind}_fore{side}", (0, 0, 0.03), (0, 0, -0.25 * H), 0.056, 0.046, coat, c, el)
        cyl(f"{kind}_cuff{side}", 0.036, 0.03, (0, 0, -0.245 * H), shirt, parent=el, coll=c)
        wr = empty(f"{kind}_wr{side}", (0, 0, -0.26 * H), parent=el, coll=c)
        chain(f"{kind}_palm{side}", [(0, 0.0, 0.0), (0, 0.004, -0.045), (0, 0.006, -0.085)], [(0.024, 0.014), (0.034, 0.013), (0.036, 0.011)], skin, c, wr)
        for k in range(4):
            fy = 0.024 - k * 0.016; ln = [0.042, 0.048, 0.045, 0.034][k]
            curl = 0.25 if kind == "arthur" else 0.35
            p1 = (0, fy, -0.09); p2 = (0, fy + 0.004, -0.09 - ln * 0.5); p3 = (0, fy + 0.004 + ln * curl * 0.3, -0.09 - ln * 0.85); p4 = (0, fy + ln * curl * 0.6, -0.09 - ln * 1.05)
            chain(f"{kind}_finger{side}{k}", [p1, p2, p3, p4], [(0.0085, 0.0075), (0.0078, 0.0068), (0.007, 0.006), (0.0055, 0.005)], skin, c, wr)
        chain(f"{kind}_thumb{side}", [(sx * -0.008, 0.026, -0.02), (sx * -0.022, 0.045, -0.05), (sx * -0.026, 0.058, -0.08)], [(0.012, 0.01), (0.009, 0.008), (0.0065, 0.006)], skin, c, wr)
        piv[f"sh{side}"], piv[f"el{side}"], piv[f"wr{side}"] = sh, el, wr
        # pernas
        hp_ = empty(f"{kind}_hip{side}", (sx * 0.1, 0, -0.02), parent=hips, coll=c)
        capsule(f"{kind}_thigh{side}", (0, 0, 0.05), (0, 0, -0.46 * H), 0.095, 0.07, trous, c, hp_)
        kn = empty(f"{kind}_kn{side}", (0, 0, -0.44 * H), parent=hp_, coll=c)
        capsule(f"{kind}_shin{side}", (0, 0, 0.04), (0, 0, -0.43 * H), 0.068, 0.055, trous, c, kn)
        box(f"{kind}_shoe{side}", (0.09, 0.26, 0.07), (0, 0.06, -0.47 * H), mat("shoe", (0.008, 0.008, 0.008), 0.25, coat=0.6), bevel=0.02, parent=kn, coll=c)
        piv[f"hip{side}"], piv[f"kn{side}"] = hp_, kn
    return dict(root=root, hips=hips, spine=spine, neck=neck, head=head_p, lids=lids, **piv)

# ---------------- poses (graus) ----------------
R = math.radians
def pose(rig, **kw):
    """Define rotações (graus) dos pivôs: pose(rig, spine=(x,y,z), shR=(...), ...)."""
    for k, v in kw.items():
        if k == "loc": rig["root"].location = v; continue
        if k == "lids":
            for l in rig["lids"]: l.rotation_euler = (R(v), 0, 0)
            continue
        rig[k].rotation_euler = tuple(R(a) for a in v)

def key_pose(rig, frame, **kw):
    pose(rig, **kw)
    for k in kw:
        if k == "loc": rig["root"].keyframe_insert("location", frame=frame); continue
        if k == "lids":
            for l in rig["lids"]: l.keyframe_insert("rotation_euler", frame=frame)
            continue
        rig[k].keyframe_insert("rotation_euler", frame=frame)

SIT = dict(hipL=(-88, 0, -4), hipR=(-88, 0, 4), knL=(85, 0, 0), knR=(85, 0, 0))
STAND = dict(hipL=(0, 0, 0), hipR=(0, 0, 0), knL=(0, 0, 0), knR=(0, 0, 0))
ARMS_DOWN = dict(shL=(0, 0, 0), shR=(0, 0, 0), elL=(0, 0, 0), elR=(0, 0, 0), wrL=(0, 0, 0), wrR=(0, 0, 0))
WRITE = dict(spine=(18, 0, 0), neck=(18, 0, 0), shR=(-45, 0, 12), elR=(-70, 0, 0), wrR=(10, 0, 0), shL=(-38, 0, -15), elL=(-75, 0, 25), wrL=(0, 0, 0))
