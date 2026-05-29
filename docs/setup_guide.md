# Setup Guide

## Requirements

- Python 3.11+
- Local terminal access
- No cloud credentials or external services

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Run The Offline Pipeline

```bash
PYTHONPATH=src python3 -m compliance_security_dashboard.main
```

Or:

```bash
./scripts/run_pipeline.sh
```

## Run Tests And Quality Checks

```bash
python3 -m pytest
python3 -m ruff check .
python3 -m black --check .
python3 -m compileall src dashboard scripts
```

## Run The Dashboard

```bash
python3 -m streamlit run dashboard/streamlit_app.py
```

The dashboard expects generated files in `outputs/`. Run the pipeline first if any page reports missing outputs.
