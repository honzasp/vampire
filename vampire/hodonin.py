from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "8fb88027ffa3b336f70949db51696ad8"
SHORT_ID = "hodonin"
URL = "https://www.nemho.cz/informace-pro-darce-krve"
NAME = "Nemocnice TGM Hodonín"

async def scrape(client):
    doc = await get_html(client, URL)

    blood_statuses = {}
    rows = doc.cssselect("div.gridInner div.row.custom-width")
    for row in rows:
        icon_src = row.cssselect("figure img")[0].get("src")
        if "kapka3" in icon_src:
            blood_status = "urgent"
        elif "kapka2" in icon_src:
            blood_status = "normal"
        elif "kapka1" in icon_src:
            blood_status = "full"
        else:
            assert False, (icon_src,)

        type_texts = inner_text(row.cssselect("article")[0]).split()
        for type_text in type_texts:
            blood_type = BLOOD_TEXT_TO_TYPE[type_text]
            blood_statuses[blood_type] = blood_status

    return blood_statuses
