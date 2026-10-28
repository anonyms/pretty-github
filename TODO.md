# TODO

Open work and ideas. Tick items off (or remove them) in the PR that finishes them.

## Next up

The PR queue, in order. Each is a small PR the maintainer reviews and merges.

- [x] **Project setup**: `pyproject.toml` with uv, ruff and pytest; drop the unused
      `requests`, `pandas` and `numpy`; `.gitattributes` for LF. A `Makefile` wrapping
      `uv run` (`make test`, `make lint`, `make format`; `make preview` and `make commits`
      come with their PRs), with `make` alone listing the targets. No behaviour change.
- [x] **Fix the patterns and make them testable**: add the missing commas (smiley, heart,
      rocket, mushroom), remove `lol_face` from the prompt (it does not exist), and a test that
      every pattern has 7 rows of equal width and only digits or spaces.
- [x] **Pattern → plan, as a pure function**: given a pattern and a start Sunday, return the list
      of (date, commit count). Reject a start date that is not a Sunday. Tests. Both the
      preview and the commit step use this, so they can never disagree.
- [ ] **Preview v1, in the terminal**: print the year grid with coloured squares (ANSI), with
      the pattern placed on it, before asking anything else. Pattern alone, no real data yet.
- [ ] **Preview v2, with real contributions**: fetch the user's calendar for the year (GitHub
      GraphQL `contributionsCollection`, via `gh api graphql`) and show "now" and "after" side
      by side, with colours bucketed over the combined data. Matters here because earlier
      drawings (2023, 2024) are already on the graph and a new one may overlap them.
- [ ] **Rework the commit step** (`make commits`): reads the same plan as the preview, shows
      it and asks for confirmation; dry run by default. Commit with
      `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` (maybe `git fast-import` for speed), push with
      `gh`/credential helper instead of a token in the URL. Uses the local git config, so no
      user/email build args.
- [ ] **Remove Docker** once the Makefile covers everything; update `README.md`.

## Bugs in version 1

- [x] Four patterns draw as one line (missing commas, see Next up).
- [ ] The token is typed with `input()` (shown on screen) and put in the push URL.
- [x] No check that the start date is a Sunday, so patterns come out shifted or cut.
- [ ] `GIT_USER` unset crashes later with a `TypeError` instead of a clear message.
- [ ] One `git add` + `git commit` subprocess per commit: slow for large patterns.

## Ideas

- **Place by column, not date**: pick a year and a week column (or "centre it"), and let the
  tool work out the start Sunday.
- **Text**: render short text with a 5×7 pixel font.
- **Patterns as files** (`patterns/*.txt`) instead of a Python dict, so adding one needs no code.
- **Intensity by level, not count**: write patterns as levels 1–4 and work out the commit
  counts from the user's real data so the colours come out as drawn.
- **HTML/SVG preview** that looks like the real graph, after the terminal one.
- **Editor**: a small web page or Streamlit app to draw a pattern on the grid with a live
  preview, then export it.

## Decided

- **The fake commits stay in this repo**, on `main`: that is the point of the project. Never
  rewrite or squash them (2026-10-26).
- **uv + Makefile instead of Docker**, like the maintainer's other repos (2026-10-26).
- **Preview starts in the terminal**; HTML/SVG later (2026-10-26).
