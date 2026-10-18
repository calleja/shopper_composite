from datetime import date, datetime
import mysql.connector
import yaml
import os
from contextlib import contextmanager
import logging

from logging_reference import LOGGING


'''
host: "localhost"
user: "lcalleja2"
password: 30598
database: "membership_ard"
'''

logger = logging.getLogger(__name__)

def get_config(yaml_file: str):
    if yaml_file is None:
        yaml_file = "/Users/casita/code/shopper_composite/secrets/secrets.yaml"
    
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"File {yaml_file} not found")
    
    #load the entire file and treat as dict
    with open(yaml_file, 'r') as file:
        file = yaml.safe_load(file)
        host = file['host']
        user = file['user']
        password = file['password']
        database = file['database']
        port = file['port']

        return {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': int(port)
        }

#cli_dict = values that might be passed to this function from cli.py; If None, then call the get_config function
#cli_dict will contain values for the connection
@contextmanager
def connect(creds_dict: dict|None = None):
    if creds_dict is None:
        creds_dict = get_config("/home/lcalleja/shopper_composite/secrets.yaml")
    try:
        conn = mysql.connector.connect(host=creds_dict['host'], port=creds_dict['port'], user=creds_dict['user'], password=creds_dict['password'], database=creds_dict['database'])
    except mysql.connector.Error:
        logger.exception("connection failure in connect() funct")
        raise
    try:
        yield conn
    finally:
        conn.close()

#accepts a connection argument
def latest_date(conn, table: str) -> date | None:
    #the single element will return a datetime.date object of format YYYY-MM-DD
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT MAX(`date`) FROM `{table}`")
            return cur.fetchone()[0]
    except mysql.connector.Error:
        logger.exception("latest_date retrieval failed for %s", table)
        raise

def append(conn, table: str, rows: list[tuple]) -> int:
    sql = (f"INSERT INTO `{table}` (`date`,`ghfc`,`trial`,`psfc`,`cbfc`,`visitor`) "
           "VALUES (%s,%s,%s,%s,%s,%s)")
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, rows)
        conn.commit()
        return len(rows)
    except mysql.connector.Error:
        logger.exception("append failed: %d rows for %s", len(rows), table)
        conn.rollback()
        raise


