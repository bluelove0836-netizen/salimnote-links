#!/bin/zsh
set -euo pipefail

repo="/Users/sso/orca/projects/salimnote-links"
lock="/tmp/salimnote-links-sync.lock"
if ! mkdir "$lock" 2>/dev/null; then
  echo "Salimnote link sync already running"
  exit 0
fi
trap 'rmdir "$lock"' EXIT

cd "$repo"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Salimnote link repo has uncommitted changes; skipping automatic deployment" >&2
  exit 1
fi
git pull --ff-only origin main
python3 scripts/sync_approved_reels.py
git add manual-products.json assets/coupang-*-thumbnail.jpg
if git diff --cached --quiet; then
  echo "No approved product changes"
  exit 0
fi
git commit -m "Sync cloud-reviewed Salimnote products"
git push origin main
