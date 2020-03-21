import csv
import sys

from . import scrape_sites
from .data import BLOOD_TYPES

if __name__ == "__main__":
    writer = csv.writer(sys.stdout)
    writer.writerow(["uuid","short_id","url","name"] + BLOOD_TYPES)
    for s in scrape_sites():
        writer.writerow([s.uuid, s.short_id, s.url, s.name] + \
            [s.blood_statuses.get(t,"") for t in BLOOD_TYPES])
