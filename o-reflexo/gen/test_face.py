import sys, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv2, numpy as np
from face import Face
t = time.time(); F = Face("assets/img/test_clara.png", (200, 120, 590, 600)); print("load", round(time.time() - t, 1), "eye0", F.eye0, flush=True)
os.makedirs("renders/test", exist_ok=True)
for name, kw in [("neutral", {}), ("blink", dict(blink=1.0)), ("half", dict(blink=0.5)), ("smile", dict(smile=1.0)), ("smile2", dict(smile=1.8)),
                 ("gaze_r", dict(gaze=(15, 0))), ("gaze_l", dict(gaze=(-15, 0))), ("yaw", dict(yaw=12, gaze=(-10, 0))), ("mouth", dict(mouth=0.5))]:
    t = time.time(); im = F.frame(**kw); cv2.imwrite(f"renders/test/{name}.png", cv2.cvtColor(im, cv2.COLOR_RGB2BGR)); print(name, round(time.time() - t, 2), flush=True)
