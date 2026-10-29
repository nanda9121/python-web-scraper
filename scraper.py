"""Scrape book data from books.toscrape.com into a CSV file."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Final
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DEFAULT_URL: Final = "https://books.toscrape.com/"
DEFAULT_OUTPUT: Final = "books.csv"
DEFAULT_TIMEOUT: Final = 15


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Starting page to scrape")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV output path")
    parser.add_argument("--max-pages", type=int, default=0, help="Maximum pages to scrape; 0 means all pages")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="HTTP timeout in seconds")
    return parser.parse_args()


def scrape_books(url: str, timeout: int, max_pages: int = 0) -> list[dict[str, str]]:
    if max_pages < 0:
        raise ValueError("max-pages must be zero or a positive integer")
    if timeout <= 0:
        raise ValueError("timeout must be a positive integer")

    books: list[dict[str, str]] = []
    next_url: str | None = url
    pages_scraped = 0

    with requests.Session() as session:
        session.headers.update({"User-Agent": "python-web-scraper/1.0"})
        while next_url and (max_pages == 0 or pages_scraped < max_pages):
            response = session.get(next_url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for book in soup.select("article.product_pod"):
                title_link = book.select_one("h3 a")
                price = book.select_one("p.price_color")
                availability = book.select_one("p.instock.availability")
                if not (title_link and price and availability):
                    continue
                books.append({
                    "title": title_link.get("title", title_link.get_text(strip=True)),
                    "price": price.get_text(strip=True).replace("Â£", "£"),
                    "availability": " ".join(availability.get_text(" ", strip=True).split()),
                    "url": urljoin(next_url, title_link.get("href", "")),
                })

            pages_scraped += 1
            next_link = soup.select_one("li.next a")
            next_url = urljoin(next_url, next_link["href"]) if next_link else None

    return books


def write_csv(books: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "availability", "url"])
        writer.writeheader()
        writer.writerows(books)


def main() -> int:
    args = parse_args()
    try:
        books = scrape_books(args.url, args.timeout, args.max_pages)
        write_csv(books, args.output)
    except (OSError, requests.RequestException, ValueError) as error:
        print(f"Scraping failed: {error}", file=sys.stderr)
        return 1
    print(f"Scraped {len(books)} books into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
