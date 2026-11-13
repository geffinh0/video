"""Definição dos planos (cenário, câmera, personagens, animação) e render.
Uso: python3 blender/shots.py <shot> <plate|layer|preview> [samples]
- plate:   fundo estático, alta qualidade, sem personagens animados  -> renders/scenes/<id>/plate.png
- layer:   personagens/objetos animados, fundo transparente, 30 fps, cenário como holdout -> renders/scenes/<id>/layer/####.png
- preview: tudo junto, baixa resolução, no meio do plano -> renders/preview/<id>.png"""
import sys, os, math, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from pouso.core import *
from pouso import study, raven, human, exterior, corridor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = f"{ROOT}/assets/textures"
SHOTS = {s["id"]: s for s in json.load(open(f"{ROOT}/roteiro/shots.json"))["shots"]}
VO = json.load(open(f"{ROOT}/assets/audio/voices/durations.json"))
FPS = 30
R = math.radians

def line_at(shot, lid):
    for l, t in SHOTS[shot].get("lines", []):
        if l == lid: return t, VO[l]
    raise KeyError(lid)

# ---------------- ambientes ----------------
def ext(fog=0.015, mansion=True, forest_n=70, moon=2.2, exposure=0.8):
    c = coll("ext")
    exterior.ground(c); exterior.night(sky=(0.012, 0.022, 0.035), moon_energy=moon, moon_dir=(R(70), 0, R(170)))
    win = None
    if mansion: _, win = exterior.mansion(c, (0, 30, 0))
    exterior.forest(c, (0, 10), 35, forest_n, clear=((0, 22), 14))
    exterior.scatter(c, (0, -16))
    world_fog(fog, (0.28, 0.36, 0.45), 0.5)
    bpy.context.scene.view_settings.exposure = exposure
    return c, win

def room(exposure=1.2, dawn=False, window_open=False):
    A = study.build(TEX)
    bpy.context.scene.view_settings.exposure = exposure
    if dawn:
        for fl, L in A["candles"]: fl.hide_render = True; L.hide_render = True
        m = bpy.data.objects["moon"]; m.data.energy = 2200; m.data.color = kelvin(7500)
        world_color((0.03, 0.04, 0.05), 1.0)
        w = A["window"]
        for nm, off, e, sz in [("dawn_fill", (0.5, 0, 0), 140, 1.6), ("dawn_bounce", (3.0, 0, 1.2), 35, 3.0)]:
            lo = light(nm, "AREA", (w.x + off[0], w.y + off[1], w.z + off[2]), e, kelvin(7800), size=sz, rot=(0, R(-90) if nm == "dawn_fill" else 0, 0))
            lo.visible_camera = False; lo.visible_glossy = nm != "dawn_fill"
    if window_open:
        bpy.data.objects["window_glass"].hide_render = True
    bpy.context.view_layer.update()
    return A

def hold_collections(names):
    """Marca coleções de cenário como holdout (para camadas)."""
    for lc in bpy.context.view_layer.layer_collection.children:
        if lc.name in names: lc.holdout = True

def hide_collections(names):
    for lc in bpy.context.view_layer.layer_collection.children:
        if lc.name in names: lc.exclude = True

def to_layer(objs, name="layerobjs"):
    """Move objetos (e filhos) do cenário para uma coleção animada."""
    c = coll(name)
    def mv(o):
        for oc in list(o.users_collection): oc.objects.unlink(o)
        c.objects.link(o)
        for ch in o.children: mv(ch)
    for o in objs: mv(o)
    return c

def arthur_seated(loc=(0, -0.62, 0), writing=True):
    rig = human.build("arthur", loc)
    human.pose(rig, **human.SIT, **(human.WRITE if writing else {}))
    rig["root"].location = (loc[0], loc[1], loc[2] - 0.47)
    return rig

def writing_anim(rig, dur, start=0):
    """Mão escrevendo: pequenos traços do antebraço direito e leve balanço da cabeça."""
    import random as Rn; r = Rn.Random(3); t = 0.0
    while t < dur:
        f = int((start + t) * FPS)
        human.key_pose(rig, f, elR=(-70 + r.uniform(-6, 6), 0, r.uniform(-8, 8)), wrR=(10 + r.uniform(-8, 8), 0, 0), neck=(18 + r.uniform(-2, 2), 0, r.uniform(-2, 2)))
        t += r.uniform(0.25, 0.5)

# ---------------- planos ----------------
def S(id_, cam, fn=None, layer=None, **kw):
    return dict(id=id_, cam=cam, fn=fn, layer=layer, **kw)

def shot_build(sid, mode):
    sh = SHOTS[sid]; dur = sh["dur"]; L = None; held = []
    if sid == "s02":
        ext(fog=0.02, mansion=False, forest_n=110)
        camera("cam", (0, -25, 3.0), (2, 10, 5.5), lens=24)
    elif sid == "s03":
        ext()
        camera("cam", (2, -12, 3.5), (0, 30, 7.5), lens=32)
    elif sid in ("s04",):
        c, _ = ext(fog=0.018)
        perch = exterior.statue(c, (0.2, -14, 0))
        rv = raven.build(perch, R(160), name="raven"); L = ["raven"]; held = ["ext"]
        raven.head_moves(rv, FPS, dur, seed=4)
        camera("cam", (1.4, -16.4, 2.75), perch + Vector((0, 0, 0.18)), lens=60, fstop=2.0)
    elif sid == "s05":
        _, win = ext(fog=0.012)
        camera("cam", (-4, 8, 4.5), win, lens=70)
    elif sid in ("s06", "s07"):
        A = room(1.3); rig = arthur_seated(); L = ["arthur"]; held = ["study"]
        writing_anim(rig, dur)
        if sid == "s06": camera("cam", (2.5, -2.4, 2.1), (-0.6, 0.5, 1.0), lens=22)
        else: camera("cam", (-0.62, -1.55, 1.42), (0.05, 0.05, 0.86), lens=40, fstop=2.8)
    elif sid == "s08":
        A = room(1.6)
        light("photo_l", "POINT", (-0.1, 0.0, 1.05), 4, kelvin(1900), size=0.05)
        pf = A["photo_frame"]; t = pf.matrix_world.translation + Vector((0, 0, 0.11))
        camera("cam", tuple(t + Vector((0.2, -0.55, 0.06))), t, lens=60, fstop=2.8)
    elif sid == "s09":
        A = room(1.3); rig = arthur_seated(writing=False); L = ["arthur"]; held = ["study"]
        human.pose(rig, spine=(8, 0, 0), neck=(5, 0, 0), shR=(-35, 0, 10), elR=(-80, 0, 0), shL=(-30, 0, -10), elL=(-80, 0, 20))
        human.key_pose(rig, 0, neck=(5, 0, 0)); human.key_pose(rig, int(5.5 * FPS), neck=(5, 0, 0)); human.key_pose(rig, int(7.0 * FPS), neck=(2, 0, -25)); human.key_pose(rig, int(dur * FPS), neck=(2, 0, -25))
        human.key_pose(rig, int(7.0 * FPS), lids=-35); human.key_pose(rig, int(7.3 * FPS), lids=20); human.key_pose(rig, int(7.6 * FPS), lids=-35)
        camera("cam", (0.42, -1.42, 1.36), (-0.35, 0.38, 0.95), lens=45, fstop=2.0)
    elif sid in ("s10", "s32"):
        A = room(1.4, dawn=(sid == "s32"))
        if sid == "s32": bpy.data.materials["clock_face"].node_tree.nodes["Image Texture"].image = bpy.data.images.load(f"{TEX}/clock_face_317.png")
        ck = A["clock"]; f = A["clock_face"].matrix_world.translation
        if sid == "s10":
            pv = A["pendulum"]; L = ["layerobjs"]; held = ["study"]; to_layer([pv])
            for k in range(int(dur) + 2):
                pv.rotation_euler = (0, R(6 if k % 2 else -6), 0); pv.keyframe_insert("rotation_euler", frame=k * FPS)
        light("clock_fill", "POINT", tuple(f + Vector((0.4, -0.6, 0.2))), 3, kelvin(1900), size=0.1)
        camera("cam", tuple(f + Vector((0.1, -0.85, 0.0))), tuple(f), lens=50, fstop=2.8)
    elif sid in ("s10b", "s12", "s13", "s14", "s11"):
        A = room(1.3); so = A["sill_out"]
        win = A["window"]
        if sid in ("s11", "s12", "s13", "s14"):
            rv = raven.build(tuple(so + Vector((0, 0, 0.02))), R(-90), name="raven"); L = ["raven"]; held = ["study"]
            raven.head_moves(rv, FPS, dur, seed={"s11": 1, "s12": 2, "s13": 3, "s14": 5}[sid], calm=0.6 if sid == "s13" else 1.0)
        if sid == "s10b":
            camera("cam", (-1.2, -0.9, 1.5), (-3, 0.5, 1.6), lens=35)
        elif sid == "s11":
            rig = arthur_seated(writing=False); L = ["raven", "arthur"]
            human.key_pose(rig, 0, neck=(15, 0, 0), spine=(15, 0, 0)); human.key_pose(rig, int(2 * FPS), neck=(15, 0, 0), spine=(15, 0, 0))
            human.key_pose(rig, int(6 * FPS), neck=(0, 0, 55), spine=(4, 0, 20)); human.key_pose(rig, int(dur * FPS), neck=(0, 0, 58), spine=(4, 0, 22))
            camera("cam", (0.55, -1.6, 1.45), (-2.8, 0.5, 1.35), lens=35, fstop=2.8)
        elif sid == "s12":
            camera("cam", (-2.15, -0.35, 1.12), tuple(so + Vector((0, 0, 0.24))), lens=50, fstop=2.8)
        elif sid == "s13":
            t0, d = line_at("s13", "C1"); raven.speak(rv, FPS, t0, d)
            for k, (t, a) in enumerate([(3.0, 0), (3.4, -28), (8.5, -28), (9.0, -10)]):
                n = rv["neck"]; n.rotation_euler = (0, R(a), 0); n.keyframe_insert("rotation_euler", frame=int(t * FPS))
            bpy.context.view_layer.update(); bpy.context.scene.frame_set(0)
            eye = rv["neck"].matrix_world @ Vector((0.032, 0.058, 0.062))
            camera("cam", tuple(eye + Vector((0.32, -0.12, 0.02))), tuple(eye), lens=100, fstop=4.0)
        elif sid == "s14":
            t0, d = line_at("s14", "C2"); raven.speak(rv, FPS, t0, d)
            r0 = rv["root"]; r0.keyframe_insert("location", frame=int(7.1 * FPS))
            r0.location = (r0.location.x, r0.location.y, r0.location.z - 50); r0.keyframe_insert("location", frame=int(7.2 * FPS))
            rig = human.build("arthur", (-1.5, 0.4, 0), R(90)); L = ["raven", "arthur"]
            human.key_pose(rig, 0, loc=(-1.5, 0.4, 0), spine=(0, 0, 0), neck=(0, 0, 0))
            human.key_pose(rig, int(0.6 * FPS), loc=(-1.5, 0.4, 0), spine=(-6, 0, 0), neck=(-5, 0, 0))
            human.key_pose(rig, int(1.4 * FPS), loc=(-1.0, 0.4, 0), spine=(-10, 0, 0), neck=(-8, 0, 0))
            human.key_pose(rig, int(dur * FPS), loc=(-0.9, 0.4, 0), spine=(-8, 0, 0), neck=(-6, 0, 0))
            camera("cam", (1.4, 1.6, 1.5), (-2.6, 0.4, 1.4), lens=30)
    elif sid == "s15":
        A = room(1.4); dr = A["drawer"]; to_layer([dr]); L = ["layerobjs"]; held = ["study"]
        y0 = dr.location.y
        for t, dy in [(0, 0), (4.0, 0), (4.15, -0.03), (4.6, -0.03), (4.8, -0.06), (5.5, -0.06), (5.7, -0.28), (dur, -0.3)]:
            dr.location.y = y0 + dy; dr.keyframe_insert("location", frame=int(t * FPS))
        camera("cam", (0.5, -1.25, 1.05), (0, -0.3, 0.72), lens=40, fstop=2.8)
    elif sid in ("s16", "s17", "s31"):
        A = room(1.3, dawn=(sid == "s31"))
        tex = {"s16": "letter_closed", "s17": "letter_open", "s31": "letter_final"}[sid]
        size = (0.2, 0.125) if sid == "s16" else (0.22, 0.3)
        lt = plane("letter", size, (0.05, -0.02, 0.812), mat_image(tex, f"{TEX}/{tex}.png", 0.75), rot=(0, 0, R(-6)))
        if sid == "s17":
            lt.location.z = 1.0; lt.rotation_euler = (R(55), 0, R(-4)); to_layer([lt]); L = ["layerobjs"]; held = ["study"]
            import random as Rn; r = Rn.Random(2)
            for k in range(int(dur * FPS)):
                lt.location = (0.05 + r.uniform(-0.002, 0.002), -0.12 + r.uniform(-0.002, 0.002), 1.0 + r.uniform(-0.002, 0.002)); lt.keyframe_insert("location", frame=k)
            camera("cam", (0.06, -0.62, 1.12), (0.05, -0.1, 1.0), lens=50, fstop=2.0)
        elif sid == "s31":
            camera("cam", (0.10, -0.40, 1.02), (0.03, -0.12, 0.81), lens=50, fstop=2.8)
        else:
            camera("cam", (0.12, -0.38, 1.12), (0.05, -0.02, 0.81), lens=50, fstop=2.8)
    elif sid == "s17b":
        A = room(1.3); rig = arthur_seated(writing=False); L = ["arthur"]; held = ["study"]
        human.pose(rig, spine=(5, 0, 12), shR=(-60, 0, 10), elR=(-50, 0, 0), shL=(-60, 0, -10), elL=(-50, 0, 0))
        for t, a in [(0, 0), (1.5, 0), (2.5, 45), (8.5, 45), (9.5, 0), (dur, 0)]:
            human.key_pose(rig, int(t * FPS), neck=(5 if a == 0 else 0, 0, a))
        camera("cam", (1.6, -1.4, 1.3), (-1.5, 0.0, 1.3), lens=35, fstop=4)
    elif sid == "s18":
        A = room(1.2); hinge = A["door"]
        lt = plane("letter", (0.22, 0.3), (0.3, -0.5, 0.95), mat_image("letter_open", f"{TEX}/letter_open.png", 0.75), rot=(R(70), 0, 0))
        to_layer([lt, hinge]); L = ["layerobjs"]; held = ["study"]
        for t, loc, rot in [(0.6, (0.3, -0.5, 0.95), (70, 0, 0)), (0.9, (0.35, -0.55, 0.6), (30, 20, 40)), (1.2, (0.4, -0.62, 0.25), (-10, 10, 80)), (1.5, (0.42, -0.66, 0.012), (0, 0, 95))]:
            lt.location = loc; lt.rotation_euler = tuple(R(a) for a in rot); lt.keyframe_insert("location", frame=int(t * FPS)); lt.keyframe_insert("rotation_euler", frame=int(t * FPS))
        for t, a in [(0, -18), (12.5, -18), (13.6, -27), (dur, -27)]:
            hinge.rotation_euler = (0, 0, R(a)); hinge.keyframe_insert("rotation_euler", frame=int(t * FPS))
        camera("cam", (-0.6, -2.2, 1.25), (1.6, 2.6, 1.15), lens=35, fstop=5.6)
    elif sid in ("s19", "s20", "s23"):
        A = corridor.build(); bpy.context.scene.view_settings.exposure = 1.5; bpy.context.view_layer.update()
        if sid == "s19":
            rig = human.build("arthur", (0, 1.0, 0), 0); L = ["arthur"]; held = ["corridor"]
            step = 0.62; n = int((dur - 1) / 0.6)
            for k in range(n + 1):
                f = int((0.5 + k * 0.6) * FPS); y = 1.0 + k * step * 0.75; sw = 22 if k % 2 else -22
                human.key_pose(rig, f, loc=(0, y, 0.02 * (k % 2)), hipL=(sw, 0, 0), hipR=(-sw, 0, 0), knL=(25 if sw < 0 else 5, 0, 0), knR=(25 if sw > 0 else 5, 0, 0), shL=(-sw * 0.6, 0, 0), shR=(sw * 0.6, 0, 0))
            camera("cam", (0.25, -0.3, 1.65), (0, 8, 1.4), lens=35)
        elif sid == "s20":
            g = A["eleanor_portrait"]; t = g.matrix_world.translation.copy()
            light("portrait_l", "POINT", (0.3, 6.9, 2.3), 10, kelvin(1800), size=0.05)
            camera("cam", (0.1, 6.55, 1.85), (1.1, 7.5, 1.95), lens=45, fstop=2.8)
        else:
            rig = human.build("arthur", (0, 11.0, 0), 0); L = ["arthur"]; held = ["corridor"]
            human.key_pose(rig, 0, neck=(0, 0, 0)); human.key_pose(rig, int(8 * FPS), neck=(18, 0, 0)); human.key_pose(rig, int(dur * FPS), neck=(22, 0, 3))
            human.key_pose(rig, 0, shR=(0, 0, 0)); human.key_pose(rig, int(10 * FPS), shR=(-55, 0, 8), elR=(-20, 0, 0)); human.key_pose(rig, int(dur * FPS), shR=(-60, 0, 8), elR=(-20, 0, 0))
            camera("cam", (0.5, 8.6, 1.55), (0, 12, 1.4), lens=40, fstop=2.8)
    elif sid == "s21":
        A = corridor.build(warm=True); bpy.context.scene.view_settings.exposure = 1.8
        rig = human.build("eleanor", (0, 11.25, 0), 0); L = ["eleanor"]; held = ["corridor"]
        for t, a in [(0, 0), (2.6, 0), (3.0, -105), (3.15, -112), (3.4, -105), (3.6, -112), (3.85, -105), (4.05, -112), (4.4, -100), (dur, -100)]:
            human.key_pose(rig, int(t * FPS), shR=(a, 0, -8), elR=(-35 if a else 0, 0, 0))
        light("door_glow", "AREA", (0, 12.3, 1.2), 30, kelvin(2000), size=0.8).rotation_euler = (R(-90), 0, 0)
        camera("cam", (-0.5, 8.4, 1.45), (0.05, 11.6, 1.45), lens=45, fstop=2.0)
    elif sid in ("s24", "s25", "s26", "s29"):
        A = room(1.3, window_open=True); held = ["study"]
        chair_top = Vector((0, 1.33, 1.33))
        if sid == "s24":
            L = ["layerobjs"]; cs = [bpy.data.objects["curtain-1"], bpy.data.objects["curtain1"]]; to_layer(cs)
            for cu in cs:
                w = cu.modifiers["folds"]; w.speed = 0.25; w.height = 0.08
            camera("cam", (2.3, -2.2, 1.7), (-1.0, 0.6, 1.2), lens=26)
        else:
            rv = raven.build(tuple(chair_top), R(180), name="raven"); L = ["raven"]
            raven.head_moves(rv, FPS, dur, seed={"s25": 7, "s26": 8, "s29": 9}[sid], calm=0.5)
            if sid == "s25": camera("cam", (0.3, -0.9, 1.45), tuple(chair_top + Vector((0, 0, 0.2))), lens=45, fstop=2.8)
            elif sid == "s26":
                t0, d = line_at("s26", "C3"); raven.speak(rv, FPS, t0, d)
                camera("cam", (0.18, 0.75, 1.62), tuple(chair_top + Vector((0, -0.12, 0.33))), lens=100, fstop=2.8)
            else:
                t0, d = line_at("s29", "C4"); raven.speak(rv, FPS, t0, d); raven.spread_wings(rv, FPS, 2.0, 0.5, hold=4.0)
                camera("cam", (0.0, -1.1, 1.5), tuple(chair_top + Vector((0, 0, 0.25))), lens=35, fstop=4)
    elif sid == "s27":
        A = room(1.3); rig = arthur_seated(writing=False); L = ["arthur"]; held = ["study"]
        human.pose(rig, spine=(5, 0, 0), shR=(-35, 0, 10), elR=(-80, 0, 0), shL=(-30, 0, -10), elL=(-80, 0, 20))
        for t, lid, nk in [(0, -35, 0), (8.5, -35, 0), (9.2, 25, -4), (10.2, 25, -6), (11, -20, 8), (dur, -20, -8)]:
            human.key_pose(rig, int(t * FPS), lids=lid, neck=(nk, 0, 0))
        camera("cam", (0.55, -0.25, 1.3), (-0.3, -0.62, 1.25), lens=85, fstop=2.0)
    elif sid == "s28":
        A = room(1.4); rig = arthur_seated(writing=False)
        human.pose(rig, spine=(15, 0, 0), shR=(-50, 0, 10), elR=(-60, 0, 0), wrR=(20, 0, 0)); bpy.context.view_layer.update()
        wr = rig["wrR"].matrix_world.translation.copy()
        tor = bpy.ops.mesh.primitive_torus_add(major_radius=0.034, minor_radius=0.004, location=wr); t = bpy.context.object
        t.data.materials.append(mat("wound", (0.25, 0.02, 0.02), 0.6)); t.parent = rig["wrR"]; t.matrix_parent_inverse = rig["wrR"].matrix_world.inverted()
        light("wrist_key", "POINT", tuple(wr + Vector((0.15, -0.25, 0.25))), 1.5, kelvin(2200), size=0.15).visible_camera = False
        camera("cam", tuple(wr + Vector((0.25, -0.25, 0.12))), tuple(wr), lens=85, fstop=2.0)
    elif sid == "s30":
        A = room(1.0, dawn=True); ch = A["arthur_chair"]; ch.location = (0.25, -1.05, 0); ch.rotation_euler = (0, 0, R(18))
        camera("cam", (2.5, -2.4, 2.1), (-0.6, 0.5, 1.0), lens=22)
    elif sid == "s33":
        A = room(1.2, dawn=True); so = A["sill_out"]; bpy.data.objects["moon"].data.energy = 700; bpy.data.objects["moon"].location.x -= 1.5
        rv = raven.build(tuple(so + Vector((0, 0, 0.02))), R(-90), name="raven"); L = ["raven"]; held = ["study"]
        raven.head_moves(rv, FPS, 10.5, seed=11, calm=0.4)
        t0, d = line_at("s33", "C5"); raven.speak(rv, FPS, t0, d)
        raven.flap(rv, FPS, 13.0, n=10)
        r0 = rv["root"]; r0.keyframe_insert("location", frame=int(13.0 * FPS))
        r0.location = (r0.location.x - 6, r0.location.y + 3, r0.location.z + 3); r0.keyframe_insert("location", frame=int(16.0 * FPS))
        camera("cam", (-1.6, 0.45, 1.25), tuple(so + Vector((0, 0, 0.3))), lens=55, fstop=2.8)
    else:
        raise SystemExit(f"plano sem cena 3D: {sid}")
    return L, held, dur

INSERTS = ["ins_key", "ins_candle", "ins_glass", "ins_shadow", "ins_hand"]
def insert_build(name):
    c = coll("ins"); bpy.context.scene.view_settings.exposure = 1.6
    wood = mat_wood("walnut", (0.07, 0.03, 0.012), (0.16, 0.075, 0.03), 5.0, 0.4, 0.3)
    box("table", (2, 2, 0.05), (0, 0, -0.025), wood, coll=c)
    light("warm", "POINT", (0.3, -0.3, 0.6), 25, kelvin(1900), size=0.05, coll=c)
    world_color((0.01, 0.006, 0.003), 1)
    if name == "ins_key":
        brass = mat("brass", (0.55, 0.38, 0.15), 0.3, 1.0)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.025, minor_radius=0.005, location=(0, 0, 0.005)); bpy.context.object.data.materials.append(brass)
        box("key_shaft", (0.09, 0.008, 0.008), (0.07, 0, 0.005), brass); box("key_bit", (0.012, 0.02, 0.006), (0.105, 0.012, 0.005), brass)
        camera("cam", (0.12, -0.18, 0.12), (0.05, 0, 0.0), lens=85, fstop=2.0)
    elif name == "ins_candle":
        cyl("c", 0.022, 0.18, (0, 0, 0.022), mat("wax", (0.85, 0.8, 0.68), 0.5, sss=0.5), rot=(0, R(90), R(20)))
        cyl("st", 0.07, 0.02, (-0.18, 0.05, 0.01), mat("brass", (0.55, 0.38, 0.15), 0.3, 1.0))
        camera("cam", (0.3, -0.3, 0.12), (0, 0, 0.02), lens=50, fstop=2.0)
    elif name == "ins_glass":
        import random as Rn; r = Rn.Random(4); g = mat("glass", (0.8, 0.8, 0.8), 0.05, transmission=1.0)
        for k in range(28):
            box(f"shard{k}", (r.uniform(0.01, 0.05), r.uniform(0.01, 0.04), 0.002), (r.uniform(-0.2, 0.2), r.uniform(-0.15, 0.15), 0.002), g, rot=(0, 0, r.uniform(0, 3)), bevel=0)
        camera("cam", (0.0, -0.45, 0.28), (0, 0, 0), lens=50, fstop=2.8)
    elif name == "ins_shadow":
        box("wall", (3, 0.1, 3), (0, 1, 1.5), mat_wallpaper("wallpaper_corr", (0.06, 0.05, 0.04), (0.12, 0.1, 0.08)), coll=c)
        rig = human.build("eleanor", (0.3, 0.2, 0), R(90)); human.pose(rig, shR=(-30, 0, 0))
        light("warm2", "POINT", (0.5, -2.5, 1.5), 300, kelvin(1900), size=0.02)
        camera("cam", (-0.8, -1.8, 1.4), (-0.5, 1.0, 1.4), lens=35)
        for o in bpy.data.collections["eleanor"].all_objects: o.visible_camera = False
    elif name == "ins_hand":
        box("door", (1.0, 0.05, 2.0), (0, 0.1, 1.0), mat_wood("walnut"), coll=c)
        rig = human.build("eleanor", (0, -0.45, 0), 0); human.pose(rig, shR=(-95, 0, 0), elR=(-20, 0, 0), wrR=(-70, 0, 0)); bpy.context.view_layer.update()
        wr = rig["wrR"].matrix_world.translation.copy()
        camera("cam", tuple(wr + Vector((0.35, -0.35, 0.05))), tuple(wr + Vector((0, 0.08, -0.05))), lens=70, fstop=2.0)

def main():
    sid, mode = sys.argv[1], sys.argv[2]
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else None
    reset()
    out = f"{ROOT}/renders/scenes/{sid}"; os.makedirs(out, exist_ok=True)
    if sid in INSERTS:
        insert_build(sid); quality(samples or 48, True, res=0.3 if mode == "preview" else 1.0)
        render(f"{ROOT}/renders/preview/{sid}.png" if mode == "preview" else f"{out}/plate.png"); return
    layers, held, dur = shot_build(sid, mode)
    sc = bpy.context.scene; sc.render.fps = FPS
    t0 = time.time()
    if mode == "preview":
        if layers and ("arthur" in layers or "eleanor" in layers):
            for o in bpy.data.objects:
                if o.type == "LIGHT" and o.name.startswith("candle_light"): o.data.energy *= 0.15
        quality(samples or 12, True, res=0.3); sc.frame_set(int(dur * FPS * 0.6))
        render(f"{ROOT}/renders/preview/{sid}.png")
    elif mode == "plate":
        if layers: hide_collections(layers)
        quality(samples or 48, True, transparent=False)
        render(f"{out}/plate.png", frame=0)
    elif mode == "layer":
        if not layers: print("sem camada"); return
        hold_collections(held)
        if "arthur" in layers or "eleanor" in layers:   # personagens humanos sempre em silhueta (sem luz de vela)
            for o in bpy.data.objects:
                if o.type == "LIGHT" and o.name.startswith(("candle_light", "clock_fill", "sconce_l")): o.hide_render = True
        for v in ("fog_volume", "window_glass"):
            if v in bpy.data.objects: bpy.data.objects[v].hide_render = True
        quality(samples or 12, True, transparent=True, res=0.5); sc.render.use_persistent_data = True
        os.makedirs(f"{out}/layer", exist_ok=True)
        n = int(dur * FPS)
        start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        for f in range(start, n):
            p = f"{out}/layer/{f:04d}.png"
            if os.path.exists(p): continue
            render(p, frame=f)
    print("TIME", sid, mode, round(time.time() - t0, 1))

if __name__ == "__main__":
    main()
