#!/usr/bin/env bash
# Renderiza o filme em blocos (retomável: pula blocos prontos) e junta no final.
cd "$(dirname "$0")/../remotion"
OUT=../renders/final/parts; mkdir -p $OUT; TOTAL=12540; STEP=600
for ((a=0; a<TOTAL; a+=STEP)); do
  b=$((a+STEP-1)); [ $b -ge $TOTAL ] && b=$((TOTAL-1)); p=$(printf "%s/part_%05d.mp4" $OUT $a)
  [ -f "$p" ] && continue
  npx remotion render OUltimoPouso "$p.tmp.mp4" --frames=$a-$b --concurrency=4 --log=error && mv "$p.tmp.mp4" "$p" && echo "PART $a-$b OK"
done
ls $OUT/part_*.mp4 | sed "s|^|file '$PWD/|;s|$|'|" > $OUT/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy ../renders/final/o-ultimo-pouso.mp4 && echo "FINAL DONE"
