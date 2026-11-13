import sys, time, math; sys.path.insert(0, "/home/user/video/o-ultimo-pouso/blender")
import bpy
from pouso.core import *; from pouso import study, human
reset(); bpy.context.scene.view_settings.exposure = 1.2
A = study.build("/home/user/video/o-ultimo-pouso/assets/textures")
rig = human.build("arthur", (0, -0.62, 0.0))
human.pose(rig, **human.SIT, **human.WRITE); rig["root"].location = (0, -0.62, -0.47)
# silhueta: câmera atrás/lado, contra a janela e a vela
camera("cam", (0.9, -2.2, 1.35), (-0.5, 0.2, 1.15), lens=32, fstop=4)
quality(24, True, res=0.4)
t = time.time(); render(sys.argv[1]); print("TIME", round(time.time() - t, 1))
