# TODO

Planned work, open ideas and decisions. Update this file in the same PR as the work that
changes it.

## Open

### Features

- **Place by column**: pick a year and a week column, or "centre it", and let the tool work
  out the start Sunday.
- **Text**: render short text with a 5×7 pixel font.
- **Better "after" shades**: estimate the cap (the busiest day, minus outliers) from GitHub's
  real levels for the year instead of assuming the busiest day. Measurements so far: in most
  years the cap is the busiest day; in some, one or two top days are left out, with no
  consistent rule.
- **HTML/SVG preview** that looks like the real graph, next to the terminal one.
- **Pattern editor**: a small web page to draw a pattern on the grid with a live preview,
  then export it as a pattern file.

### Image import

- **Background threshold**: `BLANK_BELOW` (40) decides what counts as background. A setting
  would help pictures on off-white or busy backgrounds.
- **Colour instead of darkness**: light subjects (a white ghost) disappear today. Measuring
  the difference from the background colour, not darkness, would keep them.

### Parked

- **Clean old drawings**: remove the drawings in a date range. GitHub cannot subtract
  contributions, so this means removing commits from `main` and force-pushing, which the
  "never rewrite history" rule forbids today.
  - Cost: every later commit gets a new ID; files are unchanged; every clone needs a reset.
  - Shape: `make clean FROM=... TO=...`, later `make clean PATTERN=... START=...`. Only
    "Contribution" commits by the user's email; a snapshot-based rewrite; a now/after
    preview; confirmation before rewriting and before pushing; a mirror backup with the
    restore command; `--force-with-lease`; refuse while PRs are open.
  - Before starting: confirm the range holds only drawings, and measure how long GitHub
    takes to drop contributions after a force-push.

## Decisions

- **Drawings live in this repo, on `main`.** That is how they reach the graph; never
  rewrite or squash them. One repo per drawing (deleted to undo it) was considered and
  rejected (2026-10-26, 2026-11-08).
- **uv and a Makefile instead of Docker** (2026-10-26).
- **Terminal preview first**; HTML/SVG later (2026-10-26).
- **No "intensity by level"**: drawings go into quiet years, where the digits come out as
  drawn, so commit counts are not derived from real data (2026-11-03).
- **Patterns are solid silhouettes**, drawn from scratch rather than copied from other
  tools. Thin lines and sparse dots (heartbeat, wave, glider) read as noise on the graph
  (2026-11-11).

## Done in version 2

- Project setup: uv, ruff, pytest, a Makefile, LF line endings.
- `plan_commits`: pattern and start Sunday to (day, commits), shared by preview and commits.
- Terminal preview with the real graph through `gh`: now (GitHub's shades) and after
  (estimated), plus an overlap count.
- `make commits`: checks, preview, confirmation before committing and pushing, empty
  commits at noon UTC, push with git's stored login, undo command printed.
- Version 1 removed (Docker, token prompt, the old script); its bugs are gone with it.
- Patterns as text files, 22 included; `make image` turns a picture file or URL into one.
- Short, clear error messages instead of tracebacks.
- README for visitors with SVG pictures drawn from the patterns (`make gallery`); repo
  description, topics, template setting and social preview.
