from pathlib import Path
import pandas as pd


# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Location of raw datasets
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_pos_data():
    """Load the raw POS transaction data."""
    file_path = RAW_DATA_DIR / "qsr_pos_logs.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"POS dataset not found: {file_path}")

    return pd.read_csv(file_path)


def load_menu_cogs():
    """Load the raw menu and COGS data."""
    file_path = RAW_DATA_DIR / "menu_cogs.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"Menu COGS dataset not found: {file_path}")

    return pd.read_csv(file_path)


def load_raw_data():
    """Load all raw datasets."""
    pos_data = load_pos_data()
    menu_cogs = load_menu_cogs()

    return pos_data, menu_cogs


if __name__ == "__main__":
    pos_data, menu_cogs = load_raw_data()

    print("POS data loaded successfully.")
    print(f"POS rows: {len(pos_data)}")
    print(f"POS columns: {len(pos_data.columns)}")

    print("\nMenu COGS data loaded successfully.")
    print(f"Menu rows: {len(menu_cogs)}")
    print(f"Menu columns: {len(menu_cogs.columns)}")