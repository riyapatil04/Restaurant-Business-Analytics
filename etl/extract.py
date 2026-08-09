from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")


def read_pos():
    return pd.read_csv(RAW_DIR / "qsr_pos_logs.csv")


def read_menu():
    return pd.read_csv(RAW_DIR / "menu_cogs.csv")


def main():
    pos = read_pos()
    menu = read_menu()

    print("POS dataset:")
    print(f"  Rows: {pos.shape[0]}, Columns: {pos.shape[1]}")
    print(pos.head(3))
    print("-" * 60)

    print("Menu COGS dataset:")
    print(f"  Rows: {menu.shape[0]}, Columns: {menu.shape[1]}")
    print(menu.head(3))
    print("-" * 60)


if __name__ == "__main__":
    main()