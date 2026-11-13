import sys, time; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
from pouso.core import *; from pouso import study
reset(); A = study.build("/home/user/video/o-ultimo-pouso/assets/textures")
quality(int(sys.argv[2]) if len(sys.argv) > 2 else 16, True, res=float(sys.argv[3]) if len(sys.argv) > 3 else 0.4)
import bpy; bpy.context.scene.view_settings.exposure = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
camera("cam", (2.5, -2.4, 2.1), (-0.9, 0.7, 1.0), lens=22)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
