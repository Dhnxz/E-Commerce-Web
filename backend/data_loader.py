"""Data loading utilities for dataset processing."""

from pathlib import Path
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV into a DataFrame."""
    return pd.read_csv(Path(path))
