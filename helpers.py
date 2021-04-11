import logging

logger = logging.getLogger(__name__)

def get_token(fn: str = "token.token"):
    logger.info("Getting token")
    return open(fn, 'r').readline()

def get_date():
    logger.info("Getting date")
    import datetime
    """
    return date in format day.month.year
    """
    time = str(datetime.datetime.now())
    time = time[0:10]
    year, day, month = time.split("-")
    return f'{day}.{month}.{year}'