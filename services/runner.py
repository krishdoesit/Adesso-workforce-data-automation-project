"""Run one pipeline job: QODBC -> pandas -> optional column_map -> MySQL."""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pandas as pd

from config.settings import OUTPUT_DIR, AppSettings
from db.mysql_connection import get_engine
from db.qb_connection import run_query
from queries.qb_sql_registry import REGISTERED_SQL
from services.pipeline_config import JobConfig
from services.sync_service import load_replace

logger = logging.getLogger(__name__)


def _resolve_sql(job: JobConfig) -> str:
    if job.source.type != "registered_sql":
        raise ValueError(f"Unsupported source.type: {job.source.type}")
    name = job.source.query_name
    if not name or name not in REGISTERED_SQL:
        raise KeyError(f"Unknown query_name: {name!r}. Add it to queries/qb_sql_registry.py")
    return REGISTERED_SQL[name]


def run_job(settings: AppSettings, job: JobConfig, save_csv: bool = True) -> int:
    sql = _resolve_sql(job)
    t0 = time.perf_counter()
    cols, rows = run_query(settings.qb, sql)
    df = pd.DataFrame.from_records(rows, columns=cols)
    elapsed = time.perf_counter() - t0
    logger.info("Job %s: qb rows=%s elapsed=%.2fs", job.id, len(df), elapsed)

    if job.column_map:
        df = df.rename(columns=job.column_map)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if save_csv:
        out = OUTPUT_DIR / f"{job.id}.csv"
        df.to_csv(out, index=False)
        logger.info("Wrote %s", out)

    if job.target.load_mode != "replace":
        raise NotImplementedError("Only load_mode=replace is implemented for now.")

    engine = get_engine(settings.mysql)
    return load_replace(engine, job.target.mysql_table, df)
