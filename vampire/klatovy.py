from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "ec66625e36d2e9d7e8fd6159b34941a0"
SHORT_ID = "klatovy"
URL = "https://klatovy.nemocnicepk.cz/krev/"
NAME = "Klatovská nemocnice"

async def scrape(client):
    doc = await get_html(client, URL)

    blood_statuses = {}
    for div in doc.cssselect("div.blood__list div.blood__item"):
        type_text = inner_text(div.cssselect("div.blood__name")[0]).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]

        ico_src = div.cssselect("div.blood__ico img")[0].get("src")
        if "prijdte" in ico_src:
            blood_status = "urgent"
        elif "odlozte" in ico_src:
            blood_status = "full"
        else:
            # TODO: what does the "normal" state look like?
            assert False, (ico_src,)
        blood_statuses[blood_type] = blood_status

    return blood_statuses

