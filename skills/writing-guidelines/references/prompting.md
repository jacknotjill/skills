# Prompting guidelines

These help you write prompts, skills and handbooks that read well and hold up
across different models and agents. Prompts are writing, so everything in
[../SKILL.md](../SKILL.md) applies first: lead with the point, plain active
voice, cut the filler, and drop the habits that read as machine-written. This
file covers what's specific to prompts on top of that.

Style is contagious in both directions. A prompt full of filler produces answers
full of filler, so the words you pick set the tone for everything the agent
writes back.

## The shape of a prompt

Move from broad to specific:

```
Context     The system the agent works in, who it serves, what it's there to do and why
Guidance    The details and judgment calls context won't settle
Examples    Concrete cases that show the behaviour you want
```

Keep step-by-step instructions thin. We use LLMs because they handle nuance and
edge cases on their own; the day you can spell out every step is the day you
write code instead. Reach for an example before a rule: it teaches the voice
faster and holds up better when a new model picks up the work.

**Context** sets the scene: the system the agent works in, who it serves, and
what it's there to do and why. An agent that knows why makes better calls when
the instructions run out.

**Guidance** fills the gaps context leaves: the clarifications, the calls that
matter, and the edge cases worth naming.

**Examples** show the behaviour you want in a concrete case, which lands more
reliably than describing it.

## Writing guidance

Guidance runs on a spectrum from information to instruction. Information hands
the agent something to reason with; an instruction tells it exactly what to do.
The more you give as information, the better the agent copes with cases you
didn't foresee, so reach for information first and save instructions for the
moments that allow no latitude.

- **An observation with evidence** is the most useful, and should be the most
  common. State what tends to work and let the agent weigh it: "Emails with four
  or five candidates, each with a one-line angle, roughly double the reply rate."
  It carries its own reason, so the agent can work out how far to trust it.
- **A stated preference** is a strong default that judgment can override. "Lead
  with the strongest candidate." The agent follows it most of the time and
  departs when the case calls for it.
- **A direct instruction** is the rarest, for cases with no room at all: safety,
  legal lines, irreversible actions, a format another system depends on.
  "Include the role title in every subject line." Say exactly what to do and
  leave no doubt.

Hard-coding a soft preference ("ALWAYS lead with the strongest candidate") makes
the agent rigid where judgment would serve it better. Stating a real constraint
as a vague preference means the agent drops it the moment things get unusual.

## Say it once, in the right place

The same idea often shows up in a system prompt, a handbook, a field name, a
`--help` line, and an error message. Write the full version once, where the agent
will read it, and let the other places point back with a short label.

The home for durable behaviour is almost always the system prompt, a skill or a
handbook: the context the agent carries into every session. When you find
yourself changing how an agent behaves by editing an error message or adding a
one-off pointer, look upstream. The real fix usually belongs there.

## Evolving prompts

When requirements change, rewrite rather than append. Sections bolted on over
time drift apart and start to repeat each other.

1. Reread the whole prompt with fresh eyes.
2. Ask how you'd write it from scratch for what you now know.
3. Merge related sections, drop guidance that no longer holds, and restructure
   for clarity.
4. Add a new section only when the content is separate.
