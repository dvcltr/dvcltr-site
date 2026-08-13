---
title: "Project Status: Site structure and publishing workflow"
date: 2026-08-13
project: "dvcltr.com"
summary: "Restructured the site direction around school progress and personal projects, added the technology stack, featured Cipherstone Lab, and tightened the GitHub-to-Vercel publishing workflow."
tags: ["dvcltr.com", "GitHub", "Vercel", "Astro", "Cipherstone Lab"]
draft: false
---

This personal project update covers the recent work turning `dvcltr.com` from a single school-progress page into a cleaner learning and project log.

## Completed this week

- Moved the site direction toward a hybrid structure: school progress on one side, personal projects on the other.
- Added a technology stack section with current lab hardware and important specs.
- Added a featured personal project card for Cipherstone Lab.
- Added separate project-status infrastructure so personal projects can have their own weekly-style updates.
- Continued using GitHub for version control and Vercel for production deployments.

## Site structure

The homepage is now meant to stay lighter. Instead of carrying every detail forever, it surfaces the newest school update and newest personal project update, then links deeper into the right archive.

Current structure:

```text
/
  Overview homepage

/status/
  School weekly status archive

/projects/
  Personal projects overview

/projects/status/
  Personal project status archive
```

## GitHub and Vercel workflow

The publishing flow is now straightforward:

```text
local edits → npm run build → git commit → git push → Vercel production deploy → live verification
```

That gives the site a reviewable history in GitHub while keeping the public site deployed from Vercel.

## Cipherstone Lab

Cipherstone Lab is now treated as a personal project instead of being mixed into the school update stream. The public site links to both the running app and the source repository.

## Next focus

- Keep the homepage concise.
- Add more detailed personal project pages as projects grow.
- Use `/projects/status/` for future project updates about Cipherstone Lab, site improvements, and home-lab changes.
