---
name: review-artifact
description: Build a single-page HTML review of a code change (a PR, branch or diff) that a reviewer can read top to bottom. It opens with a short, well-structured introduction (the problem, the fix, the evidence, the decision), then shows every hunk of the diff grouped by what it is for, with those intents listed down the left instead of file names. Use when asked for a review page, review artifact, PR explainer or walkthrough of a change, or when handing a change to someone who hasn't followed the work.
---

# Review artifact

A review page answers what a reviewer needs, in the order they need it: what
was wrong, what this change does about it, how we know it works, and what they
have to decide. Then it shows the whole diff, organised by intent. The left-hand
list reads like the plan of the change ("Only one request renews the token",
"Somewhere to record the claim", "Regenerated files"), and each entry opens the
hunks that carry it out, wherever they live.

Reviewers who get the story first read the diff faster and catch more, because
they can check each hunk against the intent it claims to serve.

## Write it well

Everything on this page is writing for a person. Load the `writing-guidelines`
skill ([../writing-guidelines/SKILL.md](../writing-guidelines/SKILL.md)) and
follow it throughout. The reader is a capable engineer who hasn't followed the
work: name things the way the code does, explain any term the diff introduces,
and lead every section with its point.

## Steps

1. **Gather the facts.** Get the diff (`git diff --no-color base...head > change.diff`,
   or the PR's `.diff`), the PR description, linked issues, review comments, CI
   state on the head commit, and what was actually run to test it. Read the code
   around the hunks too, since a hunk rarely explains itself.

2. **Find the intents.** Run `python3 scripts/review_page.py hunks change.diff`
   and sort every hunk by what it's for. See "Grouping by intent" below.

3. **Write the introduction** (`lede_html` and `context_html`), following
   "The introduction" below.

4. **Write a note for each group.** Say what these lines change and why, and
   point at the line or decision a reviewer should look at hardest.

5. **Build it.** Write `plan.json` (format: [references/plan.md](references/plan.md)),
   then run `python3 scripts/review_page.py build change.diff plan.json -o review.html`.
   The build refuses a plan that leaves out a hunk or uses one twice, so the page
   always carries the full change. Fix what it lists and build again.

6. **Check it, then share it.** Open the page, read it as the reviewer would,
   and check it at phone width. If your environment can publish an HTML page
   (for example an Artifact tool), publish `review.html` there, keep it private
   unless told otherwise, and give the link. Otherwise hand over the file path.

## Grouping by intent

- **Title each group with its outcome**, in plain words: "Waiting requests
  reuse the new token", not "slack.ts" or "Refactor botToken". The optional
  `summary` line says how, in a few words.
- **Order the groups the way you'd explain the change**: the core behaviour
  first, then what it needs (schema, config, wiring), then how it's proved,
  then the mechanical rest.
- **Cross file boundaries freely.** A new column, its migration and the code
  that writes to it can be one intent. One file can feed three intents.
- **Put a test with the behaviour it proves.** Give tests their own group only
  when they stand alone, such as a new harness or a fixture rewrite.
- **Collapse the mechanical**: generated code, lockfiles, snapshots and pure
  renames go in a group with `"collapsed": true` and a one-line note on how they
  were produced.
- Most changes have three to eight intents. If you have one per file, you've
  sorted by file again; if you have one, the change may only need the intro.

## The introduction

The header holds the title, a one-paragraph `lede_html` and the chips (PR link,
commit, CI, draft state). The lede says what was wrong or missing, what the
change does, and what you're asking the reader to do. A reader who stops there
should know whether they need to read on.

Then `context_html` holds a few `<section class="block">` sections, each opening
with `<span class="eyebrow">` and an `<h2>` that states its point. Use the ones
the change needs, in this order:

| Section | What it answers |
| --- | --- |
| Where things stand | What's live, what isn't, and what's still needed outside the code. Use it for follow-ups and multi-PR work. |
| The problem | What went wrong or was missing, shown concretely: a trace, a timeline, a before-and-after table. |
| The fix | How the change works as a mechanism, with the numbers that matter and how it behaves in the edge cases. |
| For the reviewer | The points that need a reviewer's judgment, each tagged. |
| Evidence | What was run, before and after, and what was not covered. |
| Your call | Your recommendation (merge, change, close) and why, plus any steps after merge. |

Scale it to the change: a one-line fix might need only the lede and Evidence.
Every claim must be checkable from the diff, the PR or a command you ran. Never
report a test or check you didn't run; say what wasn't covered instead.

Classes the template styles for you:

- `ul.plain`, `ol.plain`: spaced lists.
- `<div class="table-wrap"><table class="grid">`: a table with a header row.
- `<div class="callout">`: one aside, such as "How likely is this?".
- `<div class="points">` containing `<div class="point"><span class="tag decide">Decide</span><div>…</div></div>`.
  Tags: `decide`, `risk`, `known`, `checked`.
- `<div class="numbers">` containing `<div class="num"><b>15 s</b><span>what it is</span></div>`:
  the constants that matter.
- `<pre class="code">`: a short excerpt or pseudo-code.
- `.chip.ok`, `.chip.warn`, `.chip.bad` (set by `tone` in the plan).

A small diagram helps where timing or state is the hard part. A table with one
column per actor and one row per moment usually beats a picture.

## Before you share

- Diffs can contain secrets, customer data or internal hostnames. Scan the
  hunks; if one carries something that shouldn't leave the repo, say so and
  don't publish.
- Match the page to the head commit you describe, and put that commit in a chip.
