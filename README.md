# Restaurant Business Analytics

An end-to-end restaurant analytics application that transforms point-of-sale data into actionable business insights using Python, SQL, SQLite, Pandas, and Streamlit.

## Project Overview

Restaurant owners generate large amounts of transactional data, but raw POS logs are difficult to interpret directly.

This project converts raw restaurant transaction data into:

- Revenue and sales trends
- Menu performance analysis
- Profitability analysis
- Store performance
- Daypart analysis
- Payment and service-mode analysis
- Order behavior analysis
- Menu cost analysis
- Menu engineering matrix
- Operational insights
- Data-quality checks
- Interactive business dashboards

## Architecture

```text
Raw POS Data
     |
     v
   Extract
     |
     v
    Clean
     |
     v
  Transform
     |
     +------------------+
     |                  |
     v                  v
Data Quality       SQLite Database
     |                  |
     +--------+---------+
              |
              v
          Analytics
              |
              v
        Streamlit Dashboard
```

## Tech Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Streamlit
- Matplotlib / Plotly
- Git & GitHub

## Dataset

The project uses restaurant POS transaction data and menu cost information.

The main POS fields include:

- Order ID
- Store ID
- Transaction datetime
- Business day
- Daypart
- Service mode
- Menu item
- Modifier
- Quantity
- Unit price
- Discount
- Tax
- Total amount
- Payment type

Menu cost data includes:

- Menu item
- Category
- Selling price
- Ingredient cost
- Packaging cost
- Labor cost
- Total COGS
- Food cost percentage
- Supplier

## ETL Pipeline

The project contains an automated pipeline:

```text
Extract
   ↓
Clean
   ↓
Transform
   ↓
Load SQLite Database
   ↓
Run Analytics
   ↓
Generate Dashboard Datasets
```

Run the complete pipeline with:

```bash
python etl/run_pipeline.py
```

## Database

The project uses SQLite with the following main tables:

- `restaurants`
- `menu_items`
- `orders`
- `order_items`

Relationships are enforced using primary keys and foreign keys.

## Data Quality

A dedicated data-quality process checks:

- Missing values
- Duplicate orders
- Invalid quantities
- Invalid prices
- Invalid discounts
- Invalid taxes
- Invalid totals
- POS/COGS menu-item matching

Run:

```bash
python etl/quality_report.py
```

## Dashboard

The Streamlit application provides interactive business dashboards for:

- Executive Overview
- Sales Analysis
- Menu & Profitability
- Operational analysis
- Strategic insights

Run the application with:

```bash
streamlit run dashboard/app.py
```

The application also provides a pipeline refresh mechanism so updated source data can be processed again without manually running every analysis script.

## Key Business Questions

The application is designed to answer questions such as:

- How is revenue changing over time?
- Which days perform best?
- Which menu items generate the most revenue?
- Which menu items generate the most gross profit?
- Which items have high demand but weaker margins?
- Which menu items are potential Stars, Hidden Gems, Problem Children, or Dogs?
- Which stores perform best?
- Which dayparts generate the most revenue?
- Which service channels perform differently?
- What operational areas require attention?

## Project Structure

```text
Restaurant-Business-Analytics/
│
├── dashboard/
│   ├── app.py
│   ├── pipeline_runner.py
│   ├── data_quality.py
│   └── pages/
│
├── database/
│   ├── schema.sql
│   ├── load_database.py
│   └── restaurant.db
│
├── data/
│   ├── raw/
│   └── processed/
│
├── etl/
│   ├── extract.py
│   ├── clean/
│   ├── investigate/
│   ├── transform/
│   ├── quality_report.py
│   └── run_pipeline.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Future Improvements

Potential future versions can add:

- Real restaurant/POS database integration
- Automated scheduled ingestion
- Forecasting
- Customer segmentation
- Recommendation systems
- Demand prediction
- Inventory optimization
- Ingredient cost monitoring
- Anomaly detection
- Authentication and multi-restaurant support

## Project Goal

The goal is to demonstrate how raw transactional data can be transformed into a complete analytics product rather than simply creating isolated charts.

The project combines:

**Data Engineering + SQL + Data Analysis + Business Intelligence + Interactive Visualization**