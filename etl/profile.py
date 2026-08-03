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

def profile_dataframe(df, name):
    print(f"\nDATASET: {name}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nColumn Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isna().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nUnique Values Per Column:")
    print(df.nunique())

    print("\nNumeric Summary:")
    print(df.describe(include="number").T)

    print("\nSample Rows:")
    print(df.head(3))
    print("-" * 80)

def main():
    files = [
        "qsr_pos_logs.csv",
        "Restaurant_Data.xlsx"
    ]

    for file in files:
        df = read_dataset(file)
        profile_dataframe(df, file)

if __name__ == "__main__":
    main()