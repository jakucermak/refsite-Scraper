from src.environment import EKIS_BASE_URL
from bs4 import BeautifulSoup
from requests import Response


def scrape(request, page='', post_id="") -> Response:
    url = "{}/cz{}/ekis/i-ekis/{}".format(EKIS_BASE_URL, page, post_id)
    response = request(url)
    return response


def parse_response(html):
    bs = BeautifulSoup(html, 'lxml')
    return bs


def get_ids(parse_html):
    parsed_html = parse_html

    items = parsed_html.find_all("article", class_="item")
    post_ids = []

    for item in items:
        parsed_id: str = item['onclick']
        parsed_id = parsed_id.removeprefix("document.location='/cz/ekis/i-ekis/").removesuffix('\'')
        post_ids.append(parsed_id)
    return post_ids


def get_next_page(parse_html):

    pager = parse_html.find("div", class_="pager")
    for a in pager.find_all("a"):
        if a.string == '»':
            next_page = a['href'].removeprefix("/cz").removesuffix('/ekis/i-ekis')
            return next_page
