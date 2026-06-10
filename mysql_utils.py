from urllib.parse import quote_plus

from sqlalchemy import create_engine


def quote_identifier(value: str) -> str:
    return f"`{value.replace('`', '``')}`"


def mysql_url(cfg: dict, include_database: bool = True) -> str:
    database = f"/{quote_plus(cfg['database'])}" if include_database else ""
    return (
        f"mysql+pymysql://{quote_plus(cfg['user'])}:{quote_plus(cfg['password'])}"
        f"@{cfg['host']}:{cfg['port']}{database}"
    )


def create_mysql_engine(cfg: dict, include_database: bool = True):
    return create_engine(mysql_url(cfg, include_database=include_database), pool_pre_ping=True)


def ensure_database_exists(cfg: dict) -> None:
    server_engine = create_mysql_engine(cfg, include_database=False)
    with server_engine.begin() as conn:
        conn.exec_driver_sql(
            f"CREATE DATABASE IF NOT EXISTS {quote_identifier(cfg['database'])}"
        )
