import os
import sys

from dotenv import load_dotenv


load_dotenv()

REQUIRED_ENV_VARS = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE", "MYSQL_DST_DATABASE", "PG_HOST", "PG_PORT", "PG_USER", "PG_PASSWORD", "PG_DATABASE"]
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    print(f"ERROR: Missing required environment variables in your .env file: {', '.join(missing_vars)}")
    print("Please verify your .env file exists and contains these keys.")
    sys.exit(1)

try:
    mysql_port = int(os.getenv("MYSQL_PORT", 3306))
except ValueError:
    print("ERROR: MYSQL_PORT must be a number.")
    sys.exit(1)

MYSQL_CFG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": mysql_port,
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "customers")

MYSQL_DST_CFG = {**MYSQL_CFG, "database": os.getenv("MYSQL_DST_DATABASE")}
MYSQL_DST_TABLE = os.getenv("MYSQL_DST_TABLE", "customers_clean")


PG_CFG = {
    "host": os.getenv("PG_HOST"),
    "port": int(os.getenv("PG_PORT", 5432)),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "database": os.getenv("PG_DATABASE"),
}