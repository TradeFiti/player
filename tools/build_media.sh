#!/usr/bin/env bash
# Builds lightweight derivatives of the original media. Originals are never modified.
#   assets/posters/highlight-NN.jpg  poster frame taken from each clip at 40% of its duration
#   assets/images/thumbs/*.jpg       grid thumbnails, longest edge 900px
#   assets/images/web/*.jpg          hero-sized copies of the three 3024x4032 portraits, longest edge 1600px
# Requires ffmpeg and ffprobe. Re-run after adding or replacing media, then run tools/generate.py.
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p assets/posters assets/images/thumbs assets/images/web

resize() { # src dest longest-edge ffmpeg-qscale (2 = best, 31 = worst)
  ffmpeg -v error -y -i "$1" -vf "scale='if(gt(iw,ih),min($3,iw),-2)':'if(gt(iw,ih),-2,min($3,ih))'" -q:v "$4" "$2"
}

for f in assets/videos/highlight-*.mp4; do
  n=$(basename "$f" .mp4)
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  t=$(python3 -c "print(round($d*0.4, 2))")
  ffmpeg -v error -y -ss "$t" -i "$f" -frames:v 1 -vf "scale='if(gt(iw,ih),960,-2)':'if(gt(iw,ih),-2,960)'" -q:v 5 "assets/posters/$n.jpg"
done

for f in assets/images/*.jpeg assets/images/*.jpg; do
  case "$f" in *cambrils-instagram*|*trial-certificate-2*|*stats-twofeet*) continue;; esac
  b=$(basename "$f"); b="${b%.*}.jpg"
  resize "$f" "assets/images/thumbs/$b" 900 7
done

for n in hero-portrait portrait-1 portrait-2; do
  resize "assets/images/$n.jpeg" "assets/images/web/$n.jpg" 1600 5
done
