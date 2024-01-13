import os.path

import pytest
import requests

import src.utils.scraper as scraper
from fixtures import html_page, answer_text, question_text
from src.utils.scraper import QASectionType


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


def test_get_tags_from_detail():
    with open("test_html/detail_page.html") as f:
        actual = scraper.get_tags(scraper.parse_response(f)).sort()

    expected = ["Dotace a financování projektů","En. audity, en. průkazy a štítky budov",
                "Tepelná čerpadla, geotermální energie", "Vytápění", "Zateplování budov"].sort()

    assert actual == expected


def test_scrape_answer(answer_text):
    with open("test_html/detail_page.html") as f:
        actual = scraper.retrieve_qa_content(scraper.parse_response(f), QASectionType.ANSWER)
    expected = answer_text
    assert actual == expected


def test_scrape_question(question_text):
    with open("test_html/detail_page.html") as f:
        actual = scraper.retrieve_qa_content(scraper.parse_response(f), QASectionType.QUESTION)
    expected = question_text
    assert actual == expected
