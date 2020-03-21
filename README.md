# Vampire

> Vampire looks for blood in the Czech transfusion centers!

This program scrapes the webs of Czech transfusion centers and hospitals
and extracts information about the amount of available blood. Intended to
provide data for the map at https://darujukrev.cz.

This program can be run as a command line application:

    python3 -m vampire

It will print the results in CSV (with a header) to stdout. Or it can be
imported as a library:

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
