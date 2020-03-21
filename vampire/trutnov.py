import re
from .helpers import get_html, inner_text

UUID = "032c6b3d8ea12887e600284bb1f0fd36"
SHORT_ID = "trutnov"
URL = "http://www.nemtru.cz/oddeleni-ambulance/darcovsky-usek"
NAME = "Nemocnice Trutnov"

BLOOD_TEXT_TO_TYPE = {
    ("RH+", "A"): "a+",
    ("RH+", "AB"): "ab+",
    ("RH+", "B"): "b+",
    ("RH+", "0"): "0+",
    ("RH-", "A"): "a-",
    ("RH-", "AB"): "ab-",
    ("RH-", "B"): "b-",
    ("RH-", "0"): "0-",
}

BLOOD_LEVEL_RE = re.compile(r'blood_(\d)\.png')
BLOOD_LEVEL_TO_STATUS = ["urgent", "normal", "normal", "full"]

async def scrape(client):
    doc = await get_html(client, URL)

    blood_statuses = {}
    for class_name in ["rh_faktor_plus", "rh_faktor_minus"]:
        blood_div = doc.cssselect(f"div.blood_state div.{class_name}")[0]
        rh_text = inner_text(blood_div.cssselect("h3")[0]).strip()
        for type_div in blood_div.cssselect("div.blood_type"):
            type_text = inner_text(type_div).strip()
            blood_type = BLOOD_TEXT_TO_TYPE[(rh_text, type_text)]

            img_src = type_div.cssselect("img")[0].get("src")
            level = int(BLOOD_LEVEL_RE.search(img_src)[1])
            blood_statuses[blood_type] = BLOOD_LEVEL_TO_STATUS[level]
    return blood_statuses
