#!/usr/bin/env bash
# Render de todos os fundos e camadas (retomável). Log: renders/render.log
cd "$(dirname "$0")/.."
PLATES="s02 s03 s04 s05 s06 s07 s09 s10b s11 s12 s13 s14 s15 s16 s17 s17b s18 s19 s21 s23 s24 s25 s26 s27 s28 s29 s30 s31 s33 ins_key ins_candle ins_glass ins_shadow ins_hand"
LAYERS=""
for s in $PLATES; do
  [ -f renders/scenes/$s/plate.png ] && continue
  python3 blender/shots.py $s plate 2>&1 | grep -E "^TIME|Error|Traceback" >> renders/render.log
done
echo "PLATES DONE $(date)" >> renders/render.log
for s in $LAYERS; do
  python3 blender/shots.py $s layer 2>&1 | grep -E "^TIME|Error|Traceback" >> renders/render.log
done
echo "ALL DONE $(date)" >> renders/render.log
