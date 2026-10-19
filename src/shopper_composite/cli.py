"""Command-line entry point for the daily check-in ingest."""

import logging.config
import sys
from argparse import ArgumentParser
from datetime import date
from pathlib import Path

from shopper_composite import db_connector, fetch, transform
from shopper_composite.logging_reference import LOGGING

'''
1. Grab the latest date from the db
2. compose the report command for plum
3. execute that command on the command line of radish
4. conduct any ETL necessary
5. insert records into db (radish)
'''


def build_parser() -> ArgumentParser:
    p = ArgumentParser(
        prog="shopper-ingest",
        description="Fetch check-in stats from plum and upsert into shopper_log.",
    )
    p.add_argument(
        "--download-path",
        type=Path,
        default=Path("/home/lcalleja/stats.csv"),
        help="where wget writes the plum CSV",
    )
    p.add_argument(
        "--secrets",
        type=Path,
        default=Path("/home/lcalleja/shopper_composite/secrets.yaml"),
        help="YAML with host/user/password/database/port",
    )
    p.add_argument("--table", default="shopper_log", help="destination table")
    p.add_argument(
        "--start",
        type=date.fromisoformat,
        default=date(2023, 2, 3),
        help="start date used only when the table is empty (YYYY-MM-DD)",
    )
    return p


def main() -> int:
    args = build_parser().parse_args()
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(__name__)

    creds = db_connector.get_config(str(args.secrets))
    # connect() is a context manager; latest_date() has its own with block for the cursor
    with db_connector.connect(creds) as conn:
        latest = db_connector.latest_date(conn, args.table)
        start = latest if latest is not None else args.start
        start_str = start.isoformat()

        fetch.download2(args.download_path, start_str)

        rows = transform.transform_rows(args.download_path, after=latest)
        rows_written = 0
        if rows:
            rows_written = db_connector.append(conn, args.table, rows)
            logger.debug("wrote %d rows to %s", rows_written, args.table)

    return 0


if __name__ == "__main__":
    sys.exit(main())
