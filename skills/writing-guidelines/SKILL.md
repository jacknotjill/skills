---
name: writing-guidelines
description: How to write anything a person reads, so it sounds like a sharp colleague rather than a machine. Use whenever you write or edit prose for people, such as docs, READMEs, PR descriptions, commit messages, review pages, reports, emails, UI copy, error messages and labels, and when you write prompts or skills for other agents (see references/prompting.md). Other skills that produce writing load this one.
---

# Writing guidelines

These guidelines cover any words a person reads: product copy, documentation,
READMEs, error messages, labels, commit messages, PR descriptions, reports, and
the prompts agents run on. Good writing sounds like a colleague who knows the
subject and respects your time. Bad writing sounds like it came off an assembly
line, and these days an assembly line usually sounds like an AI. The tells below
give the writer away and make the reading slower and less clear; avoiding them
is most of the job.

This file follows its own rules. If a line here breaks one, that's a bug.

When the reader is an agent (a prompt, a skill, a handbook, `--help` text), also
read [references/prompting.md](references/prompting.md).

## What good looks like

Write the way a sharp colleague explains something at a whiteboard: the point
first, plain words, active voice, and a real example where it helps. Aim for the
plain English of the UK government's GOV.UK, with room for the nuance the subject
needs. Plain English still has a person behind it, so keep the warmth a good
explanation carries.

One test covers most of it: read the line aloud. If you'd say it to a colleague
that way, it's probably good. If it sounds like a press release, a legal notice,
or vague-profound filler ("the solution is in the seam"), rewrite it.

## Lead with the point

The first sentence of a section or paragraph says what it's for or what to do. A
reader who stops there still gets the gist. Bury the point under a wind-up
("In order to understand X, it's important to first consider...") and you've made
the reader dig for it.

## Use plain, active words

A short checklist to run on your own draft:

- **Write in the active voice.** "You test the filtering steps" tells the reader
  whose job it is and keeps the sentence moving. "The filtering steps are
  tested" hides who does what.
- **Use plain words.** Pick the short word where it carries the meaning: "buy"
  over "purchase", "about" over "approximately", "help" over "facilitate", "use"
  over "utilise".
- **Say the literal thing.** Where a plain description exists, use it. A metaphor
  like "dynamic range" or "load-bearing nudge" reads as clever today and confuses
  the reader who copies it without the meaning.
- **Give the reason.** One clause of why turns an order into something the reader
  can act on with judgment: "Sample the early steps first, because a step that
  mislabels your reference cases will mislabel thousands of strangers too."
- **Frame it as what to do.** Describe the move you want. Positive guidance
  travels further than a pile of bans.

## Cut words that add length without meaning

Filler qualifiers: genuinely, truly, really, incredibly, very, deeply, simply,
just, actually, basically.

Vague superlatives: remarkable, invaluable, exciting, unique, amazing,
fantastic, powerful, seamless, robust.

These claim importance instead of showing it. "A remarkable opportunity" tells
the reader nothing; "20-person Series B building dev tools" tells them
everything.

## Drop the habits that read as machine-written

Each of these also makes the reading slower or vaguer, so dropping them helps
every reader, not only the ones sniffing for a robot.

- **The em-dash sandwich**, where a phrase sits between two dashes and a comma
  would carry it.
- **Throat-clearing openers**: "It's worth noting that...", "to be clear...",
  "in essence...", "let's dive in", "I hope this helps". Delete them and start
  with the content.
- **Aphorism openers**: "The X is the Y" lines that sound profound but say
  nothing concrete. State the concrete thing instead.
- **Pairing a claim with its opposite** ("fast, not slow"; "it's not just X,
  it's Y") more than once in a passage. State the thing you mean and move on.
- **The rule of three on autopilot**, where every list runs to exactly three
  items and every sentence stacks three adjectives. Use the number of items the
  point needs.
- **Reflexive hedging** ("may potentially", "it could be argued that") and
  reflexive enthusiasm ("Certainly!", "Great question!"). Say what you know, at
  the confidence you actually hold.
- **Formatting as a substitute for thought**: bolding half a paragraph, turning
  every prose passage into bullets, or capping a section with a tidy summary the
  reader didn't need. Reach for structure when it earns its place.

Style is contagious. Copy full of filler trains the next reader, and the next
writer, to produce more of it, so the words you pick set the tone for everything
that follows.

## Say it once, in the right place

The same idea often shows up in a heading, a tooltip, a doc, a `--help` line, and
an error message. Write the full version once, where the reader will meet it
first, and let the other places point back with a short label. Repeating the full
text in five places means five copies to keep in sync, and they drift.

## Learn from examples

An example teaches the voice faster than a rule. Here's a rewrite that shows the
difference.

Before:

> Pick one canonical surface to carry the dynamic range; let the others just name
> the slot. A good slot name is usually the load-bearing nudge.

After:

> Write the full version once, where the reader will meet it. Everywhere else,
> use a short label that points back to it.

---

The best writing reads like a clear explanation from one person to another.
