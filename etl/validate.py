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

def validate_qsr_pos(df):
    issues = {}

    issues["negative_quantity"] = int((df["quantity"] < 0).sum()) if "quantity" in df.columns else None
    issues["zero_quantity"] = int((df["quantity"] == 0).sum()) if "quantity" in df.columns else None
    issues["negative_unit_price"] = int((df["unit_price"] < 0).sum()) if "unit_price" in df.columns else None
    issues["negative_discount"] = int((df["discount"] < 0).sum()) if "discount" in df.columns else None
    issues["negative_tax"] = int((df["tax"] < 0).sum()) if "tax" in df.columns else None
    issues["negative_total_amount"] = int((df["total_amount"] < 0).sum()) if "total_amount" in df.columns else None

    return issues

def validate_restaurant_data(df):
    issues = {}

    issues["negative_count"] = int((df["Count"] < 0).sum()) if "Count" in df.columns else None
    issues["zero_count"] = int((df["Count"] == 0).sum()) if "Count" in df.columns else None

    return issues

def main():
    qsr = read_dataset("qsr_pos_logs.csv")
    rest = read_dataset("Restaurant_Data.xlsx")

    print("QSR POS Validation:")
    print(validate_qsr_pos(qsr))
    print("-" * 60)

    print("Restaurant Data Validation:")
    print(validate_restaurant_data(rest))
    print("-" * 60)

if __name__ == "__main__":
    main()