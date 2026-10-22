# Jotihunt skill

An agent skill for the [Jotihunt](https://www.jotihunt.nl), the yearly fox hunt of Scouting Gelderland (the Netherlands). Every hour the organisers publish a cryptic hint per fox team; decoding it yields the team's location, usually as a Dutch RD (Rijksdriehoek) grid coordinate. This skill gives Claude Code (or another agent that supports skills) the puzzle knowledge to coach your team through those hints.

## Install

```bash
npx skills add ScoutingIJsselgroep/jotihunt-skill        # in a project: .claude/skills/jotihunt-hints
npx skills add ScoutingIJsselgroep/jotihunt-skill -g     # for your user: ~/.claude/skills/jotihunt-hints
```

Or copy `skills/jotihunt-hints/` into `.claude/skills/` yourself.

Then ask about a hint, for example "help met deze Jotihunt-hint, eerst alleen de richting", and paste the hint text or attachments.

## Puzzling should stay fun

The skill coaches instead of taking over. It answers in phases and lets you choose how much help you want:

1. **Direction**: the likely puzzle type, why, a quick check you can do yourself, and links to tools.
2. **Steps**: how to read it, one team worked out in full, then the others.
3. **Answer**: the coordinate per team, with how certain it is.

AI is good at recognising the puzzle type and at the computation, but its answers are often slightly off while sounding certain. Always check: is the coordinate in the team's area, and close to the team's previous position?

## Contents

| Path | Purpose |
|---|---|
| `skills/jotihunt-hints/SKILL.md` | The knowledge base (in Dutch, like the game): method, catalogue of the 2023–2026 hints with solution methods, recognition guide, code tables (KIX, Kenny, Hexahue, 7-segment, resistor colours, Gaelic numbers), public-transport tips, pitfalls |
| `skills/jotihunt-hints/scripts/jh.py` | Decoders and helpers: RD ↔ WGS84, projection, Kenny, 7-segment, Caesar, letter values, binary, image diffs, anagrams. Python 3 standard library; `python3 scripts/jh.py --help` |
| `skills/jotihunt-hints/scripts/toollinks.json` | Links to online tools (dCode, geocaching code tables, what3words, PDOK, …) |
| `skills/jotihunt-hints/references/` | How AI coaching did on the 2023, 2024 and 2026 hints, compared with the official explanations |

## Sources

- Game API: `https://www.jotihunt.nl/api/2.0/articles` (public, 30 requests per minute); earlier editions on `2025.jotihunt.nl` and the Wayback Machine.
- Code tables: [geocachen.be](https://geocachen.be/geocaching/geocache-puzzels-oplossen/geocaching-code-tabellen/), [dCode](https://www.dcode.fr/).
