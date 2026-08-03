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
        "Restaurant_Data.xlsx"
    ]

    for file in files:
        df = read_dataset(file)
        print(f"{file}: {df.shape[0]} rows, {df.shape[1]} columns")
        print(df.head(3))
        print("-" * 60)

if __name__ == "__main__":
    main()