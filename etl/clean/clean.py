import sys
from pathlib import Path

import pandas as pd


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from etl.extract import load_raw_data

# Directory for processed (cleaned) data
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def clean_pos_data(pos_data):
    """Clean POS transaction data."""

    df = pos_data.copy()

    # Missing discount means no recorded discount
    df["discount"] = df["discount"].fillna(0)

    # Preserve missing operational information
    df["service_mode"] = df["service_mode"].fillna("Unknown")

    # Preserve missing payment information
    df["payment_type"] = df["payment_type"].fillna("Unknown")

    # Convert date/time columns
    df["transaction_datetime"] = pd.to_datetime(df["transaction_datetime"])
    df["business_day"] = pd.to_datetime(df["business_day"])

    return df


def clean_menu_cogs(menu_cogs):
    """Clean Menu COGS data."""

    df = menu_cogs.copy()

    df["last_updated"] = pd.to_datetime(df["last_updated"])

    return df


def main():
    pos_data, menu_cogs = load_raw_data()

    cleaned_pos = clean_pos_data(pos_data)
    cleaned_menu_cogs = clean_menu_cogs(menu_cogs)

    # Create processed data directory
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Save cleaned datasets
    pos_output = PROCESSED_DATA_DIR / "qsr_pos_cleaned.csv"
    menu_output = PROCESSED_DATA_DIR / "menu_cogs_cleaned.csv"

    cleaned_pos.to_csv(pos_output, index=False)
    cleaned_menu_cogs.to_csv(menu_output, index=False)

    print("\n" + "=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)

    print("\nPOS DATA")
    print(f"Rows before cleaning: {len(pos_data)}")
    print(f"Rows after cleaning:  {len(cleaned_pos)}")

    print("\nRemaining missing values:")
    print(cleaned_pos.isna().sum())

    print("\nMENU COGS")
    print(f"Rows: {len(cleaned_menu_cogs)}")

    print("\nMissing values:")
    print(cleaned_menu_cogs.isna().sum())

    print("\nProcessed files created:")
    print(pos_output)
    print(menu_output)


if __name__ == "__main__":
    main()