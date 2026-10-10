#!/usr/bin/env python3
"""Build a review page that groups a diff by intent.

  review_page.py hunks <diff>           list every hunk id, to plan the groups
  review_page.py build <diff> <plan>    write the page (to -o, default review.html)

<diff> is a unified diff file (`git diff --no-color -U3 base...head > change.diff`),
or `-` for stdin. <plan> is the JSON file described in references/plan.md.
Standard library only, Python 3.9+.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@ ?(.*)$")


# ---------------------------------------------------------------- parse


def parse_diff(text):
    """Return a list of files, each with its hunks and line-level rows.

    Inside a hunk, the counts in its @@ header say how many lines belong to it,
    so a removed line that starts with "--" is never mistaken for a file header.
    """
    files = []
    current = hunk = None
    old_ln = new_ln = old_left = new_left = 0

    def strip_prefix(path, prefix):
        path = path.split("\t")[0]
        return None if path == "/dev/null" else re.sub(rf"^{prefix}/", "", path)

    for line in text.splitlines():
        in_hunk = hunk is not None and (old_left > 0 or new_left > 0)
        if in_hunk:
            mark, body = line[:1], line[1:]
            if mark == "+":
                hunk["rows"].append(("add", None, new_ln, body))
                hunk["add"] += 1
                new_ln += 1
                new_left -= 1
            elif mark == "-":
                hunk["rows"].append(("del", old_ln, None, body))
                hunk["del"] += 1
                old_ln += 1
                old_left -= 1
            elif mark == "\\":
                hunk["rows"].append(("note", None, None, line))
            else:  # context; a blank line is context whose leading space was trimmed
                hunk["rows"].append(("ctx", old_ln, new_ln, body))
                old_ln += 1
                new_ln += 1
                old_left -= 1
                new_left -= 1
            continue
        if line.startswith("\\") and hunk is not None:
            hunk["rows"].append(("note", None, None, line))
            continue

        if line.startswith("diff --git "):
            m = re.match(r"diff --git a/(.*) b/(.*)$", line)
            old, new = m.groups() if m else (None, None)
            current = {"old": old, "new": new, "status": "modified", "hunks": [], "binary": False}
            files.append(current)
            hunk = None
            continue
        if line.startswith("--- ") and (current is None or current["hunks"]):
            # A plain `diff -u` with no `diff --git` line between files.
            current = {"old": None, "new": None, "status": "modified", "hunks": [], "binary": False}
            files.append(current)
            hunk = None
        if current is None:
            continue

        m = HUNK_RE.match(line)
        if m:
            old_ln, new_ln = int(m.group(1)), int(m.group(3))
            old_left = int(m.group(2)) if m.group(2) is not None else 1
            new_left = int(m.group(4)) if m.group(4) is not None else 1
            hunk = {"header": m.group(5), "rows": [], "add": 0, "del": 0}
            current["hunks"].append(hunk)
        elif line.startswith("new file mode"):
            current["status"] = "added"
        elif line.startswith("deleted file mode"):
            current["status"] = "deleted"
        elif line.startswith("rename from "):
            current["status"] = "renamed"
            current["old"] = line[len("rename from "):]
        elif line.startswith("rename to "):
            current["new"] = line[len("rename to "):]
        elif line.startswith(("Binary files ", "GIT binary patch")):
            current["binary"] = True
        elif line.startswith("--- "):
            current["old"] = strip_prefix(line[4:], "a")
            if current["old"] is None:
                current["status"] = "added"
        elif line.startswith("+++ "):
            current["new"] = strip_prefix(line[4:], "b")
            if current["new"] is None:
                current["status"] = "deleted"

    for f in files:
        f["path"] = f["new"] or f["old"] or "unknown"
    return files


def hunk_ids(files):
    """Map 'path:N' (1-based) to (file, hunk). Binary or empty files get 'path:1'."""
    ids = {}
    for f in files:
        if not f["hunks"]:
            ids[f"{f['path']}:1"] = (f, None)
        for i, h in enumerate(f["hunks"], 1):
            ids[f"{f['path']}:{i}"] = (f, h)
    return ids


# ---------------------------------------------------------------- render

esc = html.escape


def counts_html(add, dele):
    return f'<span class="counts"><span class="a">+{add}</span> <span class="d">−{dele}</span></span>'


def render_hunk(f, h):
    if h is None:
        what = "Binary file" if f["binary"] else "No textual change"
        return f'<p class="empty">{what} ({esc(f["status"])})</p>'
    rows = [
        f'<tr class="hunk"><td class="ln"></td><td class="ln"></td>'
        f'<td class="code">@@ {esc(h["header"])}</td></tr>'
    ]
    for kind, o, n, body in h["rows"]:
        if kind == "note":
            rows.append(f'<tr class="hunk"><td class="ln"></td><td class="ln"></td><td class="code">{esc(body)}</td></tr>')
            continue
        mark = {"add": "+", "del": "−", "ctx": " "}[kind]
        cls = "" if kind == "ctx" else f' class="{kind}"'
        rows.append(
            f'<tr{cls}><td class="ln">{o or ""}</td><td class="ln">{n or ""}</td>'
            f'<td class="code"><span class="mk">{mark}</span>{esc(body)}</td></tr>'
        )
    return '<div class="diff-wrap"><table class="diff">' + "\n".join(rows) + "</table></div>"


def file_label(f):
    path = esc(f["path"])
    if f["status"] == "renamed":
        return f'{esc(f["old"])} → {path}'
    return path


def build(files, plan):
    ids = hunk_ids(files)
    seen = {}
    groups = plan.get("groups") or []
    if not groups:
        sys.exit("plan has no groups")

    errors = []
    resolved = []
    for g in groups:
        picked = []
        for ref in g.get("hunks", []):
            # A bare path takes every hunk of that file.
            keys = [ref] if ref in ids else [k for k in ids if k.rsplit(":", 1)[0] == ref]
            if not keys:
                errors.append(f"group {g.get('id')!r}: no hunk or file {ref!r}")
            for k in keys:
                if k in seen:
                    errors.append(f"{k} is in both {seen[k]!r} and {g.get('id')!r}")
                seen[k] = g.get("id")
                picked.append(k)
        resolved.append((g, picked))
    missing = [k for k in ids if k not in seen]
    if missing:
        errors.append("hunks in no group (every change must be shown):\n  " + "\n  ".join(missing))
    if errors:
        sys.exit("plan does not match the diff:\n" + "\n".join(errors))

    nav, sections = [], []
    total_add = total_del = 0
    for n, (g, picked) in enumerate(resolved, 1):
        gid = re.sub(r"[^a-z0-9-]", "-", str(g.get("id") or f"change-{n}").lower())
        add = sum(ids[k][1]["add"] for k in picked if ids[k][1])
        dele = sum(ids[k][1]["del"] for k in picked if ids[k][1])
        total_add += add
        total_del += dele
        summary = g.get("summary", "")
        nav.append(
            f'<li><a href="#{gid}"><span class="nav-n">{n}</span>'
            f'<span class="nav-body"><span class="nav-title">{esc(g["title"])}</span>'
            + (f'<span class="nav-sum">{esc(summary)}</span>' if summary else "")
            + f"{counts_html(add, dele)}</span></a></li>"
        )

        # Keep the plan's order, but show each file's path once per run of its hunks.
        body, last_path = [], None
        for k in picked:
            f, h = ids[k]
            if f["path"] != last_path:
                body.append(
                    f'<div class="file-meta"><code class="path">{file_label(f)}</code>'
                    + (f'<span class="status">{esc(f["status"])}</span>' if f["status"] != "modified" else "")
                    + "</div>"
                )
                last_path = f["path"]
            body.append(render_hunk(f, h))
        diff_html = "\n".join(body)
        if g.get("collapsed"):
            diff_html = f"<details><summary>Show the diff</summary>{diff_html}</details>"

        sections.append(
            f'<section class="change" id="{gid}">'
            f'<header class="change-head"><span class="eyebrow">Change {n} of {len(resolved)}</span>'
            f'<h3>{esc(g["title"])}</h3>{counts_html(add, dele)}</header>'
            f'<div class="note">{g.get("note_html", "")}</div>{diff_html}</section>'
        )

    chips = []
    for c in plan.get("chips", []):
        text = esc(c["text"])
        if c.get("href"):
            text = f'<a href="{esc(c["href"])}">{text}</a>'
        tone = f' {c["tone"]}' if c.get("tone") in ("ok", "warn", "bad") else ""
        chips.append(f'<span class="chip{tone}">{text}</span>')
    chips.append(f'<span class="chip">{len(files)} files · +{total_add} −{total_del}</span>')

    page = TEMPLATE.read_text(encoding="utf-8")
    fills = {
        "TITLE": esc(plan["title"]),
        "EYEBROW": esc(plan.get("eyebrow", "Review")),
        "LEDE": plan.get("lede_html", ""),
        "CHIPS": "".join(chips),
        "CONTEXT": plan.get("context_html", ""),
        "CHANGES_INTRO": plan.get("changes_intro_html", ""),
        "NAV": "\n".join(nav),
        "CHANGES": "\n".join(sections),
    }
    for key, value in fills.items():
        page = page.replace("{{" + key + "}}", value)
    return page


# ---------------------------------------------------------------- cli


def read_diff(arg):
    return sys.stdin.read() if arg == "-" else Path(arg).read_text(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    h = sub.add_parser("hunks", help="list hunk ids with a preview of each")
    h.add_argument("diff")
    h.add_argument("--lines", type=int, default=4, help="changed lines to preview per hunk")
    b = sub.add_parser("build", help="render the page")
    b.add_argument("diff")
    b.add_argument("plan")
    b.add_argument("-o", "--out", default="review.html")
    args = ap.parse_args()

    files = parse_diff(read_diff(args.diff))
    if not files:
        sys.exit("no files found in the diff")

    if args.cmd == "hunks":
        for key, (f, hk) in hunk_ids(files).items():
            if hk is None:
                print(f"{key}  [{f['status']}{', binary' if f['binary'] else ''}]")
                continue
            print(f"{key}  +{hk['add']} -{hk['del']}  @@ {hk['header']}")
            changed = [r for r in hk["rows"] if r[0] in ("add", "del")][: args.lines]
            for kind, _, _, body in changed:
                print(f"    {'+' if kind == 'add' else '-'} {body[:110]}")
        return

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    Path(args.out).write_text(build(files, plan), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
