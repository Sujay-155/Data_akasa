# MySQL Database Implementation - Summary

## What Was Implemented

### 1. Database Schema (`database/schema.sql`)
- **customers** table with fields:
  - customer_id (Primary Key)
  - customer_name
  - mobile_number (indexed)
  - region (indexed)
  - created_at timestamp
  
- **orders** table with fields:
  - order_id (Primary Key)
  - mobile_number (indexed)
  - sku_count
  - total_amount (indexed)
  - order_date_time (indexed)
  - created_at timestamp

### 2. SQL Queries (`database/queries.sql`)
- Repeat Customers query (JOIN + GROUP BY + HAVING)
- Monthly Trends query (DATE_FORMAT + GROUP BY)
- Regional Revenue query (COALESCE + SUM + LEFT JOIN)
- Top Spenders query (DATE_SUB + INTERVAL + LIMIT)

### 3. Data Loader (`src/db_approach/load_data.py`)
- `get_connection()` - Creates MySQL connection
- `create_tables()` - Executes schema.sql
- `load_customers_to_db()` - Loads CSV data with UPSERT
- `load_orders_to_db()` - Loads XML data with UPSERT and data cleaning
- Handles duplicates with `ON DUPLICATE KEY UPDATE`

### 4. KPI Queries (`src/db_approach/kpi_queries.py`)
- `get_repeat_customers()` - Returns DataFrame of repeat customers
- `get_monthly_trends()` - Returns DataFrame of monthly order counts
- `get_regional_revenue()` - Returns DataFrame of revenue by region
- `get_top_spenders_last_30_days()` - Returns top N spenders
- `calculate_all_kpis()` - Orchestrates all KPI calculations

### 5. Main Pipeline (`src/db_approach/main.py`)
- `save_reports()` - Saves KPI results to CSV files (prefixed with `db_`)
- `display_results()` - Prints formatted results to console
- `main()` - Complete pipeline: connect → create tables → load data → calculate KPIs → save reports

### 6. Runner Script (`run_db_pipeline.py`)
- Entry point for database approach
- Usage: `py run_db_pipeline.py`


## Database Configuration

Update `.env` file with your MySQL credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=akasa_data
DB_USER=root
DB_PASSWORD=your_password
```

## Running the Database Pipeline

1. Ensure MySQL server is running
2. Update `.env` with MySQL credentials
3. Run: `py run_db_pipeline.py`

## Output Files

Database approach creates separate reports:
- `output/db_repeat_customers.csv`
- `output/db_monthly_trends.csv`
- `output/db_regional_revenue.csv`
- `output/db_top_spenders_last_30_days.csv`

