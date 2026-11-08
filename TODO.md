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
- [x] **Preview v1, in the terminal**: print the year grid with coloured squares (ANSI), with
      the pattern placed on it, before asking anything else. Pattern alone, no real data yet.
- [x] **Preview v2, with real contributions**: fetch the user's calendar for the year (GitHub
      GraphQL `contributionsCollection`, via `gh api graphql`) and show "now" and "after" side
      by side, with colours bucketed over the combined data. Matters because earlier
      drawings may already be on the graph and a new one may overlap them.
      Done as two grids above each other (side by side is too wide), plus an overlap count.
- [x] **Rework the commit step** (`make commits`): reads the same plan as the preview, shows
      it and asks for confirmation; dry run by default. Commit with
      `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` (maybe `git fast-import` for speed), push with
      `gh`/credential helper instead of a token in the URL. Uses the local git config, so no
      user/email build args. Done as `commits.py`: y/N before committing and before pushing
      instead of a dry-run flag; empty commits at 12:00 UTC; one `git commit` per commit
      (24 commits in about 5 s, so no fast-import).
- [x] **Remove Docker and version 1**: `Dockerfile`, `make-commits.py`, `contributions.txt`,
      the Docker part of `README.md` and its "Watch out" about tokens.

- [x] **More default patterns**: space-invader, pacman, christmas-tree, star, cat, house,
      skull, creeper (15 in all). Then alien, the first made with `make image` (16).
- [x] **Patterns as files**: `patterns/<name>.txt`, dots for blanks, `#` for comments.
- [x] **Patterns from an image**: `make image IMAGE=cat.png NAME=cat` shrinks a small picture
      to 7 rows (keeping proportions, at most about 52 columns), maps darkness to shades 1–4,
      prints it and saves `patterns/cat.txt`. Light or transparent pixels stay blank;
      `INVERT=1` for light-on-dark pictures. Needs Pillow. IMAGE can also be a URL (asked for
      by the maintainer). Checked 2026-11-03 with Twemoji PNGs: heart, cat face and alien
      monster are recognisable; a white ghost is not (too little contrast).
- [x] **README for visitors**: what it is, a picture of the result, why this tool, a quick
      start, the pattern gallery, how it works. Pictures are SVGs drawn from the pattern files
      (`make gallery`), so no screenshots go stale. "Learnings" dropped.
- [x] **Repo settings for discoverability**: description, 10 topics (github-contributions,
      contribution-graph, gitfiti, ...) and "Template repository" switched on, so the
      README's "Use this template" works. Social preview image (the example year with the
      name, 1280×640 PNG) uploaded by hand: the API cannot set it. Repo pinned (2026-11-08).

## Ideas for getting noticed

- Real screenshots in the README: the terminal preview, and a profile graph with a drawing.
- Pin the repo on the profile; submit to awesome-lists; a "Show HN" or r/github post with
  the picture.

## Ideas for image patterns

- **Pick the threshold**: `BLANK_BELOW` (40) decides what counts as background. A setting
  could help pictures on off-white or busy backgrounds.
- **Colour instead of darkness**: the white ghost failed because it is light. Using
  "different from the background colour" instead of "dark" would catch it.

## Bugs in version 1

- [x] Four patterns draw as one line (missing commas, see Next up).
- [x] The token is typed with `input()` (shown on screen) and put in the push URL.
      `make commits` pushes with git's stored login.
- [x] No check that the start date is a Sunday, so patterns come out shifted or cut.
- [x] `GIT_USER` unset crashes later with a `TypeError` instead of a clear message.
      `make commits` uses the local git config; the old script is removed.
- [x] One `git add` + `git commit` subprocess per commit: slow for large patterns. Empty
      commits halve the calls; fast enough (24 commits in about 5 s).

## Ideas

- **Clean old drawings** (parked 2026-11-07): remove the drawings of chosen years. GitHub has
  no way to subtract contributions, so cleaning means removing the commits from `main` and
  force-pushing, which goes against "never rewrite history" and would need that rule changed
  for a deliberate clean.
  - Cost: every commit after the oldest one removed gets a new ID (kept drawings and code
    alike). Files end up unchanged; old PR pages keep pointing at the old IDs. Every clone
    needs a reset afterwards.
  - Shape: `make clean FROM=... TO=...` (date range), later also `make clean PATTERN=...
    START=...` (undo one pattern). Only commits with the message "Contribution" and the
    user's email; snapshot-based rewrite (no conflicts from version 1's `contributions.txt`
    edits); now/after preview; ask before rewriting and before pushing; a backup
    (`git clone --mirror`) and the restore command; `--force-with-lease`; no open PRs.
  - Check first that the commits in the range are all drawings, and measure how long GitHub
    takes to drop contributions after a force-push.
  - Alternative considered: one repo per drawing, deleted to undo it. Rejected: the drawings
    belong in this repo.
- **Place by column, not date**: pick a year and a week column (or "centre it"), and let the
  tool work out the start Sunday.
- **Text**: render short text with a 5×7 pixel font.
- **Better "after" shades**: work out the cap (busiest day without outliers) from GitHub's
  real levels for the year, instead of assuming the busiest day. Measured 2026-10-28 over
  several years: in most the cap is the busiest day, in some one or two top days are left
  out, and two years with a single top day were treated differently.
- **HTML/SVG preview** that looks like the real graph, after the terminal one.
- **Editor**: a small web page or Streamlit app to draw a pattern on the grid with a live
  preview, then export it.

## Decided

- **The fake commits stay in this repo**, on `main`: that is the point of the project. Never
  rewrite or squash them (2026-10-26).
- **uv + Makefile instead of Docker**, like comparable projects (2026-10-26).
- **Preview starts in the terminal**; HTML/SVG later (2026-10-26).
- **No "intensity by level"** (patterns as shades, commit counts worked out from real data):
  drawings go into quiet years, where the digits already come out as drawn (2026-11-03).
