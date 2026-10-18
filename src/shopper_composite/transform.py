#%%
from pathlib import Path
import csv
import logging
from datetime import date

'''
handle all data transformations here, this is then passed back to db_connector for the writing process

column names for table shooper_log: date,ghfc,trial,psfc,cbfc,visitor
'''
logger = logging.getLogger(__name__)

#columns are in the order expected
INT_COLS = ("ghfc", "trial", "psfc", "cbfc", "visitor")

def _to_smallint(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None       # becomes SQL NULL
    n = int(value)        # raises ValueError on bad data
    
    return n


def transform_rows(csv_path: str | Path, after: date | None = None) -> list[tuple]:
    """Single pass: parse, type-convert, and (optionally) drop rows already in the DB.
    order expected: (`date`,`ghfc`,`trial`,`psfc`,`cbfc`,`visitor`)"""
    rows: list[tuple] = []
    with open(csv_path, newline="") as f:
        for lineno, rec in enumerate(csv.DictReader(f), start=2):  # line 1 is the header
            try:
                d = date.fromisoformat(rec["date"].strip())
                if after is not None and d <= after:
                    continue                                    # skip existing rows
                rows.append((d, *(_to_smallint(rec[c]) for c in INT_COLS)))
            except (ValueError, KeyError):
                logger.exception("bad row at line %d: %r", lineno, rec)
                raise
    return rows

def transform_rows2(csv_path: str):
#this will get ingested by db_connectot append(), via sql connection cursor executemany(sql, rows)
    with open(csv_path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row)
        return data

#transform_rows(Path('/home/lcalleja/stats_mini.csv'))
# %%
