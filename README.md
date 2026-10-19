wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01

Per Andy Nelson: Yeah you could do that with a local daemon that fetches the daily logs

Python modules that allow for terminal commands:
'''
import subprocess as sp

process = sp.Popen(["your_cmd"]...)
process.wait() #Waits for command completion
'''

shopper_log table schema:
date: date (format ='YYYY-MM-DD')
ghfc: smallint
trial: smallint
psfc: smallint
cbfc: smallint
visitor: smallint

CREATE TABLE IF NOT EXISTS shopper_log
(date date UNIQUE KEY,
ghfc smallint,
trial smallint,
psfc smallint,
cbfc smallint,
visitor smallint);

first date of data from check-in desk:
2023-02-03,5,0,16,3,1

INSERT INTO shopper_log (date, ghfc, trial, psfc, cbfc, visitor) VALUES ('2023-02-03',5,0,16,3,1);

## Module synopses (`src/shopper_composite/`)

### `__init__.py`
Package marker. Defines a placeholder `main()` that prints a greeting; it is the target of the `shopper-composite` console script in `pyproject.toml` but is not part of the ingest flow (`cli.main()` is).

### `cli.py`
Entry point and orchestrator for the daily ingest. Configures logging from `logging_reference.LOGGING`, opens one DB connection, and runs the fetch -> transform -> append sequence inside it.

Hardcoded: `TABLE = 'shopper_log'`, `path_str = '/home/lcalleja/stats.csv'`.

Control flow (`main()`):
```
main()
├── logging.config.dictConfig(LOGGING)
└── with db_connector.connect() as conn
    ├── latest = db_connector.latest_date(conn, TABLE)
    ├── fetch.download2(Path(path_str), latest)
    ├── rows = transform.transform_rows(path_str, after=latest)
    └── if rows: db_connector.append(conn, TABLE, rows)
```

### `db_connector.py`
All MySQL access. This queries the database to obtain the latest date in the table and later writes rows to the table (after its vetted by transform.py).
Functions: 
  - `get_config(yaml_file: str)` loads `host`, `user`, `password`, `database`, `port` from a YAML secrets file into a dict. `connect(creds_dict: dict|None = None)` is a context manager yielding a `mysql.connector` connection (falls back to `get_config("/home/lcalleja/shopper_composite/secrets.yaml")`) and closes it on exit. 
  - `latest_date(conn, table: str)` returns `MAX(date)` or `None`. 
  - `append(conn, table: str, rows: list[tuple])` runs `executemany` INSERT, commits, and returns the row count; rolls back and re-raises on error.

### `fetch.py`
Downloads the check-in report from plum. 
Functions:
  - `download2(dest: Path, start_dt: str, timeout: int = 60)` runs `wget -O <dest> check-in-desk:8888/stats?format=csv&start=<start_dt>` via `subprocess.run(check=True)`; a non-zero exit raises `CalledProcessError` after logging. Hardcoded: the `check-in-desk:8888` host and `format=csv`.

### `transform.py`
Converts the downloaded CSV into insert-ready tuples. 
Functions: 
  - `transform_rows(csv_path: str | Path, after: date | None = None)` reads the file with `csv.DictReader`, parses `date` as ISO, skips rows where `date <= after`, and coerces the count columns through `_to_smallint` (blank -> `None`). Returns `[(date, ghfc, trial, psfc, cbfc, visitor), ...]`. Hardcoded: `INT_COLS = ("ghfc", "trial", "psfc", "cbfc", "visitor")`.