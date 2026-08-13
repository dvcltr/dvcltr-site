# dvcltr-site

Terminal-style school progress blog for dvcltr.com.

## Commands

```bash
npm run dev
npm run build
npm run preview
npm run status:dry-run
npm run status:pr
```

## Content

Weekly status posts live in:

```text
src/content/status/
```

Each post is Markdown with frontmatter:

```yaml
---
title: "Weekly Status: Month Day–Day, Year"
date: YYYY-MM-DD
course: "CYBR-508"
summary: "Short privacy-safe summary."
tags: ["Tag"]
draft: false
---
```

## Weekly Canvas draft automation

The script below creates a privacy-safe weekly status draft from Canvas:

```bash
python3 scripts/canvas_weekly_status.py --dry-run
python3 scripts/canvas_weekly_status.py --pr
```

Required environment variables:

```text
CANVAS_BASE_URL
CANVAS_API_KEY
```

Optional filters:

```text
STATUS_COURSE_QUERY=CYBR-508
STATUS_LOOKBACK_DAYS=7
STATUS_LOOKAHEAD_DAYS=7
STATUS_CREATE_EMPTY=false
```

The PR workflow keeps publishing manual-review first: the script writes a Markdown post on a new branch, runs `npm run build`, pushes the branch, and opens a GitHub pull request. Vercel publishes only after the PR is merged.
