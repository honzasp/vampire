import re
from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID ="7d48ffc5409b2d40ba0ead56facd0865"
SHORT_ID = "praha_uhkt"
URL = "https://www.uhkt.cz/darci/darovani-krve"
NAME = "Ústav hematologie a krevní transfuze"

async def scrape(client):
    doc = await get_html(client, URL)
    blood_statuses = {}
    for li in doc.cssselect("ul.barometer>li"):
        icon_class = li.cssselect("span.icon")[0].get("class")
        # WARNING: this is very strange; an icon displaying a FULL drop of blood means
        # that the status is LOW. This is the opposite of the usual convention!
        if "full-blood" in icon_class:
            blood_status = "urgent"
        elif "half-blood" in icon_class:
            blood_status = "normal"
        elif "empty-blood" in icon_class:
            blood_status = "full"

        type_text = inner_text(li).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]
        blood_statuses[blood_type] = blood_status
    return blood_statuses
