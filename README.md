# MySQL ETL Project

This project runs a small ETL pipeline from a raw MySQL table into a cleaned MySQL table.

The pipeline:

1. Extracts raw rows from `sales_analytics.customers`.
2. Cleans and enriches the data with `transform.py`.
3. Loads the cleaned result into `sales_analytics_clean.customers_clean`.

## Project Files

| File | Purpose |
| --- | --- |
| `pipeline_mysql_dump.py` | Main ETL entrypoint and orchestration. |
| `extract.py` | Reads raw rows from the source MySQL table. |
| `transform.py` | Shared cleaning and enrichment logic. |
| `load.py` | Writes cleaned rows to the destination MySQL table. |
| `config.py` | Reads MySQL settings from `.env`. |
| `logger.py` | Central logging setup used by the pipeline modules. |
| `mysql_utils.py` | MySQL URL, SQLAlchemy engine, and database creation helpers. |
| `raw_sales_analytics_seed.sql` | Raw sample MySQL data that can be imported before running the pipeline. |
| `requirements.txt` | Python package dependencies. |
| `.gitignore` | Keeps secrets, virtualenvs, caches, and generated exports out of Git. |

## Requirements

- Python 3.14 or compatible Python 3 version
- MySQL Server running locally
- A MySQL user with permission to read the source database and create/write the destination database

## Setup

Create and activate a virtual environment:

```powershell
python -m venv etl_project_venv
.\etl_project_venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=sales_analytics
MYSQL_TABLE=customers

MYSQL_DST_DATABASE=sales_analytics_clean
MYSQL_DST_TABLE=customers_clean
```

Do not commit `.env`; it contains local credentials and is ignored by `.gitignore`.

## Import Raw Data

The seed file creates the raw source database and table used by the pipeline.

Import it with the MySQL CLI:

```powershell
mysql -u root -p < raw_sales_analytics_seed.sql
```

Or open `raw_sales_analytics_seed.sql` in MySQL Workbench and run the full script.

Warning: the seed file starts with:

```sql
DROP DATABASE IF EXISTS `sales_analytics`;
```

That means importing it will replace the existing `sales_analytics` database.

## Run The Pipeline

From the project root:

```powershell
python pipeline_mysql_dump.py
```

Expected result with the provided seed data:

```text
Pipeline B: MySQL -> MySQL started
[EXTRACT] 12 rows from MySQL 'customers'
[TRANSFORM] 6 rows kept  (6 dropped)
[LOAD-MySQL] 6 rows -> `sales_analytics_clean`.`customers_clean`
Pipeline B completed
```

The destination database is created automatically if it does not already exist.

## Transformation Logic

`transform.py` performs these steps:

1. Normalizes column names to lowercase snake_case.
2. Drops duplicate rows by `id` when an `id` column exists.
3. Parses date-like columns such as `order_date` and `created_at`.
4. Drops rows missing critical fields: `id`, `order_date`, or `customer_id`.
5. Converts `quantity`, `amount`, and `unit_price` to numeric values.
6. Adds `total_amount = quantity * unit_price`.
7. Removes rows where `quantity <= 0` or `amount < 0`.
8. Adds `_etl_loaded_at` with the pipeline load timestamp.

The provided seed SQL includes intentionally messy rows so these rules are visible after the pipeline runs.

## Useful MySQL Checks

Check the raw source row count:

```sql
SELECT COUNT(*) FROM sales_analytics.customers;
```

Check the cleaned destination row count:

```sql
SELECT COUNT(*) FROM sales_analytics_clean.customers_clean;
```

Preview cleaned data:

```sql
SELECT * FROM sales_analytics_clean.customers_clean;
```

## Troubleshooting

If you see `Access denied for user`, check `MYSQL_USER`, `MYSQL_PASSWORD`, and the user's MySQL grants.

If you see `database does not exist`, confirm that `.env` uses the same source database name created by the SQL seed:

```env
MYSQL_DATABASE=sales_analytics
```

If `mysql` is not recognized in PowerShell, import the seed file through MySQL Workbench or add the MySQL `bin` directory to your PATH.

author:premchandra