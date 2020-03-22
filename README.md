# Vampire

> Vampire looks for blood in the Czech transfusion centers!

This program scrapes the webs of Czech transfusion centers and hospitals
and extracts information about the amount of available blood. Intended to
provide data for the map at https://darujukrev.cz.

**NOTE**: This program will break if the scraped web pages are modified in an
unexpected way. Therefore, it must be continually maintained.

## Scrape to CSV

To scrape the blood status into CSV, run:

    python3 -m vampire

It will print the results in CSV (with a header) to stdout.

## Scrape to a Google Sheet

To scrape the blood status into a Google Sheet, you will need to prepare two
config files:

- `secret/service_account.json`: private key and other information about a
    "service account" for a Google application with access to the Sheets API.
    This can be generated from the Google Developer Console.
- `secret/spreadsheet.json`: a JSON file which identifies the target
    spreadsheet. It must define `spreadsheet_id` (identifier of the spreadsheet)
    and `sheet_id` (name of the sheet).

The spreadsheet must have a header which corresponds to the CSV header. The
columns can be specified in any order.

The scraper can then be run as follows:

    python3 -m vampire.update_sheet

It will update any existing rows in the sheet and add any new rows. Rows that
were not scraped correctly are not modified.

## Use as a library

    import vampire
    site_statuses = vampire.scrape_sites()

The output of `scrape_sites()` is a list of `vampire.SiteStatus` (see
`vampire/data.py` for a definition).

When an error occurs during scraping (for example, if the layout of the scraped
web page has changed), the exception is logged, but other sites will still be
returned. You can pass a custom logger to `scrape_sites()` using a keyword
argument `logger`.

The library uses `asyncio` and `httpx` to scrape all sites in parallel. When
used from async code, you may want to use `vampire.async_scrape_sites()`, which
is async version of `vampire.scrape_sites()`.

---

This software is released into public domain (see `UNLICENSE` for the legalese).
