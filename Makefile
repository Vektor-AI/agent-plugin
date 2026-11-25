.PHONY: check

check:
	uv run --locked ruff check scripts tests
	uv run --locked ruff format --check scripts tests
	uv run --locked rumdl check .
	uv run --locked zizmor --offline .github/workflows
	actionlint -color=false
	uv run --locked python scripts/check_package.py
	uv run --locked python -m unittest discover -s tests
