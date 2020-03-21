import re
from .helpers import get_html, inner_text

UUID = "347a7cd913b1a57d45a37f4acc3a9582"
SHORT_ID = "ostrava"
URL = "https://www.fno.cz/krevni-centrum"
NAME = "Fakultní nemocnice Ostrava"

BLOOD_TEXT_TO_TYPE = {
    ("Rh+", "A"): "a+",
    ("Rh+", "AB"): "ab+",
    ("Rh+", "B"): "b+",
    ("Rh+", "0"): "0+",
    ("Rh-", "A"): "a-",
    ("Rh-", "AB"): "ab-",
    ("Rh-", "B"): "b-",
    ("Rh-", "0"): "0-",
}

CHART_RE = re.compile(r'chartObj = .*"renderAt": "([a-zA-Z0-9-]*)"' \
    r'.*<set.*value=\'(\d+)\'.*<set')

async def scrape(client):
    doc = await get_html(client, URL)

    chart_values = {}
    for script in doc.cssselect("script"):
        for line in inner_text(script).split("\n"):
            m = CHART_RE.search(line)
            if m is None: continue
            chart_div_id = m[1]
            chart_value = int(m[2])
            chart_values[chart_div_id] = chart_value

    blood_statuses = {}
    table = doc.cssselect("#page>table.emptyTable")[0]
    table_tds = [tr.cssselect("td") for tr in table.cssselect("tr")]
    assert len(table_tds) == 3, (len(table_tds), table_tds)
    for i in range(2):
        assert len(table_tds[i+1]) == 5
        rh_text = inner_text(table_tds[i+1][0]).strip()
        for j in range(4):
            type_text = inner_text(table_tds[0][j+1]).strip()
            blood_type = BLOOD_TEXT_TO_TYPE[(rh_text, type_text)]

            chart_div_id = table_tds[i+1][j+1].cssselect("div>div")[0].get("id")
            level = chart_values[chart_div_id]
            # TODO: determine the thresholds
            if level >= 95:
                blood_status = "full"
            elif level >= 25:
                blood_status = "normal"
            else:
                blood_status = "urgent"
            blood_statuses[blood_type] = blood_status
    return blood_statuses
