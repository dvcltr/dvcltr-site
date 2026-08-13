#!/usr/bin/env bash
set -euo pipefail

cd /home/dvcltr/dvcltr-site

# Keep local repo current before creating weekly draft branches.
git fetch origin >/dev/null
git checkout main >/dev/null
git pull --ff-only origin main >/dev/null

export STATUS_COURSE_QUERY="${STATUS_COURSE_QUERY:-}"
export STATUS_LOOKBACK_DAYS="${STATUS_LOOKBACK_DAYS:-7}"
export STATUS_LOOKAHEAD_DAYS="${STATUS_LOOKAHEAD_DAYS:-7}"
export STATUS_CREATE_EMPTY="${STATUS_CREATE_EMPTY:-false}"

python3 scripts/canvas_weekly_status.py --pr
