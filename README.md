# CIRF: Consistent Impact Representation Framework

This repository contains a reference implementation of the **Consistent Impact Representation Framework (CIRF)**.
It provides a reproducible pipeline to compute time-based, recovery-oriented, and business-level resilience metrics
from adversary-emulation experiments (e.g., CALDERA / scripted attacks) using log data.

> Metrics: MTTC, MTTD, MTTR, AUC→NRI (Normalised Resilience Index), Minimum Service Level (MLS), Disruption Ratio (DR).

## Quick start

```bash
# 1) create & activate a virtual env (recommended)
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) install requirements
pip install -r requirements.txt

# 3) run example
python src/cirf_pipeline.py --input examples/sample_logs --output results
```

Outputs will be written to the `results/` directory:
- `metrics_per_run.csv` (metrics for each run file)
- `metrics_summary.csv` (mean ± sd across runs)

## Input format

CSV with the following columns (header required):

| column      | type      | description                                                        |
|-------------|-----------|--------------------------------------------------------------------|
| timestamp   | ISO8601   | event time (e.g., 2025-08-30T10:00:00)                             |
| event       | string    | one of: `attack_start`, `compromise`, `detection`, `restored`      |
| rps         | float     | service throughput (requests per second)                           |

Notes:
- Baseline service level is estimated as the mean `rps` during the pre-attack window (before first `attack_start`).  
- Service is normalised by baseline when computing NRI / MLS / DR.  
- Missing events are handled as censored (marked `NR`) and metrics degrade gracefully.

## License

MIT
