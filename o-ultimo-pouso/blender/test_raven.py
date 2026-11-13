import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import raven
reset(); bpy.context.scene.view_settings.exposure = 1.0
rv = raven.build((0, 0, 0), math.radians(-30), fuzz=("fuzz" in sys.argv))
if len(sys.argv) > 2 and sys.argv[2] == "wings":
    for sx, w in zip((-1, 1), rv["wings"]): w.rotation_euler = raven.WING_OPEN(sx)
rv["neck"].rotation_euler = (0, math.radians(-10), math.radians(25))
box("ledge", (1.2, 0.6, 0.1), (0, 0, -0.05), mat_noise("stone", (0.08, 0.08, 0.085), (0.2, 0.2, 0.21), 8, rough=0.85, bump=0.4))
light("key", "AREA", (-0.9, -0.3, 0.8), 60, kelvin(10000), size=0.6).rotation_euler = (math.radians(50), 0, math.radians(-110))
light("rim", "AREA", (0.5, 0.9, 0.5), 15, kelvin(1900), size=0.3).rotation_euler = (math.radians(60), 0, math.radians(150))
world_color((0.01, 0.015, 0.02))
camera("cam", (0.75, 0.75, 0.32), (0, 0.03, 0.2), lens=45, fstop=4)
quality(24, True, res=0.4)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
