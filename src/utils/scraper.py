from enum import Enum

from bs4 import BeautifulSoup
from requests import Response

from src.environment import EKIS_BASE_URL


def scrape(request, page='', post_id="") -> Response:
    url = "{}/cz{}/ekis/i-ekis/{}".format(EKIS_BASE_URL, page, post_id)
    response = request(url)

    return response


def parse_response(html):
    bs = BeautifulSoup(html, 'lxml')
    return bs


def get_ids(parse_html):
    items = parse_html.find_all("article", class_="item")
    post_ids = []

    for item in items:
        parsed_id: str = item['onclick']
        parsed_id = parsed_id.removeprefix("document.location='/cz/ekis/i-ekis/").removesuffix('\'')
        post_ids.append(parsed_id)
    return post_ids


def get_next_page(parse_html) -> str | None:
    pager = parse_html.find("div", class_="pager")
    for a in pager.find_all("a"):
        if a.string == '»':
            next_page = a['href'].removeprefix("/cz").removesuffix('/ekis/i-ekis')
            return next_page
    return


def get_tags(parse_html):
    response_about_group = parse_html.find("div", class_="box-5 sz-s clr-gray odpovida")
    tags_group = response_about_group.find("div", class_="mt-1")
    tags = [tag.text for tag in tags_group.find_all("a")]
    return tags


class QASectionType(Enum):
    QUESTION = "question"
    ANSWER = "answer"


def retrieve_qa_content(parse_html, type: QASectionType):
    match type.value:
        case "question":
            class_ = "fnt-bold mt-1 mb-3"
        case "answer":
            class_ = "mt-1 mb-1"
        case _:
            raise Exception("Did not set class attributes")

    contents = parse_html.find("div", class_=class_).contents

    if '\n' == contents[-1]:
        contents.pop()

    cleared_text = clean_text(contents)
    final_text = "\n".join(cleared_text)
    return final_text


def clean_text(contents):
    cleared_text = []
    for line in contents:
        if "<br/>" != str(line):
            line = line.lstrip("\n\r").rstrip()
            line = ' '.join(item for item in line.split(" ") if item)
            cleared_text.append(line)
    return cleared_text
