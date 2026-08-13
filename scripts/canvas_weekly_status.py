#!/usr/bin/env python3
"""Create a privacy-safe weekly Canvas status post and GitHub PR.

Required environment:
  CANVAS_BASE_URL
  CANVAS_API_KEY

Optional environment:
  STATUS_LOOKBACK_DAYS=7
  STATUS_LOOKAHEAD_DAYS=7
  STATUS_COURSE_QUERY=          # optional substring, e.g. CYBR-508
  STATUS_CREATE_EMPTY=false     # when false, --pr stays quiet if no Canvas activity
  STATUS_AUTHOR_NAME=Hermes Agent
  STATUS_AUTHOR_EMAIL=hermes-agent@users.noreply.github.com

Modes:
  --dry-run   Print generated Markdown; do not write/commit/push.
  --write     Write Markdown only; do not create PR.
  --pr        Write Markdown, create branch, commit, push, and open PR.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "src" / "content" / "status"
PACIFIC = ZoneInfo("America/Los_Angeles")

@dataclass
class AssignmentItem:
    course_code: str
    course_name: str
    name: str
    status: str
    due_at: dt.datetime | None
    submitted_at: dt.datetime | None
    graded_at: dt.datetime | None


def die(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def parse_canvas_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(PACIFIC)


def canvas_get(path: str, params: dict | None = None):
    base = os.environ.get("CANVAS_BASE_URL", "").rstrip("/")
    token = os.environ.get("CANVAS_API_KEY")
    if not base or not token:
        die("CANVAS_BASE_URL and CANVAS_API_KEY must be set in the environment")

    url = base + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "dvcltr-weekly-status-generator",
    }

    out = []
    while url:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if not isinstance(data, list):
                return data
            out.extend(data)
            link = resp.headers.get("Link", "")
        next_url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                next_url = part[part.find("<") + 1 : part.find(">")]
                break
        url = next_url
    return out


def safe_course_code(course: dict) -> str:
    code = course.get("course_code") or course.get("name") or "Course"
    m = re.search(r"[A-Z]{2,5}[- ]?\d{3}", code.upper())
    return m.group(0).replace(" ", "-") if m else str(code).split()[0][:20]


def normalize_topic(name: str) -> tuple[str, str, str, str]:
    """Return safe title, focus, summary, takeaway without private details."""
    n = re.sub(r"^(Assignment|Discussion|Learning Activity)\s+\d+(\.\d+)?:\s*", "", name, flags=re.I).strip()
    low = n.lower()

    rules = [
        (("wargame", "bandit", "natas"), "Wargame Practice", "Hands-On Security Practice", "Continued wargame-based exercises to reinforce command-line, web, and security problem-solving habits.", "Repeated practice builds a more reliable workflow for careful enumeration and troubleshooting."),
        (("snort", "intrusion"), "Intrusion Detection Lab", "Intrusion Detection / Network Monitoring", "Worked with intrusion detection concepts and how monitoring tools help identify suspicious activity.", "Detection tools help turn network activity into signals defenders can investigate."),
        (("wazuh", "system monitoring"), "System Monitoring Setup", "Security Monitoring / SIEM Concepts", "Practiced centralized system monitoring concepts using defensive security tooling.", "Centralized monitoring supports alert review, investigation, and response."),
        (("vpn client monitoring",), "VPN Client Monitoring Project", "VPN Monitoring / Secure Access", "Worked on monitoring VPN client activity and documenting a secure-access setup.", "VPN security depends on visibility, logging, and clear reporting, not just encrypted access."),
        (("vpn", "pivpn", "pi-hole"), "VPN Setup Practice", "Secure Remote Access / VPN Concepts", "Practiced VPN setup concepts and secure remote access design in a lab context.", "Remote access tools need careful configuration, monitoring, and documentation."),
        (("syn flood",), "Docker-Based Traffic Simulation", "Transport Layer / Defensive Awareness", "Used a controlled lab environment to study transport-layer traffic behavior.", "Safe simulations make network attack patterns easier to understand defensively."),
        (("ping flood",), "Docker-Based Network Traffic Lab", "Network Simulation / Defensive Awareness", "Used a controlled Docker lab to study network traffic behavior and defensive implications.", "Containerized labs are useful for safely practicing network security concepts."),
        (("subnetting", "nat"), "Subnetting and NAT Practice", "IP Addressing / Network Design", "Practiced subnetting and NAT as core pieces of network structure.", "Addressing, segmentation, and traffic flow are security-relevant design choices."),
        (("layer 2", "data link"), "Layer 2 Security Analysis", "Data Link Layer / Defensive Controls", "Reviewed how lower-layer network protections can reduce exposure to common threats.", "Security weaknesses lower in the stack can affect the whole environment."),
        (("layer 1", "physical"), "Physical and Data Link Layer Security", "Layered Network Defense", "Reviewed lower-layer security risks and controls at a high level.", "Defensive controls work best when matched to the layer where risk appears."),
        (("osi",), "OSI Security Concepts", "Security Foundations / Networking", "Connected layered networking concepts with cybersecurity practice.", "Layered models help organize how risks and controls fit together."),
        (("ai in cybersecurity", "ai"), "AI and Cybersecurity Discussion", "Emerging Technology / Security Concepts", "Reviewed AI-related cybersecurity considerations at a high level.", "New technologies need both practical use cases and careful risk thinking."),
        (("zero trust", "blockchain"), "Zero Trust and Blockchain Security Discussion", "Security Architecture / Emerging Technology", "Reviewed Zero Trust and blockchain-related cybersecurity concepts at a high level.", "Security architecture requires balancing current systems, future tools, and practical limits."),
        (("hacker", "defender"), "Attacker and Defender Next Steps", "Security Operations / Threat Thinking", "Compared offensive and defensive next steps at a high level.", "Defensive planning improves when analysts think ahead about likely follow-on activity."),
        (("glossary",), "Module Glossary", "Technical Vocabulary", "Built course vocabulary around secure network engineering concepts.", "Clear vocabulary makes technical analysis and reporting more precise."),
    ]
    for needles, title, focus, summary, takeaway in rules:
        if any(x in low for x in needles):
            return title, focus, summary, takeaway

    cleaned = re.sub(r"\s+", " ", n)
    if len(cleaned) > 58 or "(" in cleaned:
        cleaned = "Course Project or Discussion"
    return cleaned, "Secure Network Engineering", "Worked on a course activity related to secure network engineering.", "Technical practice helps connect networking concepts to defensive security work."


def fetch_items(now: dt.datetime, lookback_days: int, lookahead_days: int, course_query: str | None) -> tuple[list[AssignmentItem], list[AssignmentItem]]:
    # Smoke test without printing identity details.
    canvas_get("/api/v1/users/self")

    courses = []
    for state in ("active", "completed"):
        try:
            courses.extend(canvas_get("/api/v1/courses", {"enrollment_state": state, "include[]": ["term"], "per_page": 100}))
        except Exception:
            continue

    seen = {c.get("id"): c for c in courses if c.get("id")}
    selected = []
    for c in seen.values():
        text = " ".join(str(c.get(k, "")) for k in ("name", "course_code", "original_name")).lower()
        if course_query and course_query.lower() not in text:
            continue
        if c.get("workflow_state") not in ("available", "completed"):
            continue
        selected.append(c)

    if not selected:
        die("No matching Canvas courses found")

    start = now - dt.timedelta(days=lookback_days)
    end = now
    upcoming_end = now + dt.timedelta(days=lookahead_days)
    completed: list[AssignmentItem] = []
    upcoming: list[AssignmentItem] = []

    for course in selected:
        assignments = canvas_get(f"/api/v1/courses/{course['id']}/assignments", {"include[]": ["submission"], "order_by": "due_at", "per_page": 100})
        code = safe_course_code(course)
        cname = course.get("name") or code
        for a in assignments:
            sub = a.get("submission") or {}
            due = parse_canvas_time(a.get("due_at"))
            submitted = parse_canvas_time(sub.get("submitted_at"))
            graded = parse_canvas_time(sub.get("graded_at"))
            state = sub.get("workflow_state") or "unsubmitted"
            status = "COMPLETED" if state == "graded" or submitted or state == "submitted" else "UPCOMING"
            item = AssignmentItem(code, cname, a.get("name") or "Course activity", status, due, submitted, graded)
            # Prefer the student's submission date for public progress. Only fall
            # back to graded/due date when no submission timestamp is available;
            # otherwise old work can reappear weeks later when grades post.
            activity_date = submitted or graded or due
            if status == "COMPLETED" and activity_date and start <= activity_date <= end:
                completed.append(item)
            elif status == "UPCOMING" and due and now <= due <= upcoming_end:
                upcoming.append(item)

    completed.sort(key=lambda x: (x.submitted_at or x.graded_at or x.due_at or now, x.name))
    upcoming.sort(key=lambda x: (x.due_at or upcoming_end, x.name))
    return completed, upcoming


def tags_for(items: list[AssignmentItem]) -> list[str]:
    tags = []
    joined = " ".join(i.name.lower() for i in items)
    mapping = [
        ("wargame", "Wargames"), ("bandit", "Wargames"), ("natas", "Wargames"),
        ("snort", "Snort"), ("wazuh", "Wazuh"), ("vpn", "VPN"),
        ("zero trust", "Zero Trust"), ("docker", "Docker"), ("subnet", "Subnetting"),
        ("nat", "NAT"), ("intrusion", "Intrusion Detection"),
    ]
    for key, tag in mapping:
        if key in joined and tag not in tags:
            tags.append(tag)
    codes = []
    for i in items:
        if i.course_code not in codes:
            codes.append(i.course_code)
    return (codes + tags)[:6] or ["School Progress"]


def generate_markdown(now: dt.datetime, completed: list[AssignmentItem], upcoming: list[AssignmentItem]) -> tuple[str, str]:
    start = (now - dt.timedelta(days=int(os.environ.get("STATUS_LOOKBACK_DAYS", "7")))).date()
    end = now.date()
    date_range = f"{start.strftime('%B')} {start.day}–{end.day}, {end.year}" if start.month == end.month else f"{start.strftime('%B')} {start.day}–{end.strftime('%B')} {end.day}, {end.year}"
    title = f"Weekly Status: {date_range}"
    slug = f"{end.isoformat()}-weekly-status"

    visible_items = completed[:6]
    tags = tags_for(visible_items)
    course = ", ".join(dict.fromkeys(i.course_code for i in visible_items)) if visible_items else "School Progress"
    summary = "A public progress update covering recent coursework, labs, projects, and learning themes."
    if visible_items:
        topics = ", ".join(tags[1:4] if len(tags) > 1 else tags[:3])
        summary = f"A public progress update covering recent coursework and learning themes{f' in {topics}' if topics else ''}."

    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {end.isoformat()}",
        f"course: {json.dumps(course, ensure_ascii=False)}",
        f"summary: {json.dumps(summary, ensure_ascii=False)}",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        "draft: false",
        "---",
        "",
        "This week’s progress update covers projects completed, labs practiced, and what I am learning next.",
        "",
        "## Completed this week",
        "",
    ]

    if visible_items:
        seen = set()
        for item in visible_items:
            _title, focus, _summary, _takeaway = normalize_topic(item.name)
            bullet = f"- {item.status.title()} work related to {focus.lower()}."
            if bullet not in seen:
                lines.append(bullet)
                seen.add(bullet)
    else:
        lines.append("- No new submitted Canvas work was found in the selected weekly window.")
        lines.append("- Continued reviewing course concepts and preparing for upcoming work.")

    lines += ["", "## Projects", ""]
    if visible_items:
        used_titles = {}
        for item in visible_items:
            title2, focus, summ, takeaway = normalize_topic(item.name)
            used_titles[title2] = used_titles.get(title2, 0) + 1
            display = title2 if used_titles[title2] == 1 else f"{title2} #{used_titles[title2]}"
            lines += [
                f"### {display}",
                f"**Focus:** {focus}",
                "",
                f"**Summary:** {summ}",
                "",
                f"**What I learned:** {takeaway}",
                "",
            ]
    else:
        lines += [
            "### Course Review",
            "**Focus:** Continued Learning",
            "",
            "**Summary:** Reviewed course material and prepared for the next set of assignments.",
            "",
            "**What I learned:** Consistency matters when building technical skills over time.",
            "",
        ]

    learning = []
    for item in visible_items:
        _, focus, _, _ = normalize_topic(item.name)
        for part in re.split(r"/| and ", focus):
            part = part.strip()
            if part and part not in learning:
                learning.append(part)
    if not learning:
        learning = ["Cybersecurity coursework", "Technical documentation", "Project-based learning"]

    lines += ["## Currently learning", ""]
    lines += [f"- {x}" for x in learning[:7]]

    lines += [
        "",
        "## Biggest takeaway",
        "",
        "The biggest takeaway this week was that steady hands-on practice helps connect course concepts to practical cybersecurity skills.",
        "",
        "## Next focus",
        "",
    ]
    if upcoming:
        for item in upcoming[:4]:
            title2, focus, _, _ = normalize_topic(item.name)
            lines.append(f"- Prepare for {title2.lower()} ({focus.lower()}).")
    else:
        lines += ["- Review feedback as it becomes available.", "- Continue building portfolio-ready summaries of school projects.", "- Keep practicing defensive security tools and technical documentation."]
    lines.append("")
    return slug, "\n".join(lines)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def create_pr(slug: str, md: str) -> None:
    path = POSTS_DIR / f"{slug}.md"
    branch = f"status/{slug}"

    run(["git", "config", "user.name", os.environ.get("STATUS_AUTHOR_NAME", "Hermes Agent")])
    run(["git", "config", "user.email", os.environ.get("STATUS_AUTHOR_EMAIL", "hermes-agent@users.noreply.github.com")])
    run(["git", "fetch", "origin"])
    run(["git", "checkout", "main"])
    run(["git", "pull", "--ff-only", "origin", "main"])

    if path.exists():
        print(f"Post already exists: {path.relative_to(ROOT)}")
        return

    existing = run(["git", "ls-remote", "--heads", "origin", branch], check=False).stdout.strip()
    if existing:
        print(f"Branch already exists: {branch}; not creating a duplicate PR")
        return

    run(["git", "checkout", "-b", branch])
    path.write_text(md, encoding="utf-8")
    run(["npm", "run", "build"])
    run(["git", "add", str(path.relative_to(ROOT))])
    run(["git", "commit", "-m", f"docs: add weekly status for {slug[:10]}"])
    run(["git", "push", "-u", "origin", branch])
    body = textwrap.dedent(f"""
    ## Summary
    - Adds a privacy-safe weekly Canvas status draft for `{slug}`
    - Keeps grades, scores, Canvas URLs, private comments, and instructor details out of the post

    ## Review checklist
    - [ ] The post does not include private details
    - [ ] The project/lab names are comfortable to publish
    - [ ] The takeaway sounds accurate
    - [ ] Merge only when ready to publish to Vercel
    """).strip()
    pr = run(["gh", "pr", "create", "--title", f"Weekly status draft for {slug[:10]}", "--body", body])
    print(pr.stdout.strip())


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--pr", action="store_true")
    ap.add_argument("--date", help="Override current date, YYYY-MM-DD, for testing")
    args = ap.parse_args()

    if args.date:
        now = dt.datetime.fromisoformat(args.date).replace(tzinfo=PACIFIC)
    else:
        now = dt.datetime.now(PACIFIC)
    lookback = int(os.environ.get("STATUS_LOOKBACK_DAYS", "7"))
    lookahead = int(os.environ.get("STATUS_LOOKAHEAD_DAYS", "7"))
    course_query = os.environ.get("STATUS_COURSE_QUERY") or None

    completed, upcoming = fetch_items(now, lookback, lookahead, course_query)
    slug, md = generate_markdown(now, completed, upcoming)

    if args.dry_run:
        print(md)
        print(f"\n<!-- completed_items={len(completed)} upcoming_items={len(upcoming)} slug={slug} -->")
        return

    create_empty = os.environ.get("STATUS_CREATE_EMPTY", "false").lower() in {"1", "true", "yes"}
    if args.pr and not create_empty and not completed and not upcoming:
        # Stay silent so script-only cron jobs do not notify when there is no draft to review.
        return

    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    if args.write:
        path = POSTS_DIR / f"{slug}.md"
        if path.exists():
            die(f"Post already exists: {path}")
        path.write_text(md, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
        return

    create_pr(slug, md)


if __name__ == "__main__":
    main()
