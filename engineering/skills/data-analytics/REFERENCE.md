# Data Analytics Reference

Use this reference after the objective, target, success metric, scope, and delivery format are confirmed.

## Analysis contract

Record this before implementation:

| Field | Required detail |
|---|---|
| Decision | Action the stakeholder will take from the result |
| Objective | Descriptive, diagnostic, predictive, prescriptive, or causal question |
| Unit of analysis | Customer, order, session, day, transcript, experiment unit, etc. |
| Target/KPI | Exact definition, formula, source fields, and observation time |
| Success | Primary metric, threshold, baseline, and guardrail metrics |
| Population | Inclusion/exclusion rules and time window |
| Constraints | Latency, interpretability, privacy, budget, or operational limits |
| Deliverable | Notebook, Markdown report, Excel dashboard, audience, and deadline |

If target or success cannot be defined, limit work to profiling and exploratory analysis and label conclusions as exploratory.

## Intake by format

- **CSV/TSV:** detect delimiter and encoding; verify quoted fields, decimal symbols, headers, and malformed rows.
- **Excel:** enumerate sheets, formulas, merged cells, hidden rows/columns, named ranges, and date serials. Do not overwrite the source workbook.
- **JSON/JSONL:** inspect nesting, optional fields, arrays, schema drift, and record boundaries before normalizing.
- **Markdown/text:** identify document boundaries, headings, tables, metadata, encoding, and redaction needs.
- **Chat logs/transcripts:** preserve speaker, timestamp, conversation, and message order; avoid splitting conversations across evaluation sets.

Create a manifest containing source path, size, modification time, row/document count, schema summary, and transformation outputs. Hash files when lineage or auditability matters.

## Cleaning decision log

For every material cleaning rule, record:

```text
Issue: 8.3% missing values in annual_revenue.
Rule: Median imputation within company_size segment plus missingness indicator.
Reason: Preserve rows while retaining a potentially informative missingness signal.
Impact: 4,218 values imputed; target distribution unchanged within tolerance.
```

Check at minimum:

- row/document counts before and after each stage
- unique-key and duplicate rates
- missingness overall and by target/segment/time
- impossible values and cross-field consistency
- category and unit normalization
- timestamp timezone and ordering
- join cardinality, unmatched keys, and fan-out
- label definition and leakage risk

Prefer vectorized Pandas expressions, `groupby`, `merge`, `pivot_table`, and built-in string/datetime operations. Avoid `iterrows`, `itertuples`, and per-row `apply` for large tabular workloads unless no vectorized alternative exists and profiling justifies it. For out-of-memory data, consider chunked reads or an already-available engine such as DuckDB, Polars, Spark, or Dask; do not add a dependency without checking the project and explaining why.

## EDA and feature engineering

Choose views that answer the analysis contract rather than generating every possible chart:

- distribution and missingness summaries
- time trends with relevant event annotations
- target rates by actionable segment
- correlation/association with nonlinear and categorical measures where appropriate
- cohort, funnel, retention, or survival views when the unit and objective require them
- anomaly investigation with source-record traceability

Document every derived feature with its formula, source columns, availability time, and business interpretation. Fit imputers, encoders, scalers, and feature selection only on training data. Use pipelines where the available library supports them.

For LLM/NLP-derived features:

1. Define a label schema with positive and negative examples.
2. Redact or avoid sensitive fields and obtain approval before using external services.
3. Pin the prompt, model identifier, parameters, and parsing rules.
4. Use deterministic settings when practical and retry safely.
5. Validate a stratified sample against human labels; report agreement and failure modes.
6. Cache identifiers and outputs securely so runs are reproducible and resumable.

## Method selection

| Objective | Typical methods | Required checks |
|---|---|---|
| Describe | Aggregation, distributions, cohorts, funnels | Coverage, denominator definitions, uncertainty |
| Diagnose | Segmentation, decomposition, associations | Confounding, multiple comparisons, alternative explanations |
| Compare/A-B test | Difference in means/proportions, regression, nonparametric or variance-aware tests | Randomization unit, sample ratio mismatch, power, effect size, confidence interval |
| Predict continuous target | Linear/regularized models, tree ensembles, gradient boosting | Baseline, MAE/RMSE, residuals, drift, segment errors |
| Predict class | Logistic model, Random Forest, gradient boosting | Prevalence, PR-AUC/ROC-AUC, threshold metrics, calibration, imbalance |
| Forecast | Naive/seasonal baseline, time-series regression or forecasting | Backtesting, horizon, seasonality, leakage, prediction intervals |
| Extract/classify text | Rules, classical NLP, embeddings/classifiers, LLM extraction | Human-labeled sample, agreement, cost, latency, privacy |
| Estimate causal impact | Randomized experiment or defensible quasi-experimental design | Identification assumptions, balance, interference, sensitivity analysis |

Never describe an observational association as causal without a defensible identification strategy. For experiments, analyze using the randomized unit, check sample ratio mismatch before treatment effects, and avoid peeking-driven early stopping unless the design supports sequential testing.

## Modeling gates

Before accepting a model, verify:

- a naive or current-process baseline exists
- train/validation/test boundaries reflect real deployment timing and entities
- no person, account, conversation, or future record leaks across splits
- preprocessing is learned only from training data
- hyperparameter selection does not use the final test set
- primary and guardrail metrics meet the analysis contract
- errors, calibration, and performance are examined by important segments
- feature importance or explanations are not presented as causal effects
- operational threshold, capacity, costs, and false-positive/negative tradeoffs are explicit
- results include uncertainty and stability across folds, periods, or resamples

## Deliverable standards

### Jupyter notebook

Use a linear, restartable structure:

1. Objective and analysis contract
2. Environment and imports
3. Data manifest and loading
4. Validation and cleaning log
5. EDA and feature definitions
6. Methods and assumptions
7. Results and diagnostics
8. Recommendations and limitations
9. Exported artifacts

Restart the kernel and run all cells in order. Keep secrets out of cells and outputs. Avoid hidden state, manual edits to generated files, and absolute machine-specific paths where possible.

### Markdown report

Include:

- executive summary and decision recommendation
- KPI definitions and scope
- data quality and methodology
- key findings with tables/figures
- uncertainty, limitations, and non-causal caveats
- prioritized actions with owner or measurement plan when known
- technical appendix sufficient to reproduce the work

### Excel dashboard

Use separate sheets for `README`, `KPI Summary`, analysis views, and `Clean Data` where size permits. Include source/as-of date, metric definitions, units, filters, and refresh instructions. Use consistent number formats and accessible colors; ensure charts have titles, labels, and meaningful scales. Test formulas for errors, filters for correct ranges, and displayed totals against the analysis output. If row limits or workbook performance make Excel unsuitable, explain the constraint and propose an extract or connected summary instead.

## Final QC checklist

- [ ] Analysis answers the original decision, target, and success metric.
- [ ] Source data remains unchanged and lineage is documented.
- [ ] Cleaning decisions and row-count impacts are recorded.
- [ ] Leakage, confounding, bias, and privacy risks are assessed.
- [ ] Statistical/model assumptions and uncertainty are reported.
- [ ] Key figures reconcile to source and transformed data.
- [ ] Findings, hypotheses, and recommendations are clearly separated.
- [ ] The full deliverable runs or refreshes without manual hidden steps.
- [ ] No credentials, sensitive raw data, or unintended metadata are exposed.
- [ ] Limitations and concrete next steps are included.
