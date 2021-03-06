import re
from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE, blood_percent_to_status

UUID = "62986dd03286fe38f7d6078fbf5f58f4"
SHORT_ID = "olomouc"
URL = "https://www.fnol.cz/kliniky-ustavy-oddeleni/transfuzni-oddeleni/pro-darce"
NAME = "Fakultní nemocnice Olomouc"

async def scrape(client):
    doc = await get_html(client, URL)
    blood_statuses = {}
    for div in doc.cssselect("section.clinic-detail div.pie-wrapper"):
        type_text = inner_text(div.cssselect("span.text")[0]).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]
        level = int(re.search(r'progress-(\d+)', div.get("class"))[1])
        blood_status = blood_percent_to_status(level)
        blood_statuses[blood_type] = blood_status
    return blood_statuses
