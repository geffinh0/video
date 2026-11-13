#!/usr/bin/env bash
# Worker de render distribuído: baixa os assets, renderiza as camadas dos shots dados, codifica em VP9 com alfa
# e publica em layers_enc/<shot>.webm no branch atual (git pull --rebase + push com retentativas).
# Uso: bash scripts/worker.sh s04 s12 ...
set -u
cd "$(dirname "$0")/.."
python3 -c "import bpy" 2>/dev/null || pip install -q bpy numpy pillow scipy
python3 scripts/assets.py | grep -v "^ok" || true
BR=$(git rev-parse --abbrev-ref HEAD)
mkdir -p layers_enc
for s in "$@"; do
  git pull -q --rebase origin "$BR" 2>/dev/null
  [ -f layers_enc/$s.webm ] && { echo "SKIP $s (já feito por outro worker)"; continue; }
  python3 blender/shots.py $s layer 2>&1 | grep -E "^TIME|Error|Traceback"
  ffmpeg -v error -y -framerate 30 -start_number 0 -i renders/scenes/$s/layer/%04d.png \
    -c:v libvpx-vp9 -pix_fmt yuva420p -crf 16 -b:v 0 -row-mt 1 layers_enc/$s.webm || { echo "ENCODE FAIL $s"; continue; }
  git add layers_enc/$s.webm
  git commit -qm "Camada $s (30 fps)"
  for i in 1 2 3 4 5 6; do
    git pull -q --rebase origin "$BR" && git push -q origin "HEAD:$BR" && { echo "PUSHED $s"; break; }
    sleep $((i * 5))
  done
done
echo "WORKER DONE"
