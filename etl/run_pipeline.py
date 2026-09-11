import subprocess
import sys


def run_step(description, command):
    print("\n" + "=" * 70)
    print(description)
    print("=" * 70)

    result = subprocess.run(
        [sys.executable] + command,
        check=False
    )

    if result.returncode != 0:
        print(f"\nFAILED: {description}")
        sys.exit(result.returncode)

    print(f"\nCOMPLETED: {description}")


def main():

    print("\n" + "=" * 70)
    print("RESTAURANT BUSINESS ANALYTICS - FULL PIPELINE")
    print("=" * 70)

    steps = [

        # -------------------------
        # DATA PREPARATION
        # -------------------------

        ("1. EXTRACT RAW DATA",
         ["etl/extract.py"]),

        ("2. CLEAN DATA",
         ["etl/clean/clean.py"]),

        ("3. TRANSFORM DATES",
         ["etl/transform/transform_dates.py"]),

        # -------------------------
        # DATABASE
        # -------------------------

        ("4. LOAD DATABASE",
         ["database/load_database.py"]),

        # -------------------------
        # SALES ANALYSIS
        # -------------------------

        ("5. DAILY SALES ANALYSIS",
         ["etl/transform/sales_daily.py"]),

        ("6. MONTHLY SALES ANALYSIS",
         ["etl/transform/sales_monthly.py"]),

        ("7. WEEKDAY SALES ANALYSIS",
         ["etl/transform/sales_weekday.py"]),

        ("8. SALES TREND ANALYSIS",
         ["etl/transform/sales/sales_trend_analysis.py"]),

        # -------------------------
        # OPERATIONS
        # -------------------------

        ("9. CATEGORY ANALYSIS",
         ["etl/transform/category_analysis.py"]),

        ("10. DAYPART ANALYSIS",
         ["etl/transform/daypart_analysis.py"]),

        ("11. STORE ANALYSIS",
         ["etl/transform/store_analysis.py"]),

        ("12. PAYMENT ANALYSIS",
         ["etl/transform/payment_analysis.py"]),

        ("13. SERVICE MODE ANALYSIS",
         ["etl/transform/service_mode_analysis.py"]),

        ("14. ORDER BEHAVIOR ANALYSIS",
         ["etl/transform/order_behavior.py"]),

        ("15. MODIFIER ANALYSIS",
         ["etl/transform/modifier_analysis.py"]),

        ("16. OPERATIONS ANALYSIS",
         ["etl/transform/operations_analysis.py"]),

        # -------------------------
        # MENU + PROFITABILITY
        # -------------------------

        ("17. MENU ANALYSIS",
         ["etl/transform/menu_analysis.py"]),

        ("18. MENU COST ANALYSIS",
         ["etl/transform/menu_cost_analysis.py"]),

        ("19. MENU MATRIX ANALYSIS",
         ["etl/transform/menu_matrix.py"]),

        ("20. PROFITABILITY ANALYSIS",
         ["etl/transform/profitability_analysis.py"]),

        ("21. PROFITABILITY SUMMARY",
         ["etl/transform/profitability_summary.py"]),

        # -------------------------
        # STRATEGIC ANALYSIS
        # -------------------------

        ("22. STRATEGIC ANALYSIS",
         ["etl/transform/strategic/strategic_analysis.py"]),

        # -------------------------
        # DASHBOARD DATA
        # -------------------------

        ("23. CREATE DASHBOARD DATASETS",
         ["etl/transform/dashboard/dashboard_master.py"]),
    ]

    for description, command in steps:
        run_step(description, command)

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()