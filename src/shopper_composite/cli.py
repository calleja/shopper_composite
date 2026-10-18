import logging.config
import datetime as date

from shopper_composite import db_connector
from shopper_composite.logging_reference import LOGGING
from shopper_composite import fetch

'''
1. Grab the latest date from the db
2. compose the report command for plum
3. execute that command on the command line of radish
3. conduct any ETL necessary
4. insert records into db (radish)

'''
TABLE = 'shopper_log'

def main():
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(__name__)

    #connect() is a context manager object, and is only instantiated inside a "with" statement - this is done here; `latest_date()` has its own with block to handle a cursor object

    with db_connector.connect() as conn:
        latest = db_connector.latest_date(conn, TABLE)
        #assume that max_date will be captured as a datetime.date; convert to string
        try:
            latest_str = latest.strftime("%Y-%m-%d")
        except AttributeError:
            logger.exception("Latest date is not a datetime.date object")
            raise
        fetch.download2(Path('/home/lcalleja/stats.csv'), latest)
        #db_connector.append(conn, "membership_ard", rows)
        print(latest)

        

    url = fetch.build_url(BASE_URL, latest)
    fetch.download(url, dest)

if __name__ == "__main__":
    main()

def format_latest(latest: date) -> str:
    try: 
        if latest is None:
            raise ValueError("No latest date propogated to main")
    except ValueError:
        logger.exception("No latest date propogated to main")
        raise

    return latest.strftime("%Y-%m-%d")