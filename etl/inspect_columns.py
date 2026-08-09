from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

def read_dataset(filename):
    file_path = RAW_DIR / filename

    if filename.lower().endswith(".csv"):
        return pd.read_csv(file_path)
    elif filename.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

def main():
    files = [
        "qsr_pos_logs.csv",
        "menu_cogs.csv"
    ]

    for file in files:
        df = read_dataset(file)
        print(f"\nDATASET: {file}")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        print("Columns:")
        for col in df.columns:
            print("-", col)
        print("-" * 80)

if __name__ == "__main__":
    main()