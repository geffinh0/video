"""Turnaround de personagem: python3 blender/test_human.py out.png arthur|eleanor [sit]"""
import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import human
reset(); bpy.context.scene.view_settings.exposure = 0.8
kind = sys.argv[2]
for i, rz in enumerate((200, 90, 20)):
    rig = human.build(kind, (i * 1.2 - 1.2, 0, 0), math.radians(rz), coll_name=f"{kind}{i}")
    if "sit" in sys.argv: human.pose(rig, **human.SIT, **human.WRITE)
box("floor", (8, 8, 0.02), (0, 0, -0.01), mat("fl", (0.05, 0.04, 0.03), 0.6))
k = light("key", "AREA", (2.5, 3.0, 2.6), 900, kelvin(4500), size=2.0); look_at(k, (0, 0, 1.2))
k = light("rim", "AREA", (-2.5, -2.5, 2.4), 700, kelvin(9500), size=1.5); look_at(k, (0, 0, 1.2))
world_color((0.03, 0.035, 0.04))
if "face" in sys.argv: camera("cam", (0.0, 1.6, 1.68), (0, 0, 1.66), lens=60)
else: camera("cam", (0.0, 5.2, 1.15), (0, 0, 0.98), lens=40)
quality(24, True, res=0.5)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
