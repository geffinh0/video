import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import raven
reset(); bpy.context.scene.view_settings.exposure = 1.0
rv = raven.build((0, 0, 0), math.radians(-30), fuzz=("fuzz" in sys.argv))
if len(sys.argv) > 2 and sys.argv[2] == "wings":
    for sx, w in zip((-1, 1), rv["wings"]): w.rotation_euler = raven.WING_OPEN(sx)
rv["neck"].rotation_euler = (0, math.radians(-10), math.radians(25))
box("ledge", (1.2, 0.6, 0.1), (0, 0, -0.05), mat_noise("stone", (0.08, 0.08, 0.085), (0.2, 0.2, 0.21), 8, rough=0.85, bump=0.4))
k = light("key", "AREA", (0.9, 0.2, 0.9), 40, kelvin(9000), size=0.8); look_at(k, (0, 0, 0.2))
k2 = light("rim", "AREA", (-0.8, -0.6, 0.6), 60, kelvin(12000), size=0.4); look_at(k2, (0, 0, 0.2))
world_color((0.01, 0.015, 0.02))
camera("cam", (0.95, 0.35, 0.3), (0, -0.02, 0.19), lens=45, fstop=5.6)
quality(32, True, res=0.6)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
