from __future__ import annotations
import pandas as pd
from typing import Optional, Tuple
from src.utils.helpers import iso_to_ts, EventTimes

def read_log_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # required columns: timestamp, event, rps
    if not set(['timestamp','event','rps']).issubset(df.columns):
        raise ValueError(f"Missing required columns in {path}. Need: timestamp,event,rps")
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df

def extract_events(df: pd.DataFrame) -> EventTimes:
    def first_time(ev: str) -> Optional[pd.Timestamp]:
        s = df.loc[df['event'] == ev, 'timestamp']
        return s.iloc[0] if len(s) else None

    return EventTimes(
        attack_start = first_time('attack_start'),
        compromise   = first_time('compromise'),
        detection    = first_time('detection'),
        restored     = first_time('restored'),
    )
