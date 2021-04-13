import logging

from unseen_func import get_download_format, get_episode_format, get_base_link
from requests import get
from bs4 import BeautifulSoup
from re import findall


logger = logging.getLogger(__name__)



def check_for_notification_nb(names_to_check: list, idt: list, notified_eps: list) -> dict:
    """
    :param names_to_check: list to check
    :param idt: idt
    :param notified_ep: last notified ep
    :return: :class:`dict` with key name and value url, idt
    """

    url = get_base_link("nb")

    logger.info(f"Checking page {url}")
    OK_CODE = 200

    
    resp = get(url)

    if resp.status_code != OK_CODE:
        logger.error(f"Cant get {url}. Status is {resp.status_code}")
        return 1
    
    soup = BeautifulSoup(resp.text, 'lxml')

    find_title_relative = soup.find_all("div", {"class" : "title relative"})
    find_cont_newscont = soup.find_all("div", {"class" : "cont newscont"})

    title_url_names = find_entries(find_title_relative, find_cont_newscont, names_to_check, idt, notified_eps, soup)
    logger.info("END Checking page")

    return title_url_names

def find_entries(find_title_relative: list, find_cont_newscont: list, names: list, idt: list, notified_eps: list, soup: BeautifulSoup) -> dict:
    logger.info("START find_entries")
    title_url_names = {}

    for index in range(len(find_title_relative)):


        if findall("(манга)", find_title_relative[index].text.lower()) \
            or findall(".+ожидается", find_cont_newscont[index].text.lower()):
            continue

        title_name = find_title_relative[index].text

        current_ep = int(find_title_relative[index].text.split(' ')[-2])

        for jndex in range(len(names)):

            if findall(f'.*{names[jndex].lower()}.*', title_name.lower()) and current_ep > notified_eps[jndex]:
                a = soup.find('a', href=True, text=title_name)

                title_url_names[names[jndex]] = str(get_base_link("nb") + a['href'] + ',' + str(idt[jndex]) + ',' + str(current_ep))

                names.remove(names[jndex])
                idt.remove(idt[jndex])
                notified_eps.remove(notified_eps[jndex])


                break
    del find_title_relative
    del find_cont_newscont

    logger.info("END find_entries")
    return title_url_names    