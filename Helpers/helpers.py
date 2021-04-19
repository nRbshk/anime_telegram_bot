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

    
# def get_link(url):
#     logger.info(f"Getting link with url `{url}`")
#     from bs4 import BeautifulSoup

#     from selenium import webdriver
#     """
#     :param url: url for find link
#     :return: :class:`str` link
#     """
#     chrome_options, path = setup_chrome()

#     driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

#     driver.get(url)
#     driver.find_element_by_xpath('//*[@id="ep3"]').click()
    
#     driver.implicitly_wait(2)
#     find_player = driver.find_element_by_xpath('//*[@id="player0"]').get_attribute("innerHTML").splitlines()[0]
#     soup = BeautifulSoup(find_player, 'lxml')
#     iframe = soup.find("iframe")

#     logger.info(f'END get link with data {iframe["src"][2:]}')
#     return iframe['src'][2:]


# def get_link(url):
    # logger.info(f"Getting link with url `{url}`")
    # from bs4 import BeautifulSoup

    # from selenium import webdriver
    # """
    # :param url: url for find link
    # :return: :class:`str` link
    # """
    # chrome_options, path = setup_chrome()
    
    # driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    # driver.get(url)
    # driver.find_element_by_xpath('//*[@id="ep3"]').click()
    # driver.implicitly_wait(2)
    # find_player = driver.find_element_by_xpath('//*[@id="player0"]').get_attribute("innerHTML").splitlines()[0]
    # soup = BeautifulSoup(find_player, 'lxml')
    # iframe = soup.find("iframe")

    # return iframe['src'][2:]

#     uniq_id = iframe['src'][2:].split('/')[-2]
#     sleep(2)
#     print(url)
#     print(uniq_id)

#     download_format = get_download_format(uniq_id)

#     driver.get(download_format)
#     sleep(2)
#     button = driver.find_element_by_xpath('//*[@id="uc-download-link"]').click()
#     a = driver.find_element_by_xpath('//*[@id="uc-text"]/p[2]/span').get_attribute("innerHTML").splitlines()[0]
#     soup = BeautifulSoup(a, 'lxml')
#     fn_download = soup.find("a").text

#     driver.implicitly_wait(30)
#     while not wait_until_download(path, fn_download):
#         driver.implicitly_wait(30)
    
#     driver.close()
#     driver.quit()



# def wait_until_download(path: str, fn: str) -> bool:
#     logger.info(f"Waiting for dowload file {fn}")
#     fool_name = path + "\\" + fn
    
#     return exists(fool_name)
