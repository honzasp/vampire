from .helpers import get_html, inner_text

UUID = "33cea15c8d79d71977db2db86c6e9c5c"
SHORT_ID = "benesov"
URL = "https://www.hospital-bn.cz/oddeleni/transfuzni-a-hematologicke-oddeleni/" \
    "transfuzni-sluzba/aktualni-stav-krevnich-zasob/"
NAME = "Nemocnice Benešov"

async def scrape(client):
    # TODO: the graphs seem to be broken, the first 7 graphs show 0+ and the last one
    # shows A-!!!
    return {}


