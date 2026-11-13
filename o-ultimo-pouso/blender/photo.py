import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from pouso.core import *; from pouso import human
reset(); bpy.context.scene.view_settings.exposure = 0.6
a = human.build("arthur", (0.28, 0, 0), math.radians(-8)); human.pose(a, shL=(0, 0, 0), shR=(-10, 0, 8), elR=(-60, 0, 0))
e = human.build("eleanor", (-0.28, 0.05, 0), math.radians(8)); human.pose(e, shL=(-15, 0, -8), elL=(-70, 0, 20))
box("backdrop", (6, 0.1, 4), (0, -1.5, 2), mat_noise("bd", (0.3, 0.28, 0.25), (0.5, 0.47, 0.42), 3, rough=0.9))
light("key", "AREA", (-1.2, 2.5, 2.5), 400, kelvin(5000), size=2.0); look_at(bpy.data.objects["key"], (0, 0, 1.4))
world_color((0.2, 0.2, 0.2), 1)
camera("cam", (0, 2.6, 1.5), (0, 0, 1.45), lens=65)
bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y = 700, 860
quality(24, True)
render(sys.argv[1])
