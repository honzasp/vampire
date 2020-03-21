import asyncio
import httpx
import logging

from .data import BLOOD_TYPES, BLOOD_STATUSES, SiteStatus

from . import benesov
from . import hodonin
from . import karvina
from . import klatovy
from . import liberec
from . import olomouc
from . import ostrava
from . import plzen
from . import praha_uhkt
from . import praha_vfn
from . import praha_fnkv
from . import trutnov
from . import trinec
from . import zlin

SCRAPERS = [
    benesov,
    hodonin,
    karvina,
    klatovy,
    liberec,
    olomouc,
    ostrava,
    plzen,
    praha_uhkt,
    praha_vfn,
    praha_fnkv,
    trutnov,
    trinec,
    zlin,
]

async def async_scrape_sites(*, logger=None):
    if logger is None:
        logger = logging.getLogger("vampire")

    site_statuses = []

    async def scrape(client, scraper):
        try:
            blood_statuses = await scraper.scrape(client)
        except Exception:
            logger.exception(f"Exception while scraping {scraper.__name__!r}")
            return

        for blood_type, blood_status in blood_statuses.items():
            assert blood_type in BLOOD_TYPES, (blood_type,)
            assert blood_status in BLOOD_STATUSES, (blood_status,)

        site_statuses.append(SiteStatus(uuid=scraper.UUID, short_id=scraper.SHORT_ID,
            url=scraper.URL, name=scraper.NAME, blood_statuses=blood_statuses))

    headers = {"User-Agent": "Vampire"}
    async with httpx.AsyncClient(headers=headers, verify=False) as client:
        await asyncio.gather(*[scrape(client, s) for s in SCRAPERS])
    return sorted(site_statuses, key = lambda s: s.short_id)

def scrape_sites(**kwargs):
    return asyncio.run(async_scrape_sites(**kwargs))
