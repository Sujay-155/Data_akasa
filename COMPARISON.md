# Approach Comparison

## Your Single-File Approach vs Current Modular Structure

### Decision: **Hybrid Approach** (Best of Both)

---

## What We Implemented

### 1. **Structure** (Modular - Professional)
```
Data_akasa/
├── data/raw/              # Source data files
├── output/                # Generated KPI reports
├── src/
│   ├── utils/
│   │   ├── config.py     # .env configuration
│   │   └── logger.py     # Logging setup
│   └── inmemory_approach/
│       ├── data_loader.py      # Load & clean functions
│       ├── kpi_calculator.py   # KPI calculation functions
│       └── main.py             # Pipeline orchestration
├── run_pipeline.py        # Simple entry point
├── .env                   # Configuration file
└── requirements.txt       # Dependencies
```

### 2. **Logic** (Your Approach - Superior)
- **Timezone handling**: Asia/Kolkata with proper UTC normalization
- **pandas.read_xml()**: Direct XML parsing (no manual ElementTree)
- **Robust validation**: Column checks, duplicate handling, type coercion
- **Better error handling**: Try-catch with meaningful messages
- **Defensive programming**: Handles edge cases (empty data, NaN values)

### 3. **Configuration** (Your Approach)
- **.env file**: All settings in one place (TZ, paths, TOP_N)
- **No hardcoded values**: Easy to change without touching code

---

## Key Improvements Applied

### From Your Code:
1. **Timezone-aware processing**
   - Local TZ for date boundaries (30-day window)
   - UTC internally for consistency
   
2. **Better data cleaning**
   ```python
   - Trim whitespace from all strings
   - Standardize region names (title case)
   - Handle duplicates (order_id, mobile_number)
   - Convert types with error handling (coerce)
   ```

3. **Improved KPI calculations**
   - `get_repeat_customers`: Counts unique orders per customer
   - `get_monthly_trends`: Timezone-aware month aggregation
   - `get_regional_revenue`: Handles missing regions
   - `get_top_spenders_last_30_days`: Proper 30-day window calculation

4. **Cleaner logging**
   ```
   2025-11-06 16:53:27 | INFO | Loading customers CSV
   2025-11-06 16:53:46 | WARNING | Duplicate order_id detected
   ```

### From Original Structure:
1. **Modularity**: Separate concerns (loading, cleaning, KPI calculation)
2. **Testability**: Each function can be tested independently
3. **Scalability**: Easy to add more KPIs or data sources

---

## How to Run

### Setup (One-time)
```powershell
# Create .env file (if not exists)
Copy-Item .env.example .env

# Install dependencies
py -m pip install -r requirements.txt
```

### Run Pipeline
```powershell
# Option 1: Simple runner
py run_pipeline.py

# Option 2: Direct main
py src/inmemory_approach/main.py
```

### Expected Output
```
2025-11-06 16:53:27 | INFO | Starting Akasa Air - In-memory (pandas) pipeline
2025-11-06 16:53:27 | INFO | Loading customers CSV: ./data/raw/task_DE_new_customers.csv
2025-11-06 16:53:27 | INFO | Customers loaded: 5 rows
2025-11-06 16:53:27 | INFO | Loading orders XML: ./data/raw/task_DE_new_orders.xml
2025-11-06 16:53:28 | INFO | Orders loaded: 10 rows
2025-11-06 16:53:46 | INFO | Customers after cleaning: 5 rows
2025-11-06 16:53:46 | INFO | Orders after cleaning: 3 rows
2025-11-06 16:53:46 | INFO | Calculating KPIs...
2025-11-06 16:53:47 | INFO | Saving reports...

--- Repeat Customers ---
mobile_number  order_count customer_id customer_name region
   9123456781            2    CUST-001   Aarav Mehta   West

--- Monthly Order Trends ---
order_month  order_count
 2025-09-01            1
 2025-10-01            1
 2025-11-01            1

--- Regional Revenue ---
region  revenue
  West  12749.0
 North   8930.0

--- Top Spenders (Last 30 Days) ---
mobile_number  total_spend customer_id customer_name region
   9123456781      12749.0    CUST-001   Aarav Mehta   West
```

---

## Generated Reports (CSV)

All reports saved to `output/` folder:
- `kpi_repeat_customers.csv`
- `kpi_monthly_trends.csv`
- `kpi_regional_revenue.csv`
- `kpi_top_spenders_last_30_days.csv`

---

## Why This Hybrid is Better

### For Interviews:
1. **Shows architecture skills**: Modular design
2. **Demonstrates best practices**: Error handling, logging, validation
3. **Production-ready patterns**: Configuration management, timezone handling
4. **Clean code**: Simple, readable, well-documented

### For Maintenance:
1. **Easy to test**: Each module has focused responsibility
2. **Easy to extend**: Add new KPIs in kpi_calculator.py
3. **Easy to debug**: Structured logging at each step
4. **Easy to configure**: Change .env without code changes

---

## Code Quality Highlights

### Validation
- Column existence checks
- Data type conversions with error handling
- Duplicate detection and removal
- Missing value handling

### Performance
- Efficient pandas operations
- Minimal data copying
- Grouped aggregations

### Maintainability
- Clear function names
- Type hints
- Docstrings
- Consistent formatting
