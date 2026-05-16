# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
python -m unittest discover tests

# Run a single test
python -m unittest tests.test.TestKonwxml.test_zamien

# Lint
ruff check .

# Format
ruff format .

# Build distribution packages
pip install build && python -m build
```

## Architecture

**xml_konwerter** is a Python library that processes XML templates by substituting `{{VARIABLE_NAME}}` placeholders with values from a dictionary and iterating table rows for list data (e.g., invoice line items).

### Core modules

- `xml_konwerter/konwxml.py` — `KONWXML` class, the template engine:
  - `replace_text(root, d)` — walks all XML elements, replaces `{{VAR}}` in text nodes with dict values
  - `replace_all(root, d, alista, prefix, htmlkeypairing)` — orchestrates substitution; calls `replace_text`, then `replace_linie` for table structures
  - `replace_linie(...)` — finds XML table elements marked `{{LINIE<id>}}`, clones and populates rows from list data, removes template markers
- `xml_konwerter/konwertujdok.py` — `konwertujdok(sou, dest, d, alist, htmlkeypairing)` high-level entry point: reads source template, calls `replace_all`, writes output file
- `xml_konwerter/__init__.py` — exports `KONWXML` and `konwertujdok`

### Data flow

```
XML template ({{PLACEHOLDER}} markers)
  → konwertujdok(sou, dest, d, alist, htmlkeypairing)
      → KONWXML.replace_all()
          → replace_text()    # simple key→value substitution
          → replace_linie()   # table row iteration from list data
  → ElementTree writes output XML
```

### Key concepts

- `htmlkeypairing`: list of tuples mapping table identifiers (the `<id>` in `{{LINIE<id>}}`) to dict keys holding row data
- `alist`: secondary dict for list/row data; defaults to `d` if not provided
- Tests in `tests/testdata/` contain XML fixtures covering substitution, single/multi-row tables, headers/footers, and nested structures

### Linting

`ruff` is configured in `pyproject.toml`: line length 120, rules E/F/I, double quotes. CI also runs `flake8` against the same sources.

### Publishing

Releases are triggered by pushing a `v*` tag; GitHub Actions builds and publishes to PyPI via OIDC trusted publishing (no API token needed).
