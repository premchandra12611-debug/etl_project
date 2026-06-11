from urllib.parse import quote_plus
from sqlalchemy import create_engine


def postgres_url(cfg: dict) -> str:
    return (
        f"postgresql+psycopg2://{quote_plus(cfg['user'])}:"
        f"{quote_plus(cfg['password'])}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}"
    )


def create_postgres_engine(cfg: dict):
    return create_engine(
        postgres_url(cfg),
        pool_pre_ping=True
    )