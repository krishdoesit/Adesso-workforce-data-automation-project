"""SQLAlchemy engine for MySQL."""

from __future__ import annotations

import logging
from functools import lru_cache
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from config.settings import MySQLSettings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_engine(settings: MySQLSettings) -> Engine:
    u = quote_plus(settings.user)
    p = quote_plus(settings.password)
    url = f"mysql+pymysql://{u}:{p}@{settings.host}:{settings.port}/{settings.database}"
    eng = create_engine(url, pool_pre_ping=True, pool_recycle=3600)
    logger.info("MySQL engine: %s / %s", settings.host, settings.database)
    return eng
