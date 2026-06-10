import pandas as pd

from config import MYSQL_CFG, MYSQL_TABLE
from logger import setup_logger
from mysql_utils import create_mysql_engine


log = setup_logger(__name__)


def extract_from_mysql(query: str = None) -> pd.DataFrame:
    sql = query or f"SELECT * FROM `{MYSQL_TABLE}`"
    engine = create_mysql_engine(MYSQL_CFG)
    with engine.begin() as conn:
        df = pd.read_sql(sql, conn)
    log.info(f"[EXTRACT] {len(df):,} rows from MySQL '{MYSQL_TABLE}'")
    return df
