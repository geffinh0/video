#!/usr/bin/env bash
# Prévia rápida de todos os shots (baixa resolução) -> renders/preview/<id>.png ; log em renders/preview.log
cd "$(dirname "$0")/.."
: > renders/preview.log
for s in s02 s03 s04 s05 s06 s07 s09 s10b s11 s12 s13 s14 s15 s16 s17 s17b s18 s19 s21 s23 s24 s25 s26 s27 s28 s29 s30 s31 s33 ins_key ins_candle ins_glass ins_shadow ins_hand; do
  python3 blender/shots.py $s preview ${1:-12} 2>&1 | grep -E "^TIME|Error|Traceback|line [0-9]" >> renders/preview.log
done
echo "PREVIEWS DONE" >> renders/preview.log
