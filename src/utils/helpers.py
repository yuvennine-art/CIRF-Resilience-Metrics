from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np

@dataclass
class EventTimes:
    attack_start: Optional[pd.Timestamp]
    compromise: Optional[pd.Timestamp]
    detection: Optional[pd.Timestamp]
    restored: Optional[pd.Timestamp]

def iso_to_ts(s: str) -> pd.Timestamp:
    return pd.to_datetime(s, utc=True)

def normalise_service(df: pd.DataFrame, baseline_window_end: pd.Timestamp) -> pd.DataFrame:
    # Baseline: mean rps before attack_start
    baseline_mask = df['timestamp'] < baseline_window_end
    baseline = df.loc[baseline_mask, 'rps'].mean()
    if pd.isna(baseline) or baseline <= 0:
        baseline = df['rps'].head(10).mean()  # fallback to early window
    df = df.copy()
    df['service_norm'] = df['rps'] / baseline if baseline > 0 else np.nan
    df['service_norm'] = df['service_norm'].clip(lower=0.0)  # avoid negatives
    return df, baseline

def trapezoid_auc(ts: pd.Series, ys: pd.Series) -> float:
    # expects timestamp series and normalised service in same length
    # convert to seconds since start
    t0 = ts.min()
    secs = (ts - t0).dt.total_seconds().to_numpy()
    y = ys.to_numpy()
    if len(secs) < 2:
        return float('nan')
    return float(np.trapz(y, secs))
