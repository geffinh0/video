#!/usr/bin/env bash
# Renderiza todas as sequências faciais (retomável). Log: renders/anim.log
cd "$(dirname "$0")/.."
python3 gen/anim.py s03 s06 s04 s05 s05_floor s02 2>&1 | grep --line-buffered -E "^s0|DONE|SKIP|Error|Trace|line [0-9]" >> renders/anim.log
echo "ANIM ALL DONE" >> renders/anim.log
