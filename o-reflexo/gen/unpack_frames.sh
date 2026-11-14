#!/usr/bin/env bash
# Decodifica frames_enc/<plano>_<inicio>.mp4 para renders/frames/<plano>/NNNN.jpg (sem sobrescrever quadros locais)
cd "$(dirname "$0")/.."
for f in frames_enc/*.mp4; do
  b=$(basename "$f" .mp4); s=${b%_*}; first=${b##*_}; d=renders/frames/$s; mkdir -p $d
  ffmpeg -v error -y -i "$f" -q:v 2 -start_number $((10#$first)) "$d/%04d.jpg" && echo "ok $b"
done
