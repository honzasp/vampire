from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "82a69e8086c5a0e6a3497699b5382bc5"
SHORT_ID = "karvina"
URL = "http://www.nspka.cz/cs/pacient/daruj-krev/krevni-monitor.html"
NAME = "Nemocnice s poliklinikou Karviná-Ráj"

BLOOD_TEXT_TO_STATUS = {
    "STOP STAV": "full",
    "ODEBÍRÁME": "normal",
    "POMOC": "urgent",
}

async def scrape(client):
    doc = await get_html(client, URL)

    blood_statuses = {}
    for div in doc.cssselect("div.shiplab>div.monitor-circle"):
        type_text = inner_text(div.cssselect("div.typ-text")[0]).strip()
        status_text = inner_text(div.cssselect("div.hodnota-text")[0]).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]
        blood_status = BLOOD_TEXT_TO_STATUS[status_text]
        blood_statuses[blood_type] = blood_status

    return blood_statuses
