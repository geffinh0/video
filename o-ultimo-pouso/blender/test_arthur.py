import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import human
reset(); bpy.context.scene.view_settings.exposure = 0.5
kind = sys.argv[2] if len(sys.argv) > 2 else "arthur"
rig = human.build(kind)
if "sit" in sys.argv:
    human.pose(rig, **human.SIT, **human.WRITE); rig["root"].location = (0, 0, -0.5)
box("floor", (4, 4, 0.02), (0, 0, -0.01), mat("fl", (0.05, 0.04, 0.03), 0.6))
light("key", "AREA", (0.6, 1.6, 1.8), 25, kelvin(2000), size=0.3); look_at(bpy.data.objects["key"], (0, 0, 1.6))
light("rim", "AREA", (-0.2, 1.8, 2.0), 260, kelvin(9500), size=1.2); look_at(bpy.data.objects["rim"], (0, 0, 1.5))
box("window_glow", (1.2, 0.05, 2.0), (-0.4, 2.6, 1.6), mat_emit("glow", (0.25, 0.35, 0.5), 3))
world_color((0.02, 0.025, 0.03))
if "hand" in sys.argv:
    human.pose(rig, shR=(-60, 0, 10), elR=(-40, 0, 0)); camera("cam", (0.55, 0.85, 1.25), (0.2, 0.35, 1.05), lens=70, fstop=2.8)
elif "face" in sys.argv: camera("cam", (1.0, 0.0, 1.72), (0, 0.02, 1.72), lens=85, fstop=2.8)
else: camera("cam", (2.6, -0.6, 1.2), (0, 0.3, 1.0), lens=35)
quality(24, True, res=0.4)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
