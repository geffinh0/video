#!/usr/bin/env bash
# Decodifica layers_enc/<shot>.webm (VP9 com alfa) de volta para renders/scenes/<shot>/layer/####.png
cd "$(dirname "$0")/.."
for f in layers_enc/*.webm; do
  s=$(basename "$f" .webm); d=renders/scenes/$s/layer
  [ -f "$d/.unpacked" ] && [ "$d/.unpacked" -nt "$f" ] && continue
  rm -rf "$d"; mkdir -p "$d"
  ffmpeg -v error -y -c:v libvpx-vp9 -i "$f" -pix_fmt rgba -start_number 0 "$d/%04d.png" && touch "$d/.unpacked" && echo "ok $s $(ls $d | wc -l)"
done
