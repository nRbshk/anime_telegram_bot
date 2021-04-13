import logging

from os.path import exists
from unseen_func import get_download_format, get_base_link, setup_chrome


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


def check_page(names_to_check: list, idt: list, notified_ep: list) -> dict:
    """
    :param names_to_check: list to check
    :param idt: idt
    :param notified_ep: last notified ep
    :return: :class:`dict` with key name and value url, idt
    """

    url = get_base_link()

    logger.info(f"Checking page {url}")
    OK_CODE = 200
    from requests import get
    from bs4 import BeautifulSoup
    from re import findall
    
    resp = get(url)

    if resp.status_code != OK_CODE:
        logger.error(f"Cant get {url}. Status is {resp.status_code}")
        return 1
    
    soup = BeautifulSoup(resp.text, 'lxml')

    find_title_relative = soup.find_all("div", {"class" : "title relative"})
    find_cont_newscont = soup.find_all("div", {"class" : "cont newscont"})

    title_url_names = {}

    for index in range(len(find_title_relative)):


        if findall("(манга)", find_title_relative[index].text.lower()) \
            or findall(".+ожидается", find_cont_newscont[index].text.lower()):
            continue

        title_name = find_title_relative[index].text

        current_ep = int(find_title_relative[index].text.split(' ')[-2])

        for jndex in range(len(names_to_check)):

            if findall(f'.*{names_to_check[jndex].lower()}.*', title_name.lower()) and current_ep > notified_ep[jndex]:
                a = soup.find('a', href=True, text=title_name)

                title_url_names[names_to_check[jndex]] = str(get_base_link() + a['href'] + ',' + str(idt[jndex]) + ',' + str(current_ep))

                names_to_check.remove(names_to_check[jndex])
                idt.remove(idt[jndex])
                notified_ep.remove(notified_ep[jndex])


                break

    del find_title_relative
    del find_cont_newscont
    logger.info("END Checking page")
    return title_url_names
    
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
