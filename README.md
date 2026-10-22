# Jotihunt skill

An agent skill for the [Jotihunt](https://www.jotihunt.nl), the yearly fox hunt of Scouting Gelderland (the Netherlands). Every hour the organisers publish a cryptic hint per fox team; decoding it yields the team's location, usually as a Dutch RD (Rijksdriehoek) grid coordinate. This skill gives Claude Code (or another agent that supports skills) the puzzle knowledge to coach your team through those hints.

Made by [Scouting IJsselgroep](https://github.com/ScoutingIJsselgroep). Not affiliated with the Jotihunt organisation or Scouting Gelderland.

## Install

```bash
npx skills add ScoutingIJsselgroep/jotihunt-skill        # in a project: .claude/skills/jotihunt-hints
npx skills add ScoutingIJsselgroep/jotihunt-skill -g     # for your user: ~/.claude/skills/jotihunt-hints
```

Or copy `skills/jotihunt-hints/` into `.claude/skills/` yourself.

Then ask about a hint, for example "help met deze Jotihunt-hint, eerst alleen de richting", and paste the hint text or attachments.

## Requirements

- **Python 3** for `scripts/jh.py`. Most commands (RD ↔ WGS84, projection, Kenny, 7-segment, Caesar, letter values, binary, anagrams) use only the standard library.
- **Optional**, for image commands (`imgdiff`, `verschillen`, `symbolen`): `pip install pillow numpy scipy opencv-python`.
- **Optional**, for speech in audio and video (`transcribeer`): `pip install transformers torch` and `ffmpeg`. The first run downloads Whisper large-v3-turbo; run it once with `HF_HUB_OFFLINE=0`, after that it works offline.
- ImageMagick and exiftool help with attachments but are not required.

## Puzzling should stay fun

The skill coaches instead of taking over. It answers in phases and lets you choose how much help you want:

1. **Direction**: the likely puzzle type, why, a quick check you can do yourself, and links to tools.
2. **Steps**: how to read it, one team worked out in full, then the others.
3. **Answer**: the coordinate per team, with how certain it is.

## How good is it?

AI is good at recognising the puzzle type and at the computation once the system is known. Its answers are often slightly off while sounding certain: a misread symbol or a wrong digit order gives a coordinate that looks just as convincing as a correct one. Always check whether the coordinate lies in the team's area and close to the team's previous position.

> **About the results in `references/`:** these are the AI's own assessment, not official scores. The organisers rarely publish coordinates, so "correct" there mostly means the AI judged an answer plausible after redoing it with the official method. Not everything marked correct was actually correct. For comparison: in 2026 our team scored **128 points for the hints**, while the AI evaluation of that edition counts 154 correct team answers. Read the numbers as an upper bound.

## Contents

| Path | Purpose |
|---|---|
| `skills/jotihunt-hints/SKILL.md` | The knowledge base (in Dutch, like the game): method, catalogue of the 2023–2026 hints with solution methods, recognition guide, code tables (KIX, Kenny, Hexahue, 7-segment, resistor colours, Gaelic numbers), public-transport tips, pitfalls |
| `skills/jotihunt-hints/scripts/jh.py` | Decoders and helpers; `python3 scripts/jh.py --help` |
| `skills/jotihunt-hints/scripts/toollinks.json` | Links to online tools (dCode, geocaching code tables, what3words, PDOK, …) |
| `skills/jotihunt-hints/references/` | How AI coaching did on the 2023, 2024 and 2026 hints (see the note above) |

## Contributing

Corrections and new editions are welcome as a pull request. Add a new edition's theme and hint catalogue to `SKILL.md`, and add a decoder to `jh.py` when a puzzle type keeps coming back. Keep the coaching principle: direction first, answers only when asked.

## Sources

- Game API: `https://www.jotihunt.nl/api/2.0/articles` (public, 30 requests per minute); earlier editions on `2025.jotihunt.nl` and the Wayback Machine.
- Code tables: [geocachen.be](https://geocachen.be/geocaching/geocache-puzzels-oplossen/geocaching-code-tabellen/), [dCode](https://www.dcode.fr/).
- Hint material and official explanations belong to the Jotihunt organisation; the catalogue only describes the methods.

## License

[MIT](LICENSE)
