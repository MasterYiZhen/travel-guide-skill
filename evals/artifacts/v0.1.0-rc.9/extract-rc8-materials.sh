#!/bin/sh
# 从历史提交 77ff55c（旧 rc.8，已在 main 上撤销）提取本轮复用的材料到指定目录（默认 ./rc8-materials）。
# 用法：sh evals/artifacts/v0.1.0-rc.9/extract-rc8-materials.sh [目标目录]
# 作者：yizhen
set -e
OUT="${1:-rc8-materials}"
COMMIT=77ff55cd16d2a0c484a289c2f0eaa06f2a01b580
P=evals/artifacts/v0.1.0-rc.8
mkdir -p "$OUT/travel-trial/images" "$OUT/travel-trial/references" "$OUT/travel-trial/sources" "$OUT/visual-fixtures"
for f in itinerary-proposal.md evidence-boundaries.md user-and-responses.md page-manifest.json; do
  git show "$COMMIT:$P/travel-trial/$f" > "$OUT/travel-trial/$f"
done
for f in page-01-v3 page-02-v2 page-03-v1 page-04-v2 page-05-v3; do
  git show "$COMMIT:$P/travel-trial/images/$f.png" > "$OUT/travel-trial/images/$f.png"
done
for f in $(git ls-tree -r --name-only "$COMMIT" -- "$P/travel-trial/references"); do
  git show "$COMMIT:$f" > "$OUT/travel-trial/references/$(basename "$f")"
done
git show "$COMMIT:$P/travel-trial/sources/index.json" > "$OUT/travel-trial/sources/index.json"
for f in brief.md sample-a.png sample-b.png sample-c.png; do
  git show "$COMMIT:$P/visual-fixtures/$f" > "$OUT/visual-fixtures/$f"
done
echo "extracted to $OUT"; (cd "$OUT" && find . -type f | sort | xargs shasum -a 256)
