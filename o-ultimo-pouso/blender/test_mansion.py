"""Teste de forma da mansão com luz neutra: python3 blender/test_mansion.py out.png"""
import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import exterior
reset(); bpy.context.scene.view_settings.exposure = 1.5
c = coll("ext"); exterior.ground(c); exterior.mansion(c, (0, 30, 0))
sun = bpy.data.lights.new("s", "SUN"); sun.energy = 4; so = bpy.data.objects.new("s", sun); bpy.context.scene.collection.objects.link(so); so.rotation_euler = (math.radians(55), 0, math.radians(-35))
world_color((0.15, 0.2, 0.28))
camera("cam", (-14, -12, 5), (0, 28, 9), lens=26)
quality(24, True, res=0.6)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
