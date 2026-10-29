# Python Web Scraper

A reliable, configurable scraper for the public Books to Scrape catalog. It follows pagination, extracts structured book metadata, and writes a clean UTF-8 CSV for analysis or automation workflows.

## Features

- Scrapes one page or the complete catalog
- Follows the site pagination link
- Captures title, price, availability, and product URL
- Uses a reusable requests Session with a custom User-Agent
- Applies HTTP status checks and configurable timeouts
- Exposes a command-line interface with clear error messages
- Writes UTF-8 CSV output that opens correctly in spreadsheet applications

## Setup

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Usage

Scrape the full catalog into the default books.csv file:

```powershell
python scraper.py
```

Scrape only the first page and choose a different output path:

```powershell
python scraper.py --max-pages 1 --output data\books.csv
```

Available options:

| Option | Default | Description |
| --- | --- | --- |
| --url | https://books.toscrape.com/ | Starting page |
| --output | books.csv | CSV output path |
| --max-pages | 0 | Maximum pages; 0 scrapes all pages |
| --timeout | 15 | HTTP timeout in seconds |

## Output

The generated CSV contains title, price, availability, and url columns. The target site is intentionally designed for scraping practice. For real sites, respect terms of service, robots.txt, rate limits, and applicable law.

## Technologies

- Python
- Requests
- BeautifulSoup 4
- CSV
