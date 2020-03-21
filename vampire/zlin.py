from .helpers import get_html, inner_text
from .data import SiteStatus

URL = "https://www.kntb.cz/informace-pro-darce-krve"
NAME = "Nemocnice Tomáše Bati ve Zlíně"

BLOOD_TEXT_TO_TYPE = {
    "0-": "0-",
    "0+": "0+",
    "A-": "a-",
    "A+": "a+",
    "AB-": "ab-",
    "AB+": "ab+",
    "B-": "b-",
    "B+": "b+",
}

BLOOD_LEVEL_TO_STATUS = ["urgent", "urgent", "normal", "normal", "full"]

async def scrape_zlin(sess):
    doc = await get_html(sess, URL)
    table = doc.cssselect("table.blood")[0]
    header_tds = table.cssselect("thead td")
    body_tds = [tr.cssselect("td") for tr in table.cssselect("tbody tr")]

    assert len(header_tds) == len(BLOOD_TEXT_TO_TYPE), (len(header_tds), header_tds)
    assert len(body_tds) == len(BLOOD_LEVEL_TO_STATUS)-1, (len(body_tds), body_tds)

    blood_statuses = {}
    for col in range(len(header_tds)):
        blood_type_text = inner_text(header_tds[col]).strip()
        blood_type = BLOOD_TEXT_TO_TYPE[blood_type_text]

        level = 0
        for row in range(len(body_tds)):
            td = body_tds[row][col]
            img_src = td.cssselect("img")[0].get("src")
            if "blood-empty" in img_src:
                level += 0
            elif "blood-red" in img_src:
                level += 1
            else:
                assert False, (col, row, img_src)
        blood_statuses[blood_type] = BLOOD_LEVEL_TO_STATUS[level]

    return SiteStatus(url=URL, name=NAME, blood_statuses=blood_statuses)
