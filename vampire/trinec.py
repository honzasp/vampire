import re
from .helpers import get_html, inner_text, blood_percent_to_status

UUID = "9d614319a716dc55fb6033204c08928f"
SHORT_ID = "trinec"
URL = "https://www.nemtr.cz/index.php/cs/pacienti-a-navstevnici/" \
    "pro-darce-krve/125-nemocnice-trinec/pacienti-a-navstevnici/" \
    "925-stav-krevnich-zasob"
NAME = "Nemocnice Třinec"

JS_VAR_TO_TYPE = {
    "dataApozA": "a+",
    "dataABpozA": "ab+",
    "dataBpozA": "b+",
    "dataOpozA": "0+",
    "dataAnegA": "a-",
    "dataABnegA": "ab-",
    "dataBnegA": "b-",
    "dataOnegA": "0-",
}

JS_VAR_RE = re.compile(r'var ([a-zA-Z]+) = "([0-9]+)"')

async def scrape(client):
    doc = await get_html(client, URL)

    blood_statuses = {}
    for script in doc.cssselect("script"):
        script_text = inner_text(script)
        for js_var_match in JS_VAR_RE.findall(script_text):
            js_var = js_var_match[0]
            blood_type = JS_VAR_TO_TYPE.get(js_var)
            if blood_type is None: continue

            level = int(js_var_match[1])
            blood_statuses[blood_type] = blood_percent_to_status(level)
    return blood_statuses

