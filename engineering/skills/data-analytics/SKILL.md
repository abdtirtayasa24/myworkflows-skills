---
name: data-analytics
description: Performs rigorous, reproducible analysis of structured and unstructured data and turns findings into actionable business recommendations. Use when users request deep analysis, EDA, statistical testing, predictive modeling, or reporting from CSV, Excel, JSON, Markdown, transcripts, or similar data files.
---

# Data Analytics

## Quick start

Before writing code, inspect the available files and ask the user to confirm:

1. **Decision and objective** — What decision should this analysis support?
2. **Target** — Which outcome, response, or KPI is being explained, predicted, or improved?
3. **Success** — What metric and threshold define a useful result?
4. **Scope** — Unit of analysis, population, time window, exclusions, and constraints.
5. **Delivery** — Jupyter notebook, Markdown report, or Excel dashboard; intended audience and detail level.

Translate the answers into a compact analysis contract:

```text
Objective: Reduce customer churn.
Target: churned_within_30_days (binary).
Primary metric: PR-AUC; baseline: current heuristic.
Decision rule: prioritize the top 10% highest-risk accounts.
Scope: active paid accounts observed in the previous 12 months.
Deliverable: reproducible notebook plus executive Markdown summary.
```

Do not silently invent missing business definitions. If the user cannot provide them, state provisional assumptions and request confirmation before modeling.

## Scaffold deliverables

Resolve these paths relative to this `SKILL.md` and run the appropriate generator after confirming the analysis contract:

```bash
python3 scripts/create_analysis_notebook.py --title "Churn Analysis" --objective "Identify at-risk accounts" --target "churned_within_30_days" --metric "PR-AUC" --data data/customers.csv --out output/churn-analysis.ipynb
uv run --with openpyxl python scripts/create_excel_dashboard.py --title "Churn Dashboard" --objective "Monitor churn risk" --target "churned_within_30_days" --metric "Monthly churn rate" --out output/churn-dashboard.xlsx
```

Both scripts refuse to overwrite files unless `--force` is supplied. Use `--help` for defaults and optional arguments. The notebook generator uses only the Python standard library; the dashboard generator requires `openpyxl` and provides direction-aware KPI status formulas through dropdowns.

## Workflow

### 1. Scope and translate the objective

- Classify the task as descriptive, diagnostic, predictive, prescriptive, or causal.
- Express the business question as measurable variables, hypotheses, constraints, and decision rules.
- Define primary and guardrail metrics before inspecting outcomes in depth.
- Record assumptions, available data, required joins, and known limitations.

### 2. Profile, clean, and preprocess

- Preserve source files; create transformed copies and a reproducible data manifest.
- Inspect schema, types, units, ranges, cardinality, missingness, duplicates, and time coverage.
- Resolve missing values, duplicates, outliers, inconsistent categories, dates, encodings, and units with explicit rules.
- Validate joins, row counts, key uniqueness, and target integrity before and after transformation.
- Prefer Pandas vectorized operations over row loops. For data larger than memory, use chunking or an available columnar/query engine; check dependencies first.
- Never expose sensitive data or send it to an external model without explicit approval.

### 3. Engineer features and perform EDA

- Analyze distributions, segments, trends, correlations, class balance, and anomalies.
- Separate observations from hypotheses; correlation is not causation.
- Engineer only interpretable, objective-relevant features and document formulas and timing.
- Prevent target leakage, especially with post-outcome fields and time-dependent data.
- For text, derive auditable features such as themes, sentiment, entities, or categorical flags; validate extraction on a representative sample.

### 4. Analyze and model

- Start with a simple baseline and add complexity only when it improves the defined success metric.
- Match methods to the objective: confidence intervals and tests for inference; experiment analysis for A/B tests; regression/classification, Random Forests, or gradient boosting for prediction; NLP/LLM pipelines for text extraction.
- Use suitable splits, cross-validation, imbalance handling, and time-aware validation.
- Report effect sizes and uncertainty, not only p-values or model scores; correct for multiple testing when applicable.
- Compare models on held-out data and assess calibration, stability, segment performance, and practical impact.
- Treat AI-generated labels as model outputs, not ground truth; retain prompts/model settings and manually validate a sample.

### 5. Synthesize, deliver, and quality-check

- Translate results into decisions: finding → evidence → confidence → recommended action → expected impact.
- Distinguish facts, interpretations, and recommendations; disclose limitations and alternative explanations.
- Confirm the requested output before packaging. Support:
  - **Jupyter notebook:** executable narrative with inputs, methods, results, and environment details.
  - **Markdown report:** executive summary, methodology, findings, recommendations, and appendix.
  - **Excel dashboard:** clean data sheet, KPI summary, charts/tables, filters where supported, definitions, and refresh notes.
- Re-run the full pipeline, reconcile totals to source data, verify charts and formulas, and confirm no sensitive data is exposed.
- End with prioritized actions and the next measurement or experiment needed.

For method selection, QC gates, and deliverable standards, see [REFERENCE.md](REFERENCE.md).
