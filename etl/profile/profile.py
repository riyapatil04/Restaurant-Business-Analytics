import sys
from pathlib import Path

import pandas as pd


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from etl.extract import load_raw_data


def profile_dataframe(df, dataset_name):
    """Generate a basic data profiling report."""

    print("\n" + "=" * 60)
    print(f"DATASET: {dataset_name}")
    print("=" * 60)

    # Basic structure
    print("\n--- Basic Information ---")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Column information
    print("\n--- Column Information ---")

    column_info = pd.DataFrame({
        "column": df.columns,
        "data_type": df.dtypes.astype(str).values,
        "missing_values": df.isnull().sum().values,
        "missing_percentage": (
            df.isnull().mean().values * 100
        ).round(2),
        "unique_values": df.nunique().values
    })

    print(column_info.to_string(index=False))

    # Duplicate rows
    print("\n--- Duplicate Rows ---")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    # Numerical statistics
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:
        print("\n--- Numerical Summary ---")
        print(
            df[numerical_columns]
            .describe()
            .T
            .to_string()
        )

    # Categorical summary
    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    if len(categorical_columns) > 0:
        print("\n--- Categorical Summary ---")

        for column in categorical_columns:
            print(f"\n{column}:")
            print(df[column].value_counts(dropna=False).head(10))


def main():
    pos_data, menu_cogs = load_raw_data()

    profile_dataframe(
        pos_data,
        "QSR POS Logs"
    )

    profile_dataframe(
        menu_cogs,
        "Menu COGS"
    )


if __name__ == "__main__":
    main()