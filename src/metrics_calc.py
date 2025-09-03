from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Dict, Any
from src.utils.helpers import normalise_service, trapezoid_auc
from src.log_parser import extract_events

def compute_time_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    ev = extract_events(df)
    def delta(a, b):
        if a is None or b is None:
            return 'NR'
        return (b - a).total_seconds()
    return {
        'MTTC': delta(ev.attack_start, ev.compromise),
        'MTTD': delta(ev.attack_start, ev.detection),
        'MTTR': delta(ev.compromise, ev.restored),
        'attack_start': ev.attack_start,
        'compromise': ev.compromise,
        'detection': ev.detection,
        'restored': ev.restored,
    }

def compute_service_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    ev = extract_events(df)
    # choose baseline window end: attack_start if present, else first timestamp
    baseline_end = ev.attack_start if ev.attack_start is not None else df['timestamp'].iloc[0]
    dfn, baseline = normalise_service(df, baseline_end)
    # compute NRI (AUC / total_duration)
    t0, t1 = dfn['timestamp'].min(), dfn['timestamp'].max()
    duration = (t1 - t0).total_seconds()
    auc = trapezoid_auc(dfn['timestamp'], dfn['service_norm'])
    nri = auc / duration if duration > 0 and not np.isnan(auc) else np.nan
    # MLS: minimum service level
    mls = float(dfn['service_norm'].min())
    # DR: 1 - mean normalised service
    dr = float(1.0 - dfn['service_norm'].mean())
    return {
        'baseline_rps': float(baseline),
        'NRI': float(nri) if not np.isnan(nri) else 'NR',
        'MLS': mls if not np.isnan(mls) else 'NR',
        'DR': dr if not np.isnan(dr) else 'NR',
    }
