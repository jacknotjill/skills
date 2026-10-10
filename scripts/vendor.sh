#!/usr/bin/env bash
# Copy third-party skills from their upstream repos, unchanged.
#
#   scripts/vendor.sh            refresh every skill to the commit pinned below
#   scripts/vendor.sh latest     refresh to each repo's default branch, then
#                                update the pins below and THIRD_PARTY.md
#
# Each line: skill name, upstream repo, pinned commit, path to the skill in it.
set -euo pipefail

SKILLS=(
  "show-me     humanlayer/skills  653b641  plugins/show-me/skills/show-me"
  "visual-pr   humanlayer/skills  653b641  plugins/visual-pr/skills/visual-pr"
  "grilling    mattpocock/skills  49dd158  skills/productivity/grilling"
  "grill-me    mattpocock/skills  49dd158  skills/productivity/grill-me"
)

root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

for line in "${SKILLS[@]}"; do
  read -r name repo commit path <<<"$line"
  clone="$work/${repo//\//-}"
  if [ ! -d "$clone" ]; then
    git clone -q "https://github.com/$repo" "$clone"
  fi
  if [ "${1:-}" != "latest" ]; then
    git -C "$clone" checkout -q "$commit"
  fi
  rm -rf "${root:?}/skills/$name"
  cp -R "$clone/$path" "$root/skills/$name"
  cp "$clone/LICENSE" "$root/skills/$name/LICENSE"
  echo "$name  <-  $repo@$(git -C "$clone" rev-parse --short HEAD):$path"
done
