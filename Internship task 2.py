"""
Web Scraper — Internship Task 2
================================
Scrapes quotes from https://quotes.toscrape.com

Features:
  - BeautifulSoup-based HTML parsing
  - Pagination (auto-follows "Next" button)
  - Missing data handled gracefully (N/A / Unknown fallbacks)
  - Request errors handled (timeout, HTTP errors, connection errors)
  - Saves output to CSV and/or JSON
  - CLI interface with --pages, --output, --filename, --tag, --delay

Usage:
  python scraper.py                        # 3 pages, both CSV + JSON
  python scraper.py --pages 5              # scrape 5 pages
  python scraper.py --output json          # JSON only
  python scraper.py --tag love             # filter by tag
  python scraper.py --filename my_quotes   # custom output filename
  python scraper.py --help                 # show all options
"""





import requests


from bs4 import BeautifulSoup
import csv
import json
import argparse
import time
import sys


BASE_URL = "https://quotes.toscrape.com"


# ──────────────────────────────────────────────────────────────
#  1. SCRAPING
# ──────────────────────────────────────────────────────────────

def scrape_page(url, session):
    """
    Fetch and parse one page.
    Returns: (list_of_quote_dicts, next_page_url_or_None)
    """
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to {url}. Check your internet.")
        return [], None

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out: {url}")
        return [], None

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP {e.response.status_code} for {url}")
        return [], None

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []

    for div in soup.select("div.quote"):
        text_el   = div.select_one("span.text")
        author_el = div.select_one("small.author")
        tag_els   = div.select("a.tag")

        quotes.append({
            "text":   text_el.get_text(strip=True)                          if text_el   else "N/A",
            "author": author_el.get_text(strip=True)                        if author_el else "Unknown",
            "tags":   ", ".join(t.get_text(strip=True) for t in tag_els)   if tag_els   else "",
        })

    # Follow pagination
    next_btn = soup.select_one("li.next > a")
    next_url = BASE_URL + next_btn["href"] if next_btn else None

    return quotes, next_url


def run_scraper(pages, delay, tag):
    """Main loop — handles pagination up to `pages` pages."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (InternshipScraper/1.0)"})

    all_quotes = []
    url = BASE_URL + (f"/tag/{tag}/" if tag else "/")
    page_num = 1

    print("\n" + "=" * 52)
    print("  Web Scraper  |  quotes.toscrape.com")
    if tag:
        print(f"  Tag filter   : {tag}")
    print(f"  Max pages    : {pages}")
    print("=" * 52 + "\n")

    while url and page_num <= pages:
        print(f"[PAGE {page_num}] {url}")
        page_quotes, url = scrape_page(url, session)

        if not page_quotes:
            print("  → Nothing found. Stopping early.")
            break

        all_quotes.extend(page_quotes)
        print(f"  → {len(page_quotes)} quotes  |  Total: {len(all_quotes)}")

        # Polite delay between requests
        if url and page_num < pages:
            time.sleep(delay)

        page_num += 1

    print(f"\n✓ Done. {len(all_quotes)} quotes collected.\n")
    return all_quotes


# ──────────────────────────────────────────────────────────────
#  2. SAVING OUTPUT
# ──────────────────────────────────────────────────────────────

def save_csv(data, filepath):
    if not data:
        print("[WARN] No data — CSV not written.")
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ CSV  saved → {filepath}")


def save_json(data, filepath):
    if not data:
        print("[WARN] No data — JSON not written.")
        return
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON saved → {filepath}")


# ──────────────────────────────────────────────────────────────
#  3. CLI
# ──────────────────────────────────────────────────────────────

def build_cli():
    parser = argparse.ArgumentParser(
        prog="scraper",
        description=(
            "Web Scraper — Internship Task 2\n"
            "Scrapes quotes.toscrape.com and saves to CSV / JSON.\n\n"
            "Examples:\n"
            "  python scraper.py\n"
            "  python scraper.py --pages 5 --output json\n"
            "  python scraper.py --tag love --filename love_quotes\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-p", "--pages",    type=int,   default=3,      help="Pages to scrape (default: 3)")
    parser.add_argument("-o", "--output",   choices=["csv","json","both"], default="both", help="Output format (default: both)")
    parser.add_argument("-f", "--filename", default="quotes",           help="Base filename, no extension (default: quotes)")
    parser.add_argument("-t", "--tag",      default=None,               help="Filter by tag, e.g. --tag love")
    parser.add_argument("-d", "--delay",    type=float, default=1.0,    help="Seconds between requests (default: 1.0)")
    return parser


def main():
    parser = build_cli()
    args = parser.parse_args()

    data = run_scraper(pages=args.pages, delay=args.delay, tag=args.tag)

    if not data:
        print("[ERROR] No data scraped. Exiting.")
        sys.exit(1)

    if args.output in ("csv", "both"):
        save_csv(data, f"{args.filename}.csv")

    if args.output in ("json", "both"):
        save_json(data, f"{args.filename}.json")


if __name__ == "__main__":
    main()
