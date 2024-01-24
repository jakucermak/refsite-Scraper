import logging

import requests
from fake_useragent import UserAgent
from requests import Response
from stem import Signal
from stem.control import Controller

from src.environment import RUNNING_ENVIRONMENT

logger = logging.getLogger(__name__)

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def tor_req(url):
    headers = {'User-Agent': UserAgent().random}
    with Controller.from_port(port=9051) as c:
        logger.info(f'Changing proxy for {url} with tor')
        c.authenticate()
        c.signal(Signal.NEWNYM)
        return requests.get(url, headers=headers, proxies=proxies)


def get(url) -> Response:
    match RUNNING_ENVIRONMENT:
        case 'DEBUG':
            return requests.get(url)
        case 'PRODUCTION':
            return tor_req(url)
        case _:
            logger.error(f'Could not set environment variable')
