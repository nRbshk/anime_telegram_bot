import logging
from requests import get
from asyncio import sleep

logger = logging.getLogger(__name__)



def get_id_sv(name: str):
    logger.info("START get_id_sv")

    url = "https://service.sovetromantica.com/v1/animesearch"

    headers = {"accept" : "application/json"}

    params = {"anime_name" : name}

    response = get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None
    
    response = response.json()

    logger.info("END get_id_sv")
    if response[0]:
        return response[0]['anime_id']
    return None

def get_episodes_sv(anime_id: str, dub_or_sub: str = "sub"):
    ds_dict = {"dub": 1, "sub": 0}
    logger.info("START get_episodes_sv")

    url = f"https://service.sovetromantica.com/v1/anime/{anime_id}/episodes"
    headers = {"accept" : "application/json"}

    response = get(url, headers=headers)

    if response.status_code != 200:
        return None
    
    response = response.json()

    episodes = [r for r in response if r['episode_type'] == ds_dict[dub_or_sub]]
    
    logger.info("END get_episodes_sv")
    if len(episodes) > 0:
        return episodes
    return None

    

def get_link_sv(name, idt, notified_ep, dub_or_sub):
    logger.info("START get_link_sv")
    
    anime_id = get_id_sv(name)
    if anime_id is None:
        return None
        
    last_episode = get_episodes_sv(anime_id, dub_or_sub)
    if last_episode is None:
        return None
    
    last_episode = last_episode[-1]
    if last_episode['episode_count'] > int(notified_ep):
        pre_value = last_episode['embed'] + "," + str(idt) + "," +  str(last_episode['episode_count'])
        return pre_value

    logger.info("END get_link_sv")  
    return None

async def check_for_notification_sv(names: list, idt: list, notified_eps: list, dub_or_subs: list) -> dict:
    logger.info("START check_for_notification_sv")
    if len(names) != len(idt) or len(names) != len(notified_eps) or len(names) != len(dub_or_subs):
        logger.error("Length of names and idt and notified_ep must be the same")
        return 1
    title_url_names = {}
    for index in range(len(names)):
        await sleep(1)
        url = get_link_sv(names[index], idt[index], notified_eps[index], dub_or_subs[index])
        if url is None:
            continue
        title_url_names[names[index]] = url
    
    logger.info("END check_for_notification_sv")
    return title_url_names
