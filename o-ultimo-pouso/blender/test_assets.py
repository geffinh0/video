"""Folha de contato dos assets importados: python3 blender/test_assets.py out.png nome1 nome2 ..."""
import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *
reset(); bpy.context.scene.view_settings.exposure = 0.5
names = sys.argv[2:]; x = 0
for n in names:
    r, obs = asset(n, (x, 0, 0), math.radians(25)); x += 2.2
box("floor", (40, 12, 0.02), (x / 2, 0, -0.01), mat_pbr("fl", "wood_floor_deck", 1.0, value=0.5))
k = light("key", "AREA", (x / 2, -4, 4), 2500, kelvin(3500), size=6); look_at(k, (x / 2, 0, 1))
world_color((0.03, 0.035, 0.04))
camera("cam", (x / 2 - 1.1, -1.9 * x / 2 - 2.5, 1.8), (x / 2 - 1.1, 0, 1.1), lens=32)
quality(24, True, res=0.6)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
