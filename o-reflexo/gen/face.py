"""Animação facial com LivePortrait (MIT) em CPU, por EDIÇÃO DE KEYPOINTS (sem vídeo-guia e sem insightface).
A partir de UM retrato, gera uma sequência de quadros com piscar, olhar, sorriso, boca, e giro de cabeça
controlados por curvas de animação. É assim que "real" e "reflexo" têm a mesma aparência e comportamentos diferentes.

Uso como módulo:
    F = Face("assets/img/clara.png", face_box=(x0, y0, x1, y1))
    img = F.frame(blink=0.0, smile=0.0, gaze=(0, 0), mouth=0.0, yaw=0, pitch=0, roll=0)   # RGB uint8, quadro inteiro
"""
import os, sys
import numpy as np, cv2, torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LP = f"{ROOT}/vendor/LivePortrait"; W = f"{ROOT}/models/liveportrait/liveportrait"
sys.path.insert(0, LP)
from src.config.inference_config import InferenceConfig
from src.live_portrait_wrapper import LivePortraitWrapper
from src.utils.human_landmark_runner import LandmarkRunner
from src.utils.crop import crop_image, prepare_paste_back, paste_back
from src.utils.retargeting_utils import calc_eye_close_ratio, calc_lip_close_ratio

torch.set_num_threads(os.cpu_count())

# Deslocamentos de expressão (índices dos 21 keypoints implícitos) — calibrados empiricamente na comunidade
# (AdvancedLivePortrait / ExpressionEditor, MIT) e ajustados aqui.
def _apply_expr(e, smile=0.0, gaze=(0.0, 0.0), brow=0.0):
    s = smile * 1.0
    if s:
        e[0, 20, 1] += s * -0.01; e[0, 14, 1] += s * -0.02; e[0, 17, 1] += s * 0.0065; e[0, 17, 2] += s * 0.003
        e[0, 13, 1] += s * -0.00275; e[0, 16, 1] += s * -0.00275; e[0, 3, 1] += s * -0.0035; e[0, 7, 1] += s * -0.0035
    gx, gy = gaze
    if gx:
        if gx > 0: e[0, 11, 0] += gx * 0.0007; e[0, 15, 0] += gx * 0.001
        else: e[0, 11, 0] += gx * 0.001; e[0, 15, 0] += gx * 0.0007
    if gy:
        e[0, 11, 1] += gy * -0.001; e[0, 15, 1] += gy * -0.001
    if brow:
        e[0, 1, 1] += brow * -0.001; e[0, 2, 1] += brow * 0.0005; e[0, 1, 2] += brow * 0.0005  # sobrancelha (+ = sobe)
    return e

class Face:
    def __init__(self, img_path, face_box=None):
        cfg = InferenceConfig(flag_force_cpu=True, flag_use_half_precision=False, flag_do_torch_compile=False,
                              checkpoint_F=f"{W}/base_models/appearance_feature_extractor.pth",
                              checkpoint_M=f"{W}/base_models/motion_extractor.pth",
                              checkpoint_G=f"{W}/base_models/spade_generator.pth",
                              checkpoint_W=f"{W}/base_models/warping_module.pth",
                              checkpoint_S=f"{W}/retargeting_models/stitching_retargeting_module.pth")
        self.w = LivePortraitWrapper(cfg)
        self.lmr = LandmarkRunner(ckpt_path=f"{W}/landmark.onnx", onnx_provider="cpu", device_id=0)
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB) if isinstance(img_path, str) else img_path; self.img = img
        H, Wd = img.shape[:2]
        x0, y0, x1, y1 = face_box or (Wd * 0.25, H * 0.15, Wd * 0.75, H * 0.75)
        self.box = (x0, y0, x1, y1)
        # landmarks: primeiro num recorte quadrado em volta do rosto conhecido, depois refinado
        cx, cy, s = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) * 1.1
        a, b = int(max(0, cx - s / 2)), int(max(0, cy - s / 2)); c, d = int(min(Wd, cx + s / 2)), int(min(H, cy + s / 2))
        lmk = self.lmr.run(img[b:d, a:c]); lmk[:, 0] += a; lmk[:, 1] += b
        for _ in range(2): lmk = self.lmr.run(img, lmk)
        self.lmk = lmk
        cr = crop_image(img, lmk, dsize=512, scale=2.3, vx_ratio=0, vy_ratio=-0.125, flag_do_rot=True)
        self.M_c2o = cr["M_c2o"]; crop256 = cv2.resize(cr["img_crop"], (256, 256))
        self.lmk_crop = lmk   # razões de olho/boca são invariantes à escala
        x = self.w.prepare_source(crop256)
        self.info = self.w.get_kp_info(x); self.f_s = self.w.extract_feature_3d(x)
        self.x_s = self.w.transform_keypoint(self.info)
        mask = cv2.imread(f"{LP}/src/utils/resources/mask_template.png", cv2.IMREAD_COLOR)
        self.mask_ori = prepare_paste_back(mask, self.M_c2o, dsize=(Wd, H))
        self.eye0 = float(np.mean(calc_eye_close_ratio(self.lmk_crop[None])))

    def frame(self, blink=0.0, smile=0.0, gaze=(0.0, 0.0), mouth=0.0, yaw=0.0, pitch=0.0, roll=0.0, brow=0.0, crop_only=False, base=None):
        i = self.info
        e = i["exp"].clone(); e = _apply_expr(e, smile, gaze, brow)
        kp = dict(i); kp["exp"] = e
        kp["pitch"] = i["pitch"] + pitch; kp["yaw"] = i["yaw"] + yaw; kp["roll"] = i["roll"] + roll
        x_d = self.w.transform_keypoint(kp)
        x_d = self.w.stitching(self.x_s, x_d)
        if blink > 0.001:   # retarget de olhos: razão de abertura alvo
            tgt = max(0.0, self.eye0 * (1 - blink))
            er = calc_eye_close_ratio(self.lmk_crop[None])[0]
            r = torch.tensor([[float(er[0]), float(er[1]), tgt]], dtype=torch.float32)
            x_d = x_d + self.w.retarget_eye(self.x_s, r)
        if mouth > 0.001:
            r = torch.tensor([[float(calc_lip_close_ratio(self.lmk_crop[None])[0][0]), mouth * 0.6]], dtype=torch.float32)
            x_d = x_d + self.w.retarget_lip(self.x_s, r)
        out = self.w.warp_decode(self.f_s, self.x_s, x_d)
        crop = self.w.parse_output(out["out"])[0]
        if crop_only: return crop
        return paste_back(crop, self.M_c2o, self.img if base is None else base, self.mask_ori)
