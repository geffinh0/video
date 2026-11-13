"""Teste do corpo MakeHuman: python3 blender/test_mh.py out.png [male|female]"""
import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import mh
reset(); bpy.context.scene.view_settings.exposure = 0.8
sex = sys.argv[2] if len(sys.argv) > 2 else "male"
c = coll("h")
o, arm, J = mh.body("h", [(f"macrodetails/universal-{sex}-young-averagemuscle-averageweight", 1.0), (f"macrodetails/caucasian-{sex}-young", 1.0)], 1.8, c)
cols = [(0.6, 0.45, 0.38), (0.1, 0.1, 0.5), (0.5, 0.1, 0.1), (0.1, 0.4, 0.1), (0.9, 0.9, 0.9), (0.9, 0.9, 0.9)]
for i, cl in enumerate(cols): o.data.materials.append(mat(f"p{i}", cl, 0.6))
print("JOINTS", {k: tuple(round(x, 3) for x in J[k][0]) for k in ("root", "spine05", "upperarm01.L", "lowerarm01.L", "wrist.L", "upperleg01.L", "lowerleg01.L", "foot.L", "head", "neck01")})
box("floor", (8, 8, 0.02), (0, 0, -0.01), mat("fl", (0.05, 0.04, 0.03), 0.6))
k = light("key", "AREA", (2.5, 3.0, 2.6), 900, kelvin(4500), size=2.0); look_at(k, (0, 0, 1.2))
k = light("rim", "AREA", (-2.5, -2.5, 2.4), 700, kelvin(9500), size=1.5); look_at(k, (0, 0, 1.2))
world_color((0.03, 0.035, 0.04))
camera("cam", (1.5, 4.2, 1.15), (0, 0, 0.95), lens=40)
quality(24, True, res=0.5)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
