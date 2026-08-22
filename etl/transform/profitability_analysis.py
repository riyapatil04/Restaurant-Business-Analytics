import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


# Inputs
POS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "qsr_pos_enriched.csv"
)

MENU_COGS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "menu_cogs_cleaned.csv"
)

# Output
OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
)

OUTPUT_FILE = OUTPUT_DIR / "profitability_analysis.csv"


def main():
    print("\n" + "=" * 60)
    print("PROFITABILITY ANALYSIS (SETUP)")
    print("=" * 60)

    pos = pd.read_csv(POS_FILE)
    cogs = pd.read_csv(MENU_COGS_FILE)

    print("\nPOS shape:", pos.shape)
    print("Menu COGS shape:", cogs.shape)

    print("\nPOS columns:")
    print(pos.columns.tolist())

    print("\nMenu COGS columns:")
    print(cogs.columns.tolist())

    print("\nMenu items in POS:")
    print(pos["menu_item"].nunique())

    print("\nMenu items in COGS:")
    print(cogs["menu_item"].nunique())

    print("\nSaved path (for later):")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()