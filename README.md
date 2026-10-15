# ExtractIQ — Web Extraction & Data Quality Console

## What is this project used for?

ExtractIQ is used to turn permitted public catalogue pages into clean, traceable datasets for analysis and reporting. It helps users collect product details, validate missing fields, remove duplicate source URLs and export records in CSV or JSON. Typical uses include catalogue research, data preparation and repeatable extraction jobs.

## The problem

Raw web data needs validation, deduplication and traceable source links before it can be used in analysis or operational workflows.

## The solution

ExtractIQ collects paginated catalogue records through an approved-source runner. It normalizes prices, validates required fields and removes duplicate URLs, then stores job history and clean records for review.

- Source restrictions and robots checks
- Request pacing, timeouts and bounded retries
- Pagination and validation metrics
- Authenticated, owner-scoped job access
- Record search, rating filters and original source links
- CSV and JSON exports

New runs execute through the command-line runner. The console does not claim a browser-based scraping trigger or an enabled scheduler.

## Screenshots

![Extraction history](screenshots/ExtractIQ_01_Runs.png)
![Record inspector](screenshots/ExtractIQ_02_Records.png)
![Filtered records](screenshots/ExtractIQ_03_Search.png)

## Explore the implementation

[Extraction runner](app/core/scraper.py) · [Command](app/core/management/commands/crawl_catalogue.py) · [CSV output](output/catalogue.csv) · [JSON output](output/catalogue.json) · [Run locally](SETUP.md)

## Source and validation

The actual HTTP extraction captured 40 unique records from two pages of [Books to Scrape](https://books.toscrape.com/), a public scraping-practice catalogue. Prices and ratings are illustrative source data, not commercial market pricing. There were zero rejected records in this run.

This is an independent project. The repository provides the full server application. A separate browser preview is available through GitHub Pages; it does not run the authenticated server backend.


## Browser preview

The `docs/index.html` preview runs in the browser. Search, rating filters, sorting and CSV/JSON downloads operate on the saved catalogue capture; it does not scrape new web pages.
