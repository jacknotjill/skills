# Plan file

`scripts/review_page.py build <diff> plan.json` reads this JSON. Every hunk in
the diff must land in exactly one group, or the build stops and lists the
strays and duplicates.

```json
{
  "title": "Token Refresh Race",
  "eyebrow": "Review · Slack · follow-up to #231",
  "lede_html": "#231 made the bot renew its own Slack token every 12 hours. Review found that several requests renewing at once can leave us holding a token Slack has already cancelled. This PR makes one request do the renewal and the rest wait for it.",
  "chips": [
    {"text": "acme/app#232", "href": "https://github.com/acme/app/pull/232"},
    {"text": "@ 2aa4079"},
    {"text": "CI green", "tone": "ok"},
    {"text": "Draft · your call", "tone": "warn"}
  ],
  "context_html": "<section class=\"block\" id=\"problem\">…</section>",
  "changes_intro_html": "<p>Each change below says what it's for, then shows the hunks that do it. Diffs are against <code>main</code>.</p>",
  "groups": [
    {
      "id": "claim",
      "title": "Only one request renews the token",
      "summary": "Claim the row with a conditional UPDATE before calling Slack",
      "note_html": "<p>Everything that needs the token calls <code>botToken</code>, so the fix lives there…</p>",
      "hunks": ["src/slack/store.ts:1", "src/slack/store.ts:3"]
    },
    {
      "id": "column",
      "title": "Somewhere to record the claim",
      "summary": "A nullable timestamp column and its migration",
      "note_html": "<p>Additive and nullable, so the running code is unaffected.</p>",
      "hunks": ["db/schema.sql", "migrations/0042_refresh_claim.sql"]
    },
    {
      "id": "generated",
      "title": "Regenerated files",
      "summary": "Kysely types and the Atlas checksum",
      "note_html": "<p>Output of <code>make db-generate</code>; nothing written by hand.</p>",
      "hunks": ["src/db/types.generated.ts", "migrations/atlas.sum"],
      "collapsed": true
    }
  ]
}
```

## Fields

| Field | Required | What it is |
| --- | --- | --- |
| `title` | yes | Page title and `<h1>`. A name of two to five words for the change, not the PR title copied over. |
| `eyebrow` | no | Small line above the title: kind of page, area, related PRs. |
| `lede_html` | yes | One paragraph: what was wrong or missing, what this change does about it, and what the reader is being asked to do. Inline HTML only. |
| `chips` | no | Short facts: PR link, commit, CI state, draft state. `tone` is `ok`, `warn` or `bad`. A file and line-count chip is added for you. |
| `context_html` | yes | The introduction, as `<section class="block">` elements. See SKILL.md for the sections and the classes you can use. |
| `changes_intro_html` | no | A sentence or two above the change list. |
| `groups` | yes | The intents, in reading order. |
| `groups[].id` | yes | Anchor id, kebab-case. |
| `groups[].title` | yes | The intent, as an outcome: "Only one request renews the token", not "slack.ts". |
| `groups[].summary` | no | One line under the title in the left-hand list: how it's done. |
| `groups[].note_html` | yes | What this group changes and why, and anything the reviewer should check in these lines. |
| `groups[].hunks` | yes | Hunk ids from `review_page.py hunks`. A bare path takes every hunk of that file. Hunks show in the order you list them. |
| `groups[].collapsed` | no | `true` hides the diff behind a "Show the diff" toggle. Use it for generated files, lockfiles and snapshots. |

## Hunk ids

`review_page.py hunks change.diff` prints one line per hunk:

```
src/slack/store.ts:1  +13 -0  @@ export type SlackLinkedMember = Readonly<{
    + // Slack keeps at most two bot tokens live per refresh chain, so overlapping
    + // refreshes could revoke the one we store. One request per workspace, across
src/slack/store.ts:2  +59 -6  @@ export function createSlackStore(
```

The number after the colon is the hunk's position in that file, starting at 1.
A binary file, or a file whose only change is a rename or mode, has the single
id `path:1`.

If one hunk does two jobs, put it in the group it mostly serves and say in the
other group's note where the rest lives. To split hunks more finely, regenerate
the diff with less context (`git diff -U1`), which breaks large hunks apart.
