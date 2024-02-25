import logging
from enum import Enum

from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import ConnectionError as RE

from src.environment import EKIS_BASE_URL

logger = logging.getLogger(__name__)


def scrape(r, page='', post_id="") -> Response:
    url = "{}/cz{}/ekis/i-ekis/{}".format(EKIS_BASE_URL, page, post_id)
    try:
        response = r(url)
        return response
    except RE as e:
        logger.error(repr(e))


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


def get_tags(parse_html) -> list[str]:
    response_about_group = parse_html.find("div", class_="box-5 sz-s clr-gray odpovida")
    tags_group = response_about_group.find("div", class_="mt-1")
    if tags_group is not None:
        tags = [tag.text for tag in tags_group.find_all("a")]
        return tags
    logger.info("No tags found")
    return []


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
    try:
        contents = parse_html.find("div", class_=class_).contents
    except AttributeError:
        logger.info("No contents of type: {} found".format(type.value))
        return

    if '\n' == contents[-1]:
        contents.pop()

    cleared_text = clean_text(contents)
    final_text = "\n".join(cleared_text)
    return final_text


def get_date_post(parse_html):
    content = parse_html.find("span", class_="bg-clr-orange clr-light sz-s color-block").contents
    split = content[0].split(" ")
    return split[1]


def clean_text(contents):
    cleared_text = []
    for line in contents:
        if "<br/>" != str(line):
            line = line.lstrip("\n\r").rstrip()
            line = ' '.join(item for item in line.split(" ") if item)
            cleared_text.append(line)
    return cleared_text
