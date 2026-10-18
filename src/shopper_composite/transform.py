#%%
from pathlib import Path
import csv
import logging
'''
handle all data transformations here, this is then passed back to db_connector for the writing process

column names for table shooper_log: date,ghfc,trial,psfc,cbfc,visitor
'''


def transform_rows(csv_path: str):
#this will get ingested by db_connectot append(), via sql connection cursor executemany(sql, rows)
    with open(csv_path, "r") as f:
        data = csv.DictReader(f)
        for row in data:
            print(row)

transform_rows(Path('/home/lcalleja/stats_mini.csv'))
# %%
