from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUALITY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "quality"
    / "data_quality_report.csv"
)


def load_quality_report():

    if not QUALITY_PATH.exists():
        return None

    return pd.read_csv(QUALITY_PATH)


def get_quality_summary():

    df = load_quality_report()

    if df is None:
        return {
            "available": False,
            "checks": 0,
            "failed": 0
        }

    failed = (
        df["status"]
        .astype(str)
        .str.startswith("FAIL")
        .sum()
    )

    return {
        "available": True,
        "checks": len(df),
        "failed": int(failed)
    }