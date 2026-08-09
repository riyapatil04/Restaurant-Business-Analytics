import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from etl.extract import load_raw_data


def main():
    _, menu_cogs = load_raw_data()

    menu_cogs["ingredient_formula"] = (
        menu_cogs["ingredient_cost"]
        / menu_cogs["selling_price"]
        * 100
    )

    menu_cogs["total_cogs_formula"] = (
        menu_cogs["total_cogs"]
        / menu_cogs["selling_price"]
        * 100
    )

    result = menu_cogs[
        [
            "menu_item",
            "selling_price",
            "ingredient_cost",
            "total_cogs",
            "food_cost_pct",
            "ingredient_formula",
            "total_cogs_formula",
        ]
    ]

    print(result.to_string(index=False))


if __name__ == "__main__":
    main()