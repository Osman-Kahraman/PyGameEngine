# Contributing to PyGameEngine

Thank you for your interest in contributing! This guide will help you get started. 

⚠️ IMPORTANT  
**Please use code formatting before every commit — otherwise, the pipeline will fail.**

## Code Formatting

This project uses Black, isort, and Ruff to maintain consistent code style and quality.

## Requirements

| Library     | Version |
| ----------- | ------- |
| `black`     | latest  |
| `isort`     | latest  |
| `ruff`      | latest  |

---

### Black Formatting
If you are working only on the engine code, you can format just that folder:

```bash
python3 -m black game_engine/
```

## Import Sorting

```bash
python3 -m isort game_engine/
```

## Linting (Code Quality Checks)

```bash
python3 -m ruff check game_engine/
```

## To visualise the show processing functions call 
```bash
python -m pstats profile.stats
```
then 

```commandline
sort time
stats 20
```


> **Note**: Some files may intentionally use dynamic imports or exec().
In such cases, inline ignores like # noqa: F401 are acceptable.
