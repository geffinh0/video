"""Corpo humano a partir dos DADOS abertos (CC0) do MakeHuman/MPFB2: malha base hm08, alvos de forma,
esqueleto e pesos. Nenhum código do MPFB é executado: só lemos base.obj, *.target.gz e os JSON do rig.
Convenção: pés em z=0, frente em -y (a das poses), lado R em +x. Unidades em metros."""
import bpy, gzip, json, os
from mathutils import Vector, Matrix
from .core import coll

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "vendor/mpfb2/src/mpfb/data")
PARTS = ("body", "helper-tights", "helper-skirt", "helper-hair", "helper-l-eye", "helper-r-eye")
_cache = {}


def _obj():
    if "obj" in _cache: return _cache["obj"]
    V = []; F = {p: [] for p in PARTS}; g = None
    for ln in open(f"{DATA}/3dobjs/base.obj"):
        if ln.startswith("v "):
            a = ln.split(); V.append((float(a[1]), float(a[2]), float(a[3])))
        elif ln.startswith("g "): g = ln.split()[1]
        elif ln.startswith("f ") and g in F:
            F[g].append([int(t.split("/")[0]) - 1 for t in ln.split()[1:]])
    _cache["obj"] = (V, F); return V, F


def _target(name):
    out = []
    with gzip.open(f"{DATA}/targets/{name}.target.gz", "rt") as f:
        for ln in f:
            a = ln.split()
            if len(a) == 4 and not ln.startswith("#"): out.append((int(a[0]), float(a[1]), float(a[2]), float(a[3])))
    return out


def body(name, targets, height, coll_):
    """Cria malha + armature. Retorna (obj, arm, joints) com joints = {bone: (head, tail)} em metros."""
    V0, F = _obj(); V = [list(v) for v in V0]
    for tn, w in targets:
        for i, dx, dy, dz in _target(tn):
            V[i][0] += dx * w; V[i][1] += dy * w; V[i][2] += dz * w
    ymin = min(v[1] for v in V[:13380]); ymax = max(v[1] for v in V[:13380]); s = height / (ymax - ymin)
    P = [Vector((-v[0] * s, -v[2] * s, (v[1] - ymin) * s)) for v in V]     # frente -y (convenção das poses), espelhado em x: .R em +x
    groups = json.load(open(f"{DATA}/mesh_metadata/basemesh_vertex_groups.json"))
    rig = json.load(open(f"{DATA}/rigs/standard/rig.default.json"))
    wts = json.load(open(f"{DATA}/rigs/standard/weights.default.json"))["weights"]

    def pos(d):
        st = d["strategy"]
        if st == "CUBE":
            idx = [i for a, b in groups[d["cube_name"]] for i in range(a, b + 1)]
        elif st == "VERTEX": idx = [d["vertex_index"]]
        else: idx = d["vertex_indices"]
        c = Vector((0, 0, 0))
        for i in idx: c += P[i]
        return c / len(idx)
    joints = {b: (pos(d["head"]), pos(d["tail"])) for b, d in rig.items()}

    me = bpy.data.meshes.new(name); faces = []; mats = []
    for k, p in enumerate(PARTS):
        faces += [f[::-1] for f in F[p]]; mats += [k] * len(F[p])
    me.from_pydata([tuple(p) for p in P], [], faces); me.update()
    for pl, m in zip(me.polygons, mats): pl.material_index = m; pl.use_smooth = True
    o = bpy.data.objects.new(name, me); coll_.objects.link(o)
    for b, lst in wts.items():
        vg = o.vertex_groups.new(name=b)
        for i, w in lst: vg.add([i], w, "REPLACE")
    for p in PARTS:   # grupos por parte (para máscaras)
        vg = o.vertex_groups.new(name="part:" + p)
        vg.add([i for a, b in groups[p] for i in range(a, b + 1)], 1.0, "REPLACE")

    ad = bpy.data.armatures.new(name + "_arm"); arm = bpy.data.objects.new(name + "_arm", ad); coll_.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for b in rig:
        eb = ad.edit_bones.new(b); h, t = joints[b]
        eb.head = h; eb.tail = t if (t - h).length > 1e-4 else h + Vector((0, 0, 0.01))
    for b, d in rig.items():
        if d.get("parent"): ad.edit_bones[b].parent = ad.edit_bones[d["parent"]]
    bpy.ops.object.mode_set(mode="OBJECT")
    md = o.modifiers.new("arm", "ARMATURE"); md.object = arm
    arm.hide_render = True
    return o, arm, joints


def drive(arm, bone, ctl, rest_head, quat=None, coll_=None):
    """Faz o osso seguir o pivô `ctl` rigidamente. Cria um empty-alvo filho de `ctl` cuja matriz de mundo é a
    matriz desejada do osso; o osso copia essa matriz (COPY_TRANSFORMS). `quat`: rotação extra em torno da
    cabeça do osso aplicada na pose neutra (ex.: baixar os braços da pose em A)."""
    from mathutils import Quaternion
    rest = arm.data.bones[bone].matrix_local.copy()
    q = (quat or Quaternion()).to_matrix().to_4x4()
    loc = q @ Matrix.Translation(-Vector(rest_head)) @ rest
    t = bpy.data.objects.new(f"{ctl.name}_tgt_{bone}", None); (coll_ or ctl.users_collection[0]).objects.link(t)
    t.empty_display_size = 0.01; t.parent = ctl; t.rotation_mode = "QUATERNION"
    t.location = loc.to_translation(); t.rotation_quaternion = loc.to_quaternion()
    c = arm.pose.bones[bone].constraints.new("COPY_TRANSFORMS"); c.target = t
    return t
