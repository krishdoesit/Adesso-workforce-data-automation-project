"""
QuickBooks (QODBC) -> MySQL pipeline.

Usage (on the client PC with QuickBooks + ODBC configured):
  python main.py              # all enabled jobs
  python main.py --job usa_inventory_evaluation_summary
"""

from __future__ import annotations

import argparse
import sys

from config.settings import load_settings
from db.qb_connection import close_connection
from services.pipeline_config import load_pipeline_config
from services.runner import run_job
from utils.logger import setup_logging


def main() -> int:
    p = argparse.ArgumentParser(description="QODBC to MySQL sync")
    p.add_argument(
        "--job",
        help="Run only this job id (must exist in config/pipeline.yaml)",
    )
    p.add_argument(
        "--no-csv",
        action="store_true",
        help="Do not write output/<job_id>.csv",
    )
    args = p.parse_args()

    settings = load_settings()
    setup_logging(settings.log_level)

    jobs = load_pipeline_config(settings.pipeline_config_path)
    if args.job:
        jobs = [j for j in jobs if j.id == args.job]
        if not jobs:
            print(f"No job named {args.job!r}", file=sys.stderr)
            return 1
    else:
        jobs = [j for j in jobs if j.enabled]

    if not jobs:
        print("No jobs to run (check pipeline.yaml enabled flags).", file=sys.stderr)
        return 1

    try:
        for job in jobs:
            run_job(settings, job, save_csv=not args.no_csv)
    finally:
        close_connection()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
