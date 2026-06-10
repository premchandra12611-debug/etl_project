import pandas as pd

from config import MYSQL_DST_CFG, MYSQL_DST_TABLE
from logger import setup_logger
from mysql_utils import create_mysql_engine, ensure_database_exists


log = setup_logger(__name__)


def load_to_mysql(df: pd.DataFrame) -> None:
    """Write the clean DataFrame back into MySQL using SQLAlchemy.

    Uses 'replace' to truncate and insert on every run.
    """
    cfg = MYSQL_DST_CFG
    ensure_database_exists(cfg)
    engine = create_mysql_engine(cfg)

    with engine.begin() as conn:
        df.to_sql(
            name=MYSQL_DST_TABLE,
            con=conn,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi",
        )
    log.info(
        f"[LOAD-MySQL] {len(df):,} rows -> "
        f"`{cfg['database']}`.`{MYSQL_DST_TABLE}`"
    )
