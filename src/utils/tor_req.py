from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


def tor_req(req: requests.get):
    headers = {'User-Agent': UserAgent().random}
    with Controller.from_port(port=9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)
        return req(headers=headers, proxies=proxies)
