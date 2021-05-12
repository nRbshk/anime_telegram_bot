import logging

from os.path import exists
from .unseen_func import get_download_format, get_episode_format, get_base_link
from requests import get
from bs4 import BeautifulSoup
from re import findall

logger = logging.getLogger(__name__)

def get_token(fn: str = "token.token"):
    logger.info("Getting token")
    return open(fn, 'r').readline()

def get_date():
    logger.info("START Getting date")
    import datetime
    """
    return date in format day.month.year
    """
    time = str(datetime.datetime.now())
    time = time[0:10]
    year, day, month = time.split("-")
    return f'{day}.{month}.{year}'