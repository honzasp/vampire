import re
from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "166ca624cc61984ab44e0397b9586c9b"
SHORT_ID = "liberec"
URL = "https://www.nemlib.cz/darovani-krve/"
NAME = "Krajská nemocnice Liberec"

BLOOD_LEVEL_TO_STATUS = ["urgent", "urgent", "normal", "normal", "full"]

async def scrape(client):
    doc = await get_html(client, URL)
    blood_statuses = {}
    for div in doc.cssselect("#blood-supplies .type"):
        type_text = inner_text(div.cssselect("div.lablel")[0]).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]
        level = int(re.search(r'supply-(\d)', div.get("class"))[1])
        blood_status = BLOOD_LEVEL_TO_STATUS[level]
        blood_statuses[blood_type] = blood_status
    return blood_statuses

