# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project goal

Draw pictures (patterns, later text) on a GitHub contribution graph by creating backdated
commits. The goal of the current iteration:

1. **Preview** what the graph will look like before anything is committed or pushed.
2. **A better flow**: pick a pattern and position, preview, then create the commits in a
   separate target repo and push, with as little manual input as possible.

## Where things stand

Version 1 (January–July 2025) was written by copy-pasting between Gemini, ChatGPT and Mistral,
so it was never designed as a whole. It is one script:

- `make-commits.py`: asks for a start date, a pattern name, a repo name and a token (all via
  `input()`), writes one line to `contributions.txt` per commit, commits it with `--date`, and
  pushes with the token embedded in the URL.
- `patterns.py`: a dict of patterns, 7 strings (one per weekday row), a digit = commits that
  day, space = none.
- `Dockerfile`: runs the script; git user and email come in as build args.

The fake commits go into **this repo** on purpose: that is how they reach the graph. The 900+
"Contribution" commits from 2018–2024 in `main` are earlier drawings, not clutter. They must
stay on `main` (the default branch) to count, so never squash or rewrite them.

Known problems are listed in `TODO.md`. The most important ones:

- Four patterns (smiley, heart, rocket, mushroom) are missing commas between rows, so Python
  joins them into one long string and they draw as a single line.
- There is no preview and no dry run: the only way to see the result is to push.

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
  (The exact bucketing is not documented by GitHub; verify against a real graph.)

## Commands

Moving from Docker to a `Makefile` that wraps `uv run` (see `TODO.md`). Until then, Docker as
in `README.md`:

```powershell
docker build --build-arg GIT_USER="username" --build-arg GIT_EMAIL="email" -t make-commits .
docker run -it make-commits
```

For local Python use `uv run python ...`: `python` in Git Bash is the Microsoft Store alias.
Makefile recipes run under cmd.exe: plain commands only, no pipes, redirects, `rm -rf` or `&&`
chains; use `$(info)` for printed text.

## Rules for Claude

- **Never create contribution commits or push them.** That step runs on `main` and is the
  maintainer's; print the command instead. Previews and dry runs are fine.
- **Never ask for, print or store a GitHub token.** Prefer `gh auth` or the git credential
  helper over tokens in URLs.
- Never rewrite or squash this repo's history: the old "Contribution" commits are the drawings.

## Conventions

- Python, managed with uv once `pyproject.toml` exists. Keep logic (pattern → dates and counts,
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
