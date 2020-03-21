import re
from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "f215964b5546bd32f91ffdf919136be7"
SHORT_ID = "praha_fnkv"
URL = "https://www.fnkv.cz/pro-darce.php"
NAME = "Fakultní nemocnice Královské Vinohrady"

BLOOD_TYPE_ORDER = [
    ("A", "a+"),
    ("AB", "ab+"),
    ("B", "b+"),
    ("0", "0+"),
    ("A", "a-"),
    ("AB", "ab-"),
    ("B", "b-"),
    ("0", "0-"),
]

async def scrape(client):
    doc = await get_html(client, URL)
    label_divs = doc.cssselect(".krevni-zasoba-odsz0>div")
    level_divs = doc.cssselect(".krevni-zasoba-odsz>div")
    assert len(label_divs) == len(BLOOD_TYPE_ORDER)
    assert len(level_divs) == len(BLOOD_TYPE_ORDER)

    blood_statuses = {}
    for i, (expected_label, blood_type) in enumerate(BLOOD_TYPE_ORDER):
        label_text = inner_text(label_divs[i])
        assert label_text == expected_label, (label_text, expected_label)

        level_text = level_divs[i].get("title")
        level = int(re.search(r'(\d+)%', level_text)[1])
        if level >= 90:
            blood_status = "full"
        elif level >= 25:
            blood_status = "normal"
        else:
            blood_status = "urgent"
        blood_statuses[blood_type] = blood_status
    return blood_statuses
