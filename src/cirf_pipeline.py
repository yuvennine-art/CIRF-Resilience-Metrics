from __future__ import annotations
import argparse, os, json
import pandas as pd
from typing import List, Dict, Any
from src.log_parser import read_log_csv
from src.metrics_calc import compute_time_metrics, compute_service_metrics

def compute_metrics_for_file(path: str) -> Dict[str, Any]:
    df = read_log_csv(path)
    tm = compute_time_metrics(df)
    sm = compute_service_metrics(df)
    m = {**tm, **sm}
    m['run_file'] = os.path.basename(path)
    return m

def summarise(df: pd.DataFrame) -> pd.DataFrame:
    # compute mean ± sd for numeric columns only
    numcols = df.select_dtypes(include='number').columns
    mean = df[numcols].mean(numeric_only=True)
    sd = df[numcols].std(numeric_only=True, ddof=1)
    out = pd.DataFrame({'mean': mean, 'sd': sd})
    out.index.name = 'metric'
    return out.reset_index()

def main():
    ap = argparse.ArgumentParser(description='CIRF pipeline: compute resilience metrics from logs')
    ap.add_argument('--input', required=True, help='input directory of CSV logs')
    ap.add_argument('--output', required=True, help='output directory')
    args = ap.parse_args()

    os.makedirs(args.output, exist_ok=True)
    files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.endswith('.csv')]
    if not files:
        raise SystemExit(f'No CSV files found in {args.input}')

    rows = []
    for f in sorted(files):
        m = compute_metrics_for_file(f)
        rows.append(m)
    per_run = pd.DataFrame(rows)
    per_run.to_csv(os.path.join(args.output, 'metrics_per_run.csv'), index=False)

    summary = summarise(per_run)
    summary.to_csv(os.path.join(args.output, 'metrics_summary.csv'), index=False)

    print('Wrote:', os.path.join(args.output, 'metrics_per_run.csv'))
    print('Wrote:', os.path.join(args.output, 'metrics_summary.csv'))

if __name__ == '__main__':
    main()
