#!/usr/bin/env python3
"""Create a reproducible Jupyter notebook skeleton for data analysis."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def slugify(value: str) -> str:
    """Return a filesystem-friendly slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "analysis"


def markdown(source: str) -> dict[str, Any]:
    """Build a Markdown notebook cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict[str, Any]:
    """Build an unexecuted code notebook cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def build_notebook(
    title: str,
    objective: str,
    target: str,
    metric: str,
    data_path: Path | None,
) -> dict[str, Any]:
    """Build an analysis notebook document."""
    configured_path = str(data_path) if data_path else "path/to/data.csv"
    path_literal = json.dumps(configured_path)

    cells = [
        markdown(
            f"""# {title}

## Analysis contract

- **Decision and objective:** {objective}
- **Target/KPI:** {target}
- **Primary success metric:** {metric}
- **Unit of analysis:** [Confirm before analysis]
- **Population and time window:** [Confirm before analysis]
- **Guardrail metrics:** [Define before modeling]
- **Intended deliverable/audience:** [Confirm]
"""
        ),
        markdown(
            """## Analysis plan

1. Validate source data, scope, and target integrity.
2. Apply documented cleaning and preprocessing rules.
3. Explore distributions, segments, trends, and associations.
4. Engineer objective-relevant features without leakage.
5. Establish a baseline, then evaluate appropriate statistical or predictive methods.
6. Synthesize evidence, uncertainty, limitations, and recommended actions.
"""
        ),
        code(
            """# Setup and reproducibility
from __future__ import annotations

import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
pd.set_option("display.max_columns", 100)
"""
        ),
        code(
            f"""# Configuration: keep paths and analysis constants in one place
DATA_PATH = Path({path_literal})
OUTPUT_DIR = Path("output/data-analytics")
TARGET_COLUMN = {json.dumps(target)}
PRIMARY_METRIC = {json.dumps(metric)}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
"""
        ),
        markdown(
            """## Data intake and provenance

Record the source owner, extraction time, reporting timezone, grain, expected keys, and any access or privacy restrictions. Keep source files unchanged and write transformed artifacts separately.
"""
        ),
        code(
            """# Load common tabular and text formats; adapt explicitly for unusual schemas.
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Update DATA_PATH; file not found: {DATA_PATH}")

suffix = DATA_PATH.suffix.lower()
if suffix == ".csv":
    raw_df = pd.read_csv(DATA_PATH)
elif suffix in {".tsv", ".txt"}:
    raw_df = pd.read_csv(DATA_PATH, sep="\\t")
elif suffix in {".xlsx", ".xls"}:
    raw_df = pd.read_excel(DATA_PATH)
elif suffix == ".jsonl":
    raw_df = pd.read_json(DATA_PATH, lines=True)
elif suffix == ".json":
    raw_df = pd.read_json(DATA_PATH)
elif suffix in {".md", ".markdown"}:
    raw_df = pd.DataFrame({"document": [DATA_PATH.read_text(encoding="utf-8")]})
else:
    raise ValueError(f"Unsupported source format: {suffix}")

print(f"Loaded {len(raw_df):,} rows and {raw_df.shape[1]:,} columns from {DATA_PATH}")
raw_df.head()
"""
        ),
        markdown(
            """## Data validation and cleaning

Document every material rule with the issue, chosen treatment, rationale, and row/value impact. Validate row counts, unique keys, joins, missingness, ranges, categories, dates, units, and target timing before and after transformation.
"""
        ),
        code(
            """# Vectorized data-quality profile
quality_summary = pd.DataFrame({
    "dtype": raw_df.dtypes.astype(str),
    "missing_count": raw_df.isna().sum(),
    "missing_pct": raw_df.isna().mean().mul(100).round(2),
    "unique_count": raw_df.nunique(dropna=False),
}).sort_values("missing_pct", ascending=False)

print(f"Exact duplicate rows: {raw_df.duplicated().sum():,}")
quality_summary
"""
        ),
        code(
            """# Apply approved cleaning rules here; avoid mutating raw_df.
analysis_df = raw_df.copy()
cleaning_log: list[dict[str, object]] = []

# Example:
# before = len(analysis_df)
# analysis_df = analysis_df.drop_duplicates(subset=["record_id"])
# cleaning_log.append({
#     "issue": "Duplicate record IDs",
#     "rule": "Keep the first record per record_id",
#     "rows_affected": before - len(analysis_df),
# })

pd.DataFrame(cleaning_log)
"""
        ),
        markdown(
            """## Exploratory data analysis

Prioritize views tied to the analysis contract: target distribution, actionable segments, time trends, anomalies, and plausible relationships. Treat correlations as hypotheses rather than causal evidence.
"""
        ),
        code(
            """# Numeric overview; add focused plots instead of generating every possible chart.
numeric_summary = analysis_df.describe(include=[np.number]).T
numeric_summary

# Example target check:
# analysis_df[TARGET_COLUMN].value_counts(dropna=False, normalize=True)
"""
        ),
        markdown(
            """## Feature engineering

For each feature, record its formula, source fields, availability time, and business interpretation. Fit learned preprocessing only on training data and exclude post-outcome information.
"""
        ),
        code(
            """# Build objective-relevant features with vectorized operations.
model_df = analysis_df.copy()
feature_definitions: dict[str, str] = {}

# Example:
# model_df["order_value"] = model_df["quantity"].mul(model_df["unit_price"])
# feature_definitions["order_value"] = "quantity * unit_price"

feature_definitions
"""
        ),
        markdown(
            """## Modeling and evaluation

Start with a naive or current-process baseline. Select methods that match the objective, use leakage-safe validation, and compare held-out performance using the predefined primary and guardrail metrics. Report effect sizes, uncertainty, calibration, segment performance, and operational tradeoffs.
"""
        ),
        code(
            """# Define the baseline, split strategy, method, and evaluation here.
# For time-dependent data, split chronologically rather than randomly.
results: dict[str, object] = {
    "baseline": None,
    "candidate": None,
    "primary_metric": PRIMARY_METRIC,
    "limitations": [],
}
results
"""
        ),
        markdown(
            """## Synthesis and quality control

### Findings
- [Finding] → [Evidence] → [Confidence]

### Recommended actions
1. [Action] — expected impact, owner, and measurement plan.

### Limitations and alternative explanations
- [Limitation]

### Reproducibility checks
- [ ] Source and transformed row counts reconcile.
- [ ] Cleaning decisions and feature definitions are documented.
- [ ] Leakage, bias, privacy, and uncertainty were assessed.
- [ ] Figures and reported metrics match computed results.
- [ ] Notebook runs top-to-bottom after restarting the kernel.
"""
        ),
        code(
            """# Export only reviewed, non-sensitive artifacts.
# analysis_df.to_csv(OUTPUT_DIR / "clean_data.csv", index=False)
# pd.DataFrame([results]).to_json(OUTPUT_DIR / "model_results.json", orient="records", indent=2)
"""
        ),
    ]

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Human-readable notebook title.")
    parser.add_argument("--objective", default="[Confirm the business objective]", help="Decision or objective.")
    parser.add_argument("--target", default="[Confirm the target or KPI]", help="Target variable or KPI.")
    parser.add_argument("--metric", default="[Confirm the success metric]", help="Primary success metric.")
    parser.add_argument("--data", type=Path, help="Optional initial source-data path.")
    parser.add_argument("--out", type=Path, help="Output .ipynb path.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    return parser.parse_args()


def main() -> None:
    """Generate the requested notebook."""
    args = parse_args()
    output = args.out or Path("output/jupyter-notebook") / f"{slugify(args.title)}.ipynb"
    if output.suffix.lower() != ".ipynb":
        raise SystemExit(f"Output must use the .ipynb extension: {output}")
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {output}")

    notebook = build_notebook(args.title, args.objective, args.target, args.metric, args.data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(notebook, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote analysis notebook: {output.resolve()}")


if __name__ == "__main__":
    main()
