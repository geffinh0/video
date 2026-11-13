import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import corridor, human
reset(); bpy.context.scene.view_settings.exposure = 2.0
A = corridor.build(warm="warm" in sys.argv)
if "warm" in sys.argv:
    rig = human.build("eleanor", (0, 11.2, 0), math.radians(0))
    human.pose(rig, shR=(-100, 0, -10), elR=(-40, 0, 0))
    camera("cam", (-0.6, 8.2, 1.5), (0.1, 11.5, 1.4), lens=40, fstop=2.8)
else:
    camera("cam", (0.3, 0.2, 1.6), (0, 12, 1.3), lens=28)
quality(16, True, res=0.4)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
