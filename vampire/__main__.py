import aiohttp
import asyncio
import logging

from . import trutnov
from . import trinec
from . import zlin

SCRAPERS = [
    ("032c6b3d8ea12887e600284bb1f0fd36", trutnov.scrape_trutnov),
    ("9d614319a716dc55fb6033204c08928f", trinec.scrape_trinec),
    ("2b165b7a1f651b22402aecc253f3821f", zlin.scrape_zlin),
]

async def main(loop):
    headers = {"User-Agent": "Blood Status Bot"}
    timeout = aiohttp.ClientTimeout(total=30)

    statuses = {}
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as sess:
        for guid, scraper in SCRAPERS:
            status = await scraper(sess)
            statuses[guid] = status

    print(statuses)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_task = loop.create_task(main(loop))
    loop.run_until_complete(main_task)
