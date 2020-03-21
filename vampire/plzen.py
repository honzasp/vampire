import re
from .helpers import get_html, inner_text

UUID = "4d21d633b378885af5468746345fe510"
SHORT_ID = "plzen"
URL = "https://to.fnplzen.cz/"
NAME = "Fakultní nemocnice Plzeň"

BLOOD_ID_TO_TYPE = {
    "transfusni-inzerce-krev-0plus": "0+",
    "transfusni-inzerce-krev-aplus": "a+",
    "transfusni-inzerce-krev-bplus": "b+",
    "transfusni-inzerce-krev-abplus": "ab+",
    "transfusni-inzerce-krev-0minus": "0-",
    "transfusni-inzerce-krev-aminus": "a-",
    "transfusni-inzerce-krev-bminus": "b-",
    "transfusni-inzerce-krev-abminus": "ab-",
}

async def scrape(client):
    doc = await get_html(client, "https://www.fnplzen.cz/fn_plzen/krevdiv")
    blood_statuses = {}
    for div in doc.cssselect("#transfusni-inzerce-krev-zasoby>div"):
        if len(div) == 0: continue
        type_div, label_div = list(div)
        type_id = type_div.get("id")
        blood_type = BLOOD_ID_TO_TYPE[type_id]

        level_text = inner_text(label_div)
        level = int(re.search(r'(\d+)%', level_text)[1])
        if level >= 100:
            blood_status = "full"
        elif level >= 25:
            blood_status = "normal"
        else:
            blood_status = "urgent"
        blood_statuses[blood_type] = blood_status
    return blood_statuses
