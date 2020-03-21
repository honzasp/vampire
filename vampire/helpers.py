import asyncio
import lxml.html

async def get_html(client, url):
    resp = await client.get(url)
    resp.raise_for_status()
    return lxml.html.fromstring(resp.text)

def inner_text(elem):
    return ((elem.text or "")
        + ("\n" if elem.tag in ("br", "BR") else "")
        + "".join(map(inner_text, elem.iterchildren()))
        + (elem.tail or ""))

BLOOD_TEXT_TO_TYPE = {
    "0+": "0+",
    "0-": "0-",
    "A-": "a-",
    "A+": "a+",
    "B-": "b-",
    "B+": "b+",
    "AB-": "ab-",
    "AB+": "ab+",
    "Krevní plazma": "plasma",
}

