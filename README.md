# gas-calculator

[![CI](https://github.com/MichaelESantiagoG/gas-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/MichaelESantiagoG/gas-calculator/actions/workflows/ci.yml)

Streamlit app that estimates fuel fill-up costs, remaining range, and top-up targets.

## Features
- US and Metric unit system support
- Vehicle tank presets
- Fuel-needed and cost-to-full estimates
- Quarter, half, and full top-up cost targets
- Current tank-level gauge with low/medium/high thresholds
- Range estimate from fuel efficiency input

## Run locally
```bash
python3 -m pip install -r requirements.txt
streamlit run main.py
```

## Run tests
```bash
python3 -m pip install -r requirements-dev.txt
pytest -q
```

## Lint and format checks
```bash
ruff check .
black --check .
```

## Pre-commit hooks
```bash
pre-commit install
pre-commit run --all-files
```
