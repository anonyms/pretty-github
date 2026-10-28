# Recipes are kept to plain commands so they work with both cmd.exe (Windows make)
# and sh (Linux/macOS/Git Bash). Avoid pipes, redirects and shell-specific syntax.

RUN = uv run

# Two-space indent for help text ($(info) strips leading whitespace)
EMPTY :=
I := $(EMPTY)  $(EMPTY)

.DEFAULT_GOAL := help
.PHONY: help preview test lint format lock sync clean

# $(info) prints from make itself, so help looks the same in every shell
help:
	$(info Usage: make TARGET)
	$(info )
	$(info Drawing)
	$(info $(I)preview   Show a pattern on the graph - nothing is committed)
	$(info $(I)          e.g. make preview PATTERN=heart START=2024-03-03 - START is a Sunday)
	$(info )
	$(info Quality)
	$(info $(I)test      Run pytest)
	$(info $(I)lint      Check linting and formatting with ruff)
	$(info $(I)format    Auto-fix lint issues and format code with ruff)
	$(info )
	$(info Dependencies)
	$(info $(I)lock      Update uv.lock after editing pyproject.toml)
	$(info $(I)sync      Create or update the local .venv for VS Code)
	$(info )
	$(info Other)
	$(info $(I)clean     Remove tool caches)
	@cd .

preview:
	$(RUN) python preview.py $(PATTERN) $(START)

test:
	$(RUN) pytest

lint:
	$(RUN) ruff check .
	$(RUN) ruff format --check .

format:
	$(RUN) ruff format .
	$(RUN) ruff check --fix .

lock:
	uv lock

sync:
	uv sync

clean:
	$(RUN) python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('.pytest_cache', '.ruff_cache')]"
