"""Load pandas DataFrames into MySQL."""

from __future__ import annotations

import logging

import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def load_replace(engine: Engine, table: str, df: pd.DataFrame) -> int:
    """
    Full refresh: if the table exists, TRUNCATE + INSERT; otherwise CREATE from DataFrame.
    Refine column types in MySQL later when mappings are final.
    """
    rows = len(df)
    insp = inspect(engine)
    if insp.has_table(table):
        if df.empty:
            logger.warning("DataFrame empty; truncating %s only", table)
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE `{table}`"))
        if not df.empty:
            df.to_sql(table, engine, if_exists="append", index=False, chunksize=1000, method="multi")
    else:
        logger.info("Table %s does not exist; creating from DataFrame dtypes", table)
        df.to_sql(table, engine, if_exists="replace", index=False, chunksize=1000, method="multi")
    logger.info("Loaded %s rows into %s (replace)", rows, table)
    return rows
