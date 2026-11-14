#!/usr/bin/env bash
# Worker de nuvem: instala o mínimo, baixa só o LivePortrait, renderiza um plano (ou faixa de quadros)
# e publica os quadros como vídeo (frames_enc/<plano>_<a>_<b>.mp4) no branch atual.
# Uso: bash gen/anim_worker.sh <plano> [<a> <b>]
set -u
cd "$(dirname "$0")/.."
S=$1; A=${2:-0}; B=${3:-99999}
python3 -c "import torch, cv2, onnxruntime" 2>/dev/null || pip install -q torch torchvision opencv-python-headless onnxruntime scipy pyyaml rich tyro imageio scikit-image huggingface_hub
[ -d vendor/LivePortrait ] || git clone -q --depth 1 https://github.com/KwaiVGI/LivePortrait.git vendor/LivePortrait
HF_HUB_DISABLE_XET=1 python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('KwaiVGI/LivePortrait', local_dir='models/liveportrait', allow_patterns=['liveportrait/base_models/*','liveportrait/retargeting_models/*','liveportrait/landmark.onnx'])"
RANGE="$A:$B" python3 gen/anim.py $S 2>&1 | grep --line-buffered -E "^s0|DONE|SKIP|Error|Trace|line [0-9]"
BR=$(git rev-parse --abbrev-ref HEAD); mkdir -p frames_enc; OUTV=frames_enc/${S}_${A}_${B}.mp4
python3 - "$S" "$A" "$B" <<'PY'
import sys, os, shutil
s, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); d = f"renders/frames/{s}"; t = f"renders/tmp_{s}"
os.makedirs(t, exist_ok=True)
fs = sorted(x for x in os.listdir(d) if x.endswith(".jpg") and a <= int(x[:4]) < b)
for k, x in enumerate(fs): shutil.copy(f"{d}/{x}", f"{t}/{k:04d}.jpg")
open(f"{t}/first.txt", "w").write(fs[0][:4] if fs else "0")
PY
FIRST=$(cat renders/tmp_$S/first.txt)
ffmpeg -v error -y -framerate 15 -i renders/tmp_$S/%04d.jpg -c:v libx264 -crf 12 -preset slow -pix_fmt yuv444p frames_enc/${S}_${FIRST}.mp4
git add frames_enc/${S}_${FIRST}.mp4 && git commit -qm "Quadros $S a partir de $FIRST"
for i in 1 2 3 4 5 6; do git pull -q --rebase origin "$BR" && git push -q origin "HEAD:$BR" && { echo "PUSHED $S $FIRST"; break; }; sleep $((i*5)); done
echo "WORKER DONE"
