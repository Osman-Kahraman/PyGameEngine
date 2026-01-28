# Contributing to PyGameEngine

Thank you for your interest in contributing! This guide will help you get started.

## Code Formatting

This project uses Black, isort, and Ruff to maintain consistent code style and quality.

### Format a specific directory
If you are working only on the engine code, you can format just that folder:

```bash
python3 -m black game_engine/
```

### Format a single file

```bash
python3 -m black game_engine/ui.py
```

## Import Sorting

```bash
python3 -m isort game_engine/
```

## Linting (Code Quality Checks)

```bash
python3 -m ruff check game_engine/
```

> **Note**: Some files may intentionally use dynamic imports or exec().
In such cases, inline ignores like # noqa: F401 are acceptable.