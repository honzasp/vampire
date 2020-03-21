import aiohttp
import asyncio
import lxml.html

async def get_html(sess, url):
    async with sess.request("GET", url) as resp:
        resp.raise_for_status()
        resp_bytes = await resp.content.read()
    return lxml.html.fromstring(resp_bytes)

def inner_text(elem):
    return ((elem.text or "")
        + ("\n" if elem.tag in ("br", "BR") else "")
        + "".join(map(inner_text, elem.iterchildren()))
        + (elem.tail or ""))

