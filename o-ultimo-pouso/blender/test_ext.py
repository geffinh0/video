import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import exterior
reset(); bpy.context.scene.view_settings.exposure = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
c = coll("ext")
exterior.ground(c); exterior.night(sky=(0.02, 0.035, 0.05), moon_energy=2.5, moon_dir=(math.radians(75), 0, math.radians(170)))
m, win = exterior.mansion(c, (0, 30, 0))
exterior.forest(c, (0, 10), 35, 70, clear=((0, 22), 14))
world_fog(float(sys.argv[2]) if len(sys.argv) > 2 else 0.008, (0.55, 0.65, 0.75), 0.5)
camera("cam", (2, -12, 4.5), (0, 30, 8), lens=35)
quality(16, True, res=0.4)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
