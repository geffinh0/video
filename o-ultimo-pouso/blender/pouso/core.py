"""Núcleo: cena, render, materiais procedurais, luzes e câmera (Blender 5.3 / bpy)."""
import bpy, math, random
from mathutils import Vector

W, H = 1920, 800  # 2,4:1 (barras pretas adicionadas na montagem para 1920x1080)

def reset(seed=1897):
    random.seed(seed)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = False
    sc.render.threads_mode = "FIXED"; sc.render.threads = 4
    sc.view_settings.view_transform = "AgX"
    try: sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception: pass
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 3; sc.cycles.glossy_bounces = 3
    sc.cycles.transparent_max_bounces = 8; sc.cycles.volume_bounces = 0
    sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 1.0
    sc.render.fps = 24
    w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True
    world_color((0.002, 0.003, 0.005), 1.0)
    return sc

def quality(samples=64, denoise=True, transparent=False, res=1.0):
    sc = bpy.context.scene
    sc.cycles.samples = samples; sc.cycles.use_denoising = denoise
    if denoise:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.render.film_transparent = transparent
    sc.render.resolution_percentage = int(res * 100)

def world_color(rgb, strength=1.0):
    nt = bpy.context.scene.world.node_tree
    bg = nt.nodes.get("Background")
    bg.inputs[0].default_value = (*rgb, 1); bg.inputs[1].default_value = strength

def world_fog(density=0.02, color=(0.35, 0.42, 0.5), anis=0.3, size=(160, 160, 40), center=(0, 20, 18)):
    """Neblina: cubo volumétrico (só para fundos estáticos: é cara)."""
    m = bpy.data.materials.new("fog"); m.use_nodes = True; nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Density"].default_value = density
    vol.inputs["Color"].default_value = (*color, 1)
    vol.inputs["Anisotropy"].default_value = anis
    if "Absorption Color" in vol.inputs: vol.inputs["Absorption Color"].default_value = (1, 1, 1, 1)
    nt.links.new(vol.outputs[0], nt.nodes["Material Output"].inputs["Volume"])
    bpy.ops.mesh.primitive_cube_add(size=1, location=center); o = bpy.context.object; o.name = "fog_volume"; o.scale = size
    o.data.materials.append(m)
    o.visible_shadow = False
    sc = bpy.context.scene; sc.cycles.volume_bounces = 0; sc.cycles.volume_step_rate = 4.0
    return o

# ---------------- materiais ----------------
def _bsdf(m):
    return m.node_tree.nodes.get("Principled BSDF")

def mat(name, color, rough=0.6, metal=0.0, spec=0.5, emit=None, emit_str=0.0, alpha=1.0, sss=0.0, transmission=0.0, ior=1.45, coat=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = _bsdf(m)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["IOR"].default_value = ior
    if "Specular IOR Level" in b.inputs: b.inputs["Specular IOR Level"].default_value = spec
    if transmission: b.inputs["Transmission Weight"].default_value = transmission
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.2)
        b.inputs["Subsurface Scale"].default_value = 0.01
    if coat: b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = emit_str
    if alpha < 1: b.inputs["Alpha"].default_value = alpha
    return m

def _n(m, kind, **kw):
    n = m.node_tree.nodes.new(kind)
    for k, v in kw.items():
        if k in n.inputs: n.inputs[k].default_value = v
        else: setattr(n, k, v)
    return n

def _ramp(m, c1, c2, pos=(0.3, 0.7)):
    r = m.node_tree.nodes.new("ShaderNodeValToRGB")
    e = r.color_ramp.elements; e[0].position, e[1].position = pos
    e[0].color = (*c1, 1); e[1].color = (*c2, 1)
    return r

def mat_noise(name, c1, c2, scale=4.0, detail=8.0, rough=0.6, bump=0.15, rough_var=0.2, metal=0.0, coord="Object", stretch=None):
    """Material com variação procedural (pedra, gesso, papel, couro...)."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, c1, rough, metal); L = m.node_tree.links; b = _bsdf(m)
    tc = _n(m, "ShaderNodeTexCoord")
    src = tc.outputs[coord]
    if stretch:
        mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = stretch; L.new(src, mp.inputs[0]); src = mp.outputs[0]
    nz = _n(m, "ShaderNodeTexNoise", Scale=scale, Detail=detail, Roughness=0.6)
    L.new(src, nz.inputs["Vector"])
    r = _ramp(m, c1, c2); L.new(nz.outputs["Fac"], r.inputs[0]); L.new(r.outputs[0], b.inputs["Base Color"])
    rr = _n(m, "ShaderNodeMapRange", **{"To Min": rough - rough_var, "To Max": rough + rough_var})
    L.new(nz.outputs["Fac"], rr.inputs[0]); L.new(rr.outputs[0], b.inputs["Roughness"])
    bp = _n(m, "ShaderNodeBump", Strength=bump, Distance=0.02); L.new(nz.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def mat_wood(name, c1=(0.05, 0.022, 0.01), c2=(0.12, 0.055, 0.025), scale=3.0, rough=0.45, coat=0.15):
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, c1, rough, coat=coat); L = m.node_tree.links; b = _bsdf(m)
    tc = _n(m, "ShaderNodeTexCoord")
    mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 1, 8)
    L.new(tc.outputs["Object"], mp.inputs[0])
    nz = _n(m, "ShaderNodeTexNoise", Scale=2.0, Detail=4.0)
    L.new(mp.outputs[0], nz.inputs["Vector"])
    wv = _n(m, "ShaderNodeTexWave", Scale=scale, Distortion=6.0, Detail=4.0)
    wv.bands_direction = "Z"; L.new(mp.outputs[0], wv.inputs["Vector"])
    mix = _n(m, "ShaderNodeMath", operation="MULTIPLY"); L.new(wv.outputs["Fac"], mix.inputs[0]); L.new(nz.outputs["Fac"], mix.inputs[1])
    r = _ramp(m, c1, c2, (0.1, 0.6)); L.new(mix.outputs[0], r.inputs[0]); L.new(r.outputs[0], b.inputs["Base Color"])
    bp = _n(m, "ShaderNodeBump", Strength=0.08); L.new(mix.outputs[0], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def mat_planks(name, c1=(0.035, 0.018, 0.009), c2=(0.09, 0.045, 0.02)):
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, c1, 0.5, coat=0.2); L = m.node_tree.links; b = _bsdf(m)
    tc = _n(m, "ShaderNodeTexCoord")
    br = _n(m, "ShaderNodeTexBrick", Scale=1.0, **{"Mortar Size": 0.004, "Brick Width": 1.6, "Row Height": 0.16})
    br.offset = 0.37; br.inputs["Color1"].default_value = (*c1, 1); br.inputs["Color2"].default_value = (*c2, 1)
    br.inputs["Mortar"].default_value = (0.01, 0.005, 0.003, 1)
    L.new(tc.outputs["Object"], br.inputs["Vector"])
    nz = _n(m, "ShaderNodeTexNoise", Scale=30.0, Detail=6.0)
    mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (0.15, 3, 1); L.new(tc.outputs["Object"], mp.inputs[0]); L.new(mp.outputs[0], nz.inputs["Vector"])
    mx = _n(m, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); mx.inputs[0].default_value = 0.6
    L.new(br.outputs["Color"], mx.inputs[6]); L.new(nz.outputs["Color"], mx.inputs[7]); L.new(mx.outputs[2], b.inputs["Base Color"])
    bp = _n(m, "ShaderNodeBump", Strength=0.25); L.new(br.outputs["Fac"], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def mat_wallpaper(name, c1=(0.025, 0.04, 0.035), c2=(0.05, 0.07, 0.06)):
    """Papel de parede vitoriano: padrão de damasco aproximado por voronoi + listras."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, c1, 0.8); L = m.node_tree.links; b = _bsdf(m)
    tc = _n(m, "ShaderNodeTexCoord")
    vo = _n(m, "ShaderNodeTexVoronoi", Scale=9.0); vo.feature = "F1"
    L.new(tc.outputs["Object"], vo.inputs["Vector"])
    wv = _n(m, "ShaderNodeTexWave", Scale=6.0, Distortion=2.0); wv.wave_type = "BANDS"; wv.bands_direction = "X"
    L.new(tc.outputs["Object"], wv.inputs["Vector"])
    mul = _n(m, "ShaderNodeMath", operation="MULTIPLY"); L.new(vo.outputs["Distance"], mul.inputs[0]); L.new(wv.outputs["Fac"], mul.inputs[1])
    r = _ramp(m, c1, c2, (0.05, 0.5)); L.new(mul.outputs[0], r.inputs[0]); L.new(r.outputs[0], b.inputs["Base Color"])
    nz = _n(m, "ShaderNodeTexNoise", Scale=2.0, Detail=5.0)  # manchas de umidade
    L.new(tc.outputs["Object"], nz.inputs["Vector"])
    dk = _n(m, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); dk.inputs[0].default_value = 0.5
    L.new(r.outputs[0], dk.inputs[6]); L.new(nz.outputs["Color"], dk.inputs[7]); L.new(dk.outputs[2], b.inputs["Base Color"])
    return m

def mat_glass_rain(name="glass_rain"):
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, (0.6, 0.65, 0.7), rough=0.08, transmission=1.0, ior=1.5); L = m.node_tree.links; b = _bsdf(m)
    tc = _n(m, "ShaderNodeTexCoord")
    mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1, 1, 0.25); L.new(tc.outputs["Object"], mp.inputs[0])
    vo = _n(m, "ShaderNodeTexVoronoi", Scale=40.0); L.new(mp.outputs[0], vo.inputs["Vector"])
    rr = _n(m, "ShaderNodeMapRange", **{"From Min": 0.0, "From Max": 0.25, "To Min": 1.0, "To Max": 0.0}); L.new(vo.outputs["Distance"], rr.inputs[0])
    bp = _n(m, "ShaderNodeBump", Strength=0.6, Distance=0.002); L.new(rr.outputs[0], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def mat_emit(name, color, strength):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.remove(nt.nodes["Principled BSDF"])
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*color, 1); e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], nt.nodes["Material Output"].inputs[0])
    return m

def mat_image(name, path, rough=0.7, emit=0.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, (1, 1, 1), rough); L = m.node_tree.links; b = _bsdf(m)
    tx = _n(m, "ShaderNodeTexImage"); tx.image = bpy.data.images.load(path)
    L.new(tx.outputs["Color"], b.inputs["Base Color"])
    if emit:
        L.new(tx.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emit
    return m

# ---------------- objetos ----------------
def obj_from_mesh(name, mesh, mtl=None, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, coll=None):
    o = bpy.data.objects.new(name, mesh)
    (coll or bpy.context.scene.collection).objects.link(o)
    o.location = loc; o.rotation_euler = rot
    if mtl: o.data.materials.append(mtl)
    if parent: o.parent = parent
    return o

def _active(o):
    for s in bpy.context.selected_objects: s.select_set(False)
    bpy.context.view_layer.objects.active = o; o.select_set(True)

def box(name, size, loc=(0, 0, 0), mtl=None, rot=(0, 0, 0), bevel=0.004, parent=None, coll=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        md = o.modifiers.new("bev", "BEVEL"); md.width = bevel; md.segments = 2; md.limit_method = "ANGLE"
    if mtl: o.data.materials.append(mtl)
    if parent: o.parent = parent
    _move(o, coll)
    return o

def cyl(name, r, h, loc=(0, 0, 0), mtl=None, rot=(0, 0, 0), verts=32, r2=None, parent=None, coll=None, smooth=True):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=r, radius2=r2, depth=h, vertices=verts, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    if smooth: bpy.ops.object.shade_smooth()
    if mtl: o.data.materials.append(mtl)
    if parent: o.parent = parent
    _move(o, coll)
    return o

def sphere(name, r, loc=(0, 0, 0), mtl=None, scale=(1, 1, 1), seg=32, parent=None, coll=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=seg, ring_count=seg // 2)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth()
    if mtl: o.data.materials.append(mtl)
    if parent: o.parent = parent
    _move(o, coll)
    return o

def plane(name, size, loc=(0, 0, 0), mtl=None, rot=(0, 0, 0), coll=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = (size[0], size[1], 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mtl: o.data.materials.append(mtl)
    _move(o, coll)
    return o

def coll(name):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c

def _move(o, c):
    if not c: return
    for oc in list(o.users_collection): oc.objects.unlink(o)
    c.objects.link(o)

def empty(name, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, coll=None):
    e = bpy.data.objects.new(name, None); (coll or bpy.context.scene.collection).objects.link(e)
    e.location = loc; e.rotation_euler = rot
    if parent: e.parent = parent
    return e

# ---------------- luzes ----------------
def kelvin(k):
    k = k / 100.0
    r = 1.0 if k <= 66 else min(1, 1.292936 * (k - 60) ** -0.1332)
    g = min(1, 0.390081 * math.log(k) - 0.631841) if k <= 66 else min(1, 1.129891 * (k - 60) ** -0.0755)
    b = 1.0 if k >= 66 else (0.0 if k <= 19 else min(1, 0.543207 * math.log(k - 10) - 1.196254))
    return (max(r, 0), max(g, 0), max(b, 0))

def light(name, kind, loc, energy, color=(1, 1, 1), size=0.1, rot=(0, 0, 0), spot=None, shadow_soft=None, coll=None):
    ld = bpy.data.lights.new(name, kind); ld.energy = energy; ld.color = color
    if kind in ("POINT", "SPOT"): ld.shadow_soft_size = size
    if kind == "AREA": ld.size = size
    if kind == "SPOT" and spot: ld.spot_size = math.radians(spot); ld.spot_blend = 0.6
    o = bpy.data.objects.new(name, ld); (coll or bpy.context.scene.collection).objects.link(o)
    o.location = loc; o.rotation_euler = rot
    return o

def look_at(o, target):
    d = Vector(target) - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()

def camera(name, loc, target, lens=35, fstop=None, focus=None, sensor=36):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = sensor
    o = bpy.data.objects.new(name, cd); bpy.context.scene.collection.objects.link(o)
    o.location = loc; look_at(o, target)
    if fstop:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
        cd.dof.focus_distance = focus if focus else (Vector(target) - Vector(loc)).length
    bpy.context.scene.camera = o
    return o

def render(path, frame=None):
    sc = bpy.context.scene
    if frame is not None: sc.frame_set(frame)
    sc.render.filepath = path
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if sc.render.film_transparent else "RGB"
    bpy.ops.render.render(write_still=True)

# ---------------- assets livres (Poly Haven, CC0) adaptados à paleta do filme ----------------
import os as _os
ASSETS = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), "assets/polyhaven")

def _grade(m, tint=(1, 1, 1), value=1.0, sat=1.0, rough=None, tag=""):
    """Reinterpreta um material importado: multiplica a cor base (tint), ajusta valor/saturação e aspereza."""
    b = _bsdf(m)
    if b is None: return
    L = m.node_tree.links; inp = b.inputs["Base Color"]
    hs = _n(m, "ShaderNodeHueSaturation"); hs.inputs["Saturation"].default_value = sat; hs.inputs["Value"].default_value = value
    mx = _n(m, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (*tint, 1)
    if inp.is_linked:
        src = inp.links[0].from_socket; L.remove(inp.links[0]); L.new(src, hs.inputs["Color"])
    else: hs.inputs["Color"].default_value = inp.default_value[:]
    L.new(hs.outputs[0], mx.inputs[6]); L.new(mx.outputs[2], inp)
    if rough is not None:
        r = b.inputs["Roughness"]
        if r.is_linked:
            src = r.links[0].from_socket; L.remove(r.links[0])
            mr = _n(m, "ShaderNodeMath", operation="MULTIPLY"); mr.use_clamp = True; L.new(src, mr.inputs[0]); mr.inputs[1].default_value = rough; L.new(mr.outputs[0], r)
        else: r.default_value = min(1, r.default_value * rough)

def asset(name, loc=(0, 0, 0), rot_z=0.0, scale=1.0, coll=None, parent=None, tint=(1, 1, 1), value=1.0, sat=1.0, rough=None, key=None):
    """Importa um modelo glTF do Poly Haven e devolve (empty raiz, {nome: objeto}).
    Cada uso ganha materiais próprios regraduados (tint/value/sat) para a paleta do filme."""
    f = f"{ASSETS}/models/{name}/{name}.gltf"; before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=f)
    new = [o for o in bpy.data.objects if o not in before]
    c = coll or bpy.context.scene.collection; key = key or f"{name}_{len(bpy.data.objects)}"
    root = empty(key, loc, (0, 0, rot_z), parent=parent, coll=c); root.scale = (scale,) * 3
    done = {}
    for o in new:
        for oc in list(o.users_collection): oc.objects.unlink(o)
        c.objects.link(o)
        if o.parent is None: o.parent = root
        if o.type == "MESH":
            for sl in o.material_slots:
                if sl.material is None: continue
                if sl.material.name not in done:
                    m = sl.material.copy(); m.name = f"{key}_{sl.material.name}"; _grade(m, tint, value, sat, rough); done[sl.material.name] = m
                sl.material = done[sl.material.name]
    return root, {o.name.split(".")[0]: o for o in new}

def mat_pbr(name, tex, scale=1.0, tint=(1, 1, 1), value=1.0, sat=1.0, rough=1.0, bump=1.0, rot=0.0):
    """Material PBR com texturas reais (Poly Haven), projeção em caixa nas coordenadas do objeto (sem UV)."""
    m = bpy.data.materials.get(name)
    if m: return m
    m = mat(name, (0.5, 0.5, 0.5), 0.6); b = _bsdf(m); L = m.node_tree.links; d = f"{ASSETS}/textures/{tex}"
    tc = _n(m, "ShaderNodeTexCoord"); mp = _n(m, "ShaderNodeMapping"); mp.inputs["Scale"].default_value = (scale,) * 3; mp.inputs["Rotation"].default_value = (0, 0, rot)
    L.new(tc.outputs["Object"], mp.inputs[0])
    def img(fn, cs):
        for ext in ("jpg", "png"):
            p = f"{d}/{fn}.{ext}"
            if _os.path.exists(p):
                n = _n(m, "ShaderNodeTexImage"); n.image = bpy.data.images.load(p, check_existing=True); n.image.colorspace_settings.name = cs
                n.projection = "BOX"; n.projection_blend = 0.25; L.new(mp.outputs[0], n.inputs["Vector"]); return n
    di = img("diff", "sRGB")
    if di:
        hs = _n(m, "ShaderNodeHueSaturation"); hs.inputs["Saturation"].default_value = sat; hs.inputs["Value"].default_value = value; L.new(di.outputs["Color"], hs.inputs["Color"])
        mx = _n(m, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY"); mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (*tint, 1)
        L.new(hs.outputs[0], mx.inputs[6]); L.new(mx.outputs[2], b.inputs["Base Color"])
    if not di:      # textura sem mapa de cor: usa a cor do filme com leve variação
        nzc = _n(m, "ShaderNodeTexNoise", Scale=9.0, Detail=6.0); L.new(mp.outputs[0], nzc.inputs["Vector"])
        mxc = _n(m, "ShaderNodeMix", data_type="RGBA"); L.new(nzc.outputs["Fac"], mxc.inputs[0])
        mxc.inputs[6].default_value = (*[t * value * 0.55 for t in tint], 1); mxc.inputs[7].default_value = (*[t * value for t in tint], 1)
        L.new(mxc.outputs[2], b.inputs["Base Color"])
    ri = img("rough", "Non-Color")
    if ri:
        mr = _n(m, "ShaderNodeMath", operation="MULTIPLY"); mr.use_clamp = True; mr.inputs[1].default_value = rough; L.new(ri.outputs["Color"], mr.inputs[0]); L.new(mr.outputs[0], b.inputs["Roughness"])
    ni = img("nor", "Non-Color")
    if ni:
        nm = _n(m, "ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bump; nm.space = "OBJECT" if False else "TANGENT"
        # projeção em caixa não tem tangentes: usa o relevo (disp) como bump, mais robusto
    hi = img("disp", "Non-Color")
    if hi:
        bp = _n(m, "ShaderNodeBump", Strength=0.35 * bump, Distance=0.01); L.new(hi.outputs["Color"], bp.inputs["Height"]); L.new(bp.outputs[0], b.inputs["Normal"])
    return m

def world_hdri(name, strength=1.0, rot_z=0.0, tint=(1, 1, 1)):
    """Céu noturno real (HDRI Poly Haven) como luz ambiente."""
    w = bpy.context.scene.world; nt = w.node_tree; bg = nt.nodes.get("Background")
    env = nt.nodes.new("ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(f"{ASSETS}/hdris/{name}.hdr", check_existing=True)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = (0, 0, rot_z)
    nt.links.new(tc.outputs["Generated"], mp.inputs[0]); nt.links.new(mp.outputs[0], env.inputs[0])
    mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (*tint, 1)
    nt.links.new(env.outputs[0], mx.inputs[6]); nt.links.new(mx.outputs[2], bg.inputs[0]); bg.inputs[1].default_value = strength
