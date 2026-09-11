from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

POS_PATH = PROJECT_ROOT / "data" / "processed" / "qsr_pos_enriched.csv"
COGS_PATH = PROJECT_ROOT / "data" / "processed" / "menu_cogs_cleaned.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "quality"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def check_numeric_rules(df):

    results = []

    rules = {
        "quantity <= 0": (df["quantity"] <= 0).sum(),
        "unit_price < 0": (df["unit_price"] < 0).sum(),
        "discount < 0": (df["discount"] < 0).sum(),
        "tax < 0": (df["tax"] < 0).sum(),
        "total_amount < 0": (df["total_amount"] < 0).sum(),
    }

    for rule, failures in rules.items():
        results.append({
            "check": rule,
            "failures": int(failures),
            "status": "PASS" if failures == 0 else "FAIL"
        })

    return results


def main():

    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT")
    print("=" * 60)

    pos = pd.read_csv(POS_PATH)
    cogs = pd.read_csv(COGS_PATH)

    report = []

    # Row counts
    report.append({
        "check": "POS row count",
        "failures": 0,
        "status": f"PASS - {len(pos)} rows"
    })

    report.append({
        "check": "COGS row count",
        "failures": 0,
        "status": f"PASS - {len(cogs)} rows"
    })

    # Duplicate orders
    duplicate_orders = pos["order_id"].duplicated().sum()

    report.append({
        "check": "Duplicate order IDs",
        "failures": int(duplicate_orders),
        "status": "PASS" if duplicate_orders == 0 else "FAIL"
    })

    # Missing values
    for column in pos.columns:

        missing = pos[column].isna().sum()

        report.append({
            "check": f"Missing values - {column}",
            "failures": int(missing),
            "status": "PASS" if missing == 0 else f"INFO - {missing}"
        })

    # Numeric rules
    report.extend(check_numeric_rules(pos))

    # Menu matching
    pos_items = set(pos["menu_item"].dropna())
    cogs_items = set(cogs["menu_item"].dropna())

    unmatched = pos_items - cogs_items

    report.append({
        "check": "POS menu items missing from COGS",
        "failures": len(unmatched),
        "status": "PASS" if len(unmatched) == 0 else "FAIL"
    })

    report_df = pd.DataFrame(report)

    output_path = OUTPUT_DIR / "data_quality_report.csv"

    report_df.to_csv(output_path, index=False)

    print("\nQuality checks completed.")
    print(f"Report saved to: {output_path}")

    print("\nSummary:")
    print(report_df["status"].value_counts().to_string())


if __name__ == "__main__":
    main()