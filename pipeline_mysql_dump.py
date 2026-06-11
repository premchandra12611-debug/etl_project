# Pipeline B: MySQL source -> Transform -> MySQL target

import sys

from mysql.connector import Error as MySQLError
from sqlalchemy.exc import OperationalError

from config import (
    MYSQL_CFG,
)
from extract import extract_from_mysql
#from load import load_to_mysql
from load import load_to_postgres
from logger import setup_logger
from transform import clean_and_enrich


log = setup_logger(__name__)


def run() -> None:
    log.info("Pipeline B: MySQL -> PostgreSQL started")
    try:
        raw_df = extract_from_mysql()
        clean_df = clean_and_enrich(raw_df)
        #load_to_mysql(clean_df)
        load_to_postgres(clean_df)
        log.info("Pipeline B completed")
    except OperationalError as exc:
        errno = getattr(exc.orig, "args", [None])[0]
        if errno == 1045:
            log.error(
                "MySQL access denied for user '%s'@'%s' on database '%s'. "
                "Update MYSQL_USER/MYSQL_PASSWORD in .env or grant this user access.",
                MYSQL_CFG["user"],
                MYSQL_CFG["host"],
                MYSQL_CFG["database"],
            )
            sys.exit(1)
        if errno == 1049:
            log.error(
                "MySQL database '%s' does not exist or user '%s' cannot access it. "
                "Create the database or update MYSQL_DATABASE in .env.",
                MYSQL_CFG["database"],
                MYSQL_CFG["user"],
            )
            sys.exit(1)
        log.error(f"Pipeline B failed: {exc}")
        raise
    except MySQLError as exc:
        if exc.errno == 1045:
            log.error(
                "MySQL access denied for user '%s'@'%s' on database '%s'. "
                "Update MYSQL_USER/MYSQL_PASSWORD in .env or grant this user access.",
                MYSQL_CFG["user"],
                MYSQL_CFG["host"],
                MYSQL_CFG["database"],
            )
            sys.exit(1)
        if exc.errno == 1049:
            log.error(
                "MySQL database '%s' does not exist or user '%s' cannot access it. "
                "Create the database or update MYSQL_DATABASE in .env.",
                MYSQL_CFG["database"],
                MYSQL_CFG["user"],
            )
            sys.exit(1)
        log.error(f"Pipeline B failed: {exc}")
        raise
    except Exception as exc:
        log.error(f"Pipeline B failed: {exc}")
        raise


if __name__ == "__main__":
    run()
