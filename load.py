import pandas as pd

#from config import MYSQL_DST_CFG, MYSQL_DST_TABLE
from logger import setup_logger
#from mysql_utils import create_mysql_engine, ensure_database_exists
from config import PG_CFG
from postgres_utils import create_postgres_engine

log = setup_logger(__name__)


def load_to_postgres(df: pd.DataFrame) -> None:
    """Write the clean DataFrame back into PostgreSQL using SQLAlchemy.

    Uses 'replace' to truncate and insert on every run.
    """
    # cfg = MYSQL_DST_CFG
    # ensure_database_exists(cfg)
    # engine = create_mysql_engine(cfg)
    cfg = PG_CFG
    engine = create_postgres_engine(cfg)

    with engine.begin() as conn:
        df.to_sql(
            name="customers_clean",
            con=conn,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi",
        )
    log.info(
    f"[LOAD-PostgreSQL] {len(df):,} rows -> "
    f"{cfg['database']}.customers_clean"
)
    # log.info(
    #     f"[LOAD-PostgreSQL] {len(df):,} rows -> "
    #     f"`{cfg['database']}`.`{cfg['table']}`"
    # )
