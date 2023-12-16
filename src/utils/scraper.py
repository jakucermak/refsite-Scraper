import requests
from tor_req import tor_req
from src.environment import EKIS_BASE_URL

def scrape_ids():
    return tor_req('https://ident.me')

