# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project goal

Draw pictures (patterns, later text) on a GitHub contribution graph by creating backdated
commits. The goal of the current iteration:

1. **Preview** what the graph will look like before anything is committed or pushed.
2. **A better flow**: pick a pattern and position, preview, then create the commits in this
   repo and push, with as little manual input as possible.

## Where things stand

Version 1 (January–July 2025) was written by copy-pasting between Gemini, ChatGPT and Mistral,
so it was never designed as a whole. Version 2 replaces it piece by piece:

- `commits.py` (`make commits`): checks main is clean and level with GitHub, shows the
  preview, asks before committing and before pushing. Empty commits at 12:00 UTC, pushed with
  git's stored login. Prints the undo (`git reset --keep <sha>`) before the first commit.
- `patterns.py`: a dict of patterns, 7 strings (one per weekday row), a digit = commits that
  day, space = none.
- `plan.py`: `plan_commits(pattern, start)` turns a pattern and a start Sunday into
  `(day, commits)` pairs. The one place that maps patterns onto the graph: the preview and
  the commit step must both use it.
- `preview.py`: draws the year's graph in the terminal (`make preview`): now, with GitHub's
  own shades, and after the planned commits, with estimated shades, plus how many planned
  days already have contributions. Digits instead of colours when the output is not a
  terminal, which is what the tests check.
- `contributions.py`: reads the real graph through `gh api graphql` (read only). Falls back
  to the pattern alone if `gh` is missing or offline.
- Version 1, until the next PR removes it: `make-commits.py` (asks for a token, appends to
  `contributions.txt` per commit) and the `Dockerfile` that runs it.

The fake commits go into **this repo** on purpose: that is how they reach the graph. The 900+
"Contribution" commits from 2018–2024 in `main` are earlier drawings, not clutter. They must
stay on `main` (the default branch) to count, so never squash or rewrite them.

Open work is in `TODO.md`.

`tests/test_patterns.py` checks every pattern is 7 rows of equal width. `patterns.py` is
wrapped in `# fmt: off` so ruff keeps each pattern one row per line. `tests/test_commits.py`
makes real commits, but only in throwaway repos under pytest's `tmp_path`.

## How the contribution graph works

What the preview and the commit generator need to get right:

- One column per week, 7 rows from **Sunday (top) to Saturday (bottom)**; the year view shows
  about 53 columns. A pattern's top-left cell must therefore land on a Sunday.
- A commit counts on the day of its **author date**, in the timezone of the date given.
- Commits only count when the author email is verified on the GitHub account, they are on the
  repo's default branch, and the repo is not a fork. Commits to a private repo only show if
  "private contributions" is switched on in the profile.
- The colours (5 levels) are **relative to the user's own activity**: the same number of
  commits can be a light or a dark square depending on their other contributions. So the
  preview must combine the pattern with the user's real contributions to be accurate.
- GitHub does not document the shading. Measured 2026-10-28 on the maintainer's graph: shade =
  `ceil(4 × count / cap)`, where the cap is the busiest day except that some outlier days are
  left out (2026: busiest 28, cap about 20). When outliers are dropped is not consistent, so
  the preview's "after" shades are an estimate. The API returns GitHub's real shade per day
  (`contributionLevel`), so "now" is exact.
- Reading the graph (`gh api graphql`, `gh api user`) is read only and fine for Claude to run.

## Commands

Everything runs locally via make and uv. Run `make` to list the targets.

| Command | Purpose |
|---|---|
| `make preview PATTERN=heart START=2024-03-03` | show a pattern on the graph; START is a Sunday |
| `make commits PATTERN=heart START=2024-03-03` | the same preview, then commit and push (asks first) |
| `make test` | pytest |
| `make lint` / `make format` | ruff check / format and auto-fix |
| `make lock` / `make sync` | update `uv.lock` / create the local `.venv` |
| `make clean` | remove tool caches |

The old Docker way still works until the next PR removes it.

- Dependencies: `uv add <pkg>` (or `uv add --group dev <pkg>`); commit `uv.lock` together with
  `pyproject.toml`, never edit it by hand.
- For Python use `uv run python ...`: `python` in Git Bash is the Microsoft Store alias.
- Makefile recipes run under cmd.exe: plain commands only, no pipes, redirects, `rm -rf` or
  `&&` chains; use `$(info)` for printed text.
- Run `make lint` and `make test` before pushing.

## Rules for Claude

- **Never run `make commits`** or otherwise create contribution commits in this repo or push
  them. That step runs on `main` and is the maintainer's; print the command instead.
  `make preview`, and end-to-end runs against throwaway clones in the scratchpad (a bare
  clone standing in for GitHub), are fine.
- **Never ask for, print or store a GitHub token.** Prefer `gh auth` or the git credential
  helper over tokens in URLs.
- Never rewrite or squash this repo's history: the old "Contribution" commits are the drawings.

## Conventions

- Python 3.13, ruff (line length 100). Keep logic (pattern → dates and counts,
  preview rendering) in plain functions that can be tested without git or the network.
- Comments are for the maintainer, who knows some Python: explain the why and non-obvious
  constructs briefly, don't repeat the code.
- The maintainer is on **Windows** (PowerShell and Git Bash). Use LF line endings and UTF-8.
- Don't write the maintainer's name in files, commits or PRs; write "the maintainer" (they/them).

## Workflow

- **`TODO.md`** holds the PR queue, bugs, ideas and open decisions. Update it in the same
  commit as the work that changes it.
- **Plan first.** For any non-trivial change, propose the steps and wait for an OK, then do one
  step at a time and report after each.
- **Small PRs, one topic per branch**, cut from a fresh `main`. Claude may create branches,
  commit, push them and open PRs with `gh`. **Never push to `main` or merge a PR.**
  (Code changes go through PRs; the fake commits are made directly on `main` by the maintainer.)
- Update this file when the architecture, commands or conventions change.
