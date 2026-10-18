import pytest
from shopper_composite import transform
from pathlib import Path
from datetime import date
import csv

@pytest.fixture
def csv_path():
    return Path('/home/lcalleja/stats_mini.csv')

def test_csv_exists(csv_path):
    rows: list[tuple] = []
    with open(csv_path, newline="") as f:
        for rec in csv.DictReader(f):
            rows.append(rec)
    assert len(rows) > 1


def test_transform(csv_path):
#function signature: transform_rows(csv_path: str | Path, after: date | None = None)
    rows_results = transform.transform_rows(csv_path)
    type_list = [type(i) for i in rows_results[0]]

    assert type_list == [date, int, int, int, int, int]



