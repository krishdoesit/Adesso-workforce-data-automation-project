"""Shared QODBC connection (autocommit, retry, serialized use)."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

import pyodbc

from config.settings import QBODBCSettings

logger = logging.getLogger(__name__)
_lock = threading.Lock()
_conn: pyodbc.Connection | None = None


def _conn_str(settings: QBODBCSettings) -> str:
    if settings.connection_string:
        return settings.connection_string
    if settings.dsn:
        return f"DSN={settings.dsn}"
    driver = settings.driver or "QODBC Driver for QuickBooks"
    return f"DRIVER={{{driver}}};"


def get_connection(settings: QBODBCSettings) -> pyodbc.Connection:
    global _conn
    with _lock:
        if _conn is not None:
            try:
                _conn.cursor().execute("SELECT 1")
            except Exception:
                logger.warning("QODBC reconnecting after unhealthy connection")
                try:
                    _conn.close()
                except Exception:
                    pass
                _conn = None
        if _conn is None:
            last: Exception | None = None
            for attempt in range(1, settings.connect_retries + 1):
                try:
                    _conn = pyodbc.connect(
                        _conn_str(settings),
                        autocommit=settings.autocommit,
                    )
                    logger.info("QODBC connected (attempt %s)", attempt)
                    break
                except Exception as e:
                    last = e
                    logger.exception("QODBC connect failed %s/%s", attempt, settings.connect_retries)
                    if attempt < settings.connect_retries:
                        time.sleep(settings.retry_delay_seconds)
            if _conn is None and last:
                raise last
        assert _conn is not None
        return _conn


def close_connection() -> None:
    global _conn
    with _lock:
        if _conn is not None:
            try:
                _conn.close()
            except Exception:
                logger.exception("Error closing QODBC")
            _conn = None


def run_query(
    settings: QBODBCSettings,
    sql: str,
    parameters: tuple[Any, ...] | list[Any] | None = None,
) -> tuple[list[str], list[tuple[Any, ...]]]:
    with _lock:
        conn = get_connection(settings)
        cur = conn.cursor()
        if parameters:
            cur.execute(sql, parameters)
        else:
            cur.execute(sql)
        cols = [c[0] for c in cur.description] if cur.description else []
        rows = cur.fetchall()
        return cols, rows
