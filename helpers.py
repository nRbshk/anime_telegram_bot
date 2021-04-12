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


def check_page(names_to_check: list, idt: list) -> dict:
    """
    :param name_to_check: list to check
    :return: :class:`dict` with key name and value url, idt
    """

    url = 'https://naruto-base.su/'

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

    add_to_link = 'https://naruto-base.su'
    for index in range(len(find_title_relative)):

        if findall("(манга)", find_title_relative[index].text.lower()) or findall(".+ожидается", find_cont_newscont[index].text.lower()):
            continue

        title_name = find_title_relative[index].text

        for jndex in range(len(names_to_check)):

            if findall(f'.*{names_to_check[jndex].lower()}.*', title_name.lower()):
                a = soup.find_all('a', href=True, text=title_name)

                title_url_names[names_to_check[jndex]] = str(add_to_link + a[0]['href'] + ',' + str(idt[jndex]))
                names_to_check.remove(names_to_check[jndex])
                idt.remove(idt[jndex])

                break

    del find_title_relative
    del find_cont_newscont

    return title_url_names
    