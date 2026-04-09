"""Load settings from environment (.env optional)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
load_dotenv(PROJECT_ROOT / ".env")


def _g(key: str, default: str | None = None) -> str | None:
    v = os.environ.get(key, default)
    return v if v not in ("", None) else default


@dataclass(frozen=True)
class QBODBCSettings:
    dsn: str | None
    driver: str | None
    connection_string: str | None
    autocommit: bool = True
    connect_retries: int = 3
    retry_delay_seconds: float = 2.0


@dataclass(frozen=True)
class MySQLSettings:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass(frozen=True)
class AppSettings:
    qb: QBODBCSettings
    mysql: MySQLSettings
    log_level: str
    pipeline_config_path: Path


def load_settings(pipeline_config: str | Path | None = None) -> AppSettings:
    path = (
        Path(pipeline_config).resolve()
        if pipeline_config
        else PROJECT_ROOT / "config" / "pipeline.yaml"
    )
    return AppSettings(
        qb=QBODBCSettings(
            dsn=_g("QB_ODBC_DSN"),
            driver=_g("QB_ODBC_DRIVER", "QODBC Driver for QuickBooks"),
            connection_string=_g("QB_ODBC_CONNECTION_STRING"),
        ),
        mysql=MySQLSettings(
            host=_g("MYSQL_HOST", "127.0.0.1") or "127.0.0.1",
            port=int(_g("MYSQL_PORT", "3306") or "3306"),
            user=_g("MYSQL_USER", "") or "",
            password=_g("MYSQL_PASSWORD", "") or "",
            database=_g("MYSQL_DATABASE", "") or "",
        ),
        log_level=(_g("LOG_LEVEL", "INFO") or "INFO").upper(),
        pipeline_config_path=path,
    )
