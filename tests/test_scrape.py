import os.path

import pytest
import requests

import src.utils.scraper as scraper
from fixtures import html_page


def test_scrape():
    def get_request(url):
        return requests.get(url)

    response = scraper.scrape(get_request)
    assert response.status_code == 200


@pytest.mark.skip()
def test_parse(html_page):
    path = os.path.curdir
    with open("test_html/init_page.html", 'r') as f:
        scrp = scraper.parse_response(f).find_all(True)
        line_list = []
        for n in range(1, len(scrp)):

            str = "{}".format(scrp[n]).rstrip()
            line_list.append(str)
        expected = html_page
        assert line_list == expected


def test_get_ids_from_html(html_page):
    path = os.path.curdir
    with open("test_html/init_page.html", 'r') as f:
        actual = scraper.get_ids(scraper.parse_response(f))
        actual.sort()

    expected = ["180457", "180453", "180550"]
    expected.sort()

    assert actual == expected


def test_next_page():
    with open("test_html/init_page.html", "r") as f:
        parser = scraper.parse_response(f)
    next_page = scraper.get_next_page(parser)

    expected = "2"
    assert next_page == expected
