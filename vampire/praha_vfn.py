import re
from .helpers import get_html, inner_text, BLOOD_TEXT_TO_TYPE

UUID = "d052dc10eb314a96399c574fce480165"
SHORT_ID = "praha_vfn"
URL = "https://www.vfn.cz/pacienti/kliniky-ustavy/" \
    "fakultni-transfuzni-oddeleni/aktualni-potreba-krve/"
NAME = "Všeobecná fakultní nemocnice v Praze"

COLOR_RE = re.compile(r'background-color:\s*#([0-9a-f]{6})')
BLOOD_COLOR_TO_STATUS = {
    "32ff33": "urgent",
    "21a900": "normal",
    "fa0106": "full",
}

async def scrape(client):
    doc = await get_html(client, URL)
    blood_statuses = {}
    table = doc.cssselect("#idobsahu>table")[0]
    for td in table.cssselect("td"):
        type_text = inner_text(td).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[type_text]
        color = COLOR_RE.search(td.get("style"))[1]
        blood_status = BLOOD_COLOR_TO_STATUS[color]
        blood_statuses[blood_type] = blood_status
    return blood_statuses
