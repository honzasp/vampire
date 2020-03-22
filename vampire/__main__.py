import csv
import sys

from . import scrape_sites
from .data import BLOOD_TYPES, SITE_STATUS_FIELDS, site_status_to_fields

if __name__ == "__main__":
    site_statuses = scrape_sites()
    writer = csv.DictWriter(sys.stdout, fieldnames=SITE_STATUS_FIELDS)
    writer.writeheader()
    for s in site_statuses:
        writer.writerow(site_status_to_fields(s))
