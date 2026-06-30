# 🕸️ Web Scraper — Quotes Edition

A robust, polite, and well-structured CLI web scraper built with Python, Requests, and BeautifulSoup. Scrapes quotes from [quotes.toscrape.com](https://quotes.toscrape.com) with full pagination support, graceful error handling, and flexible CSV/JSON export.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-yellow)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## ✨ Features

- **Automatic Pagination** — Follows the "Next" button until the page limit or the data runs out
- **Tag Filtering** — Scrape only quotes belonging to a specific tag (e.g. `love`, `life`, `humor`)
- **Dual Export** — Save results to CSV, JSON, or both at once
- **Resilient Requests** — Gracefully handles connection errors, timeouts, and HTTP errors without crashing
- **Missing Data Fallbacks** — Defaults to `N/A` / `Unknown` instead of breaking on incomplete HTML
- **Polite Scraping** — Configurable delay between requests to avoid hammering the server
- **Clean CLI** — Built with `argparse`, including a custom `--help` with usage examples
- **Session Reuse** — Uses a persistent `requests.Session` with a custom User-Agent for efficiency

---

## 📸 Preview

```
====================================================
  Web Scraper  |  quotes.toscrape.com
  Max pages    : 3
====================================================

[PAGE 1] https://quotes.toscrape.com/
  → 10 quotes  |  Total: 10
[PAGE 2] https://quotes.toscrape.com/page/2/
  → 10 quotes  |  Total: 20
[PAGE 3] https://quotes.toscrape.com/page/3/
  → 10 quotes  |  Total: 30

✓ Done. 30 quotes collected.

✓ CSV  saved → quotes.csv
✓ JSON saved → quotes.json
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/web-scraper-quotes.git
cd web-scraper-quotes

# Install dependencies
pip install requests beautifulsoup4
```

> 💡 Tip: consider adding a `requirements.txt` with `requests` and `beautifulsoup4` for one-line installs (`pip install -r requirements.txt`).

---

## 🛠️ Usage

### Basic run (3 pages, CSV + JSON)
```bash
python scraper.py
```

### Scrape more pages
```bash
python scraper.py --pages 5
```

### Export only JSON
```bash
python scraper.py --output json
```

### Filter by tag
```bash
python scraper.py --tag love
```

### Custom output filename
```bash
python scraper.py --filename my_quotes
```

### Combine options
```bash
python scraper.py --pages 5 --tag life --filename life_quotes --output both --delay 1.5
```

### Show all options
```bash
python scraper.py --help
```

---

## ⚙️ CLI Options

| Flag | Short | Description | Default |
|---|---|---|---|
| `--pages` | `-p` | Number of pages to scrape | `3` |
| `--output` | `-o` | Output format: `csv`, `json`, or `both` | `both` |
| `--filename` | `-f` | Base filename (no extension) | `quotes` |
| `--tag` | `-t` | Filter quotes by tag | `None` |
| `--delay` | `-d` | Delay (seconds) between page requests | `1.0` |

---

## 📁 Project Structure

```
web-scraper-quotes/
├── scraper.py          # Main scraper script
├── quotes.csv           # Generated CSV output
├── quotes.json           # Generated JSON output
└── README.md
```

---

## 🧩 Sample Output

**`quotes.json`**
```json
[
  {
    "text": "The world as we have created it is a process of our thinking.",
    "author": "Albert Einstein",
    "tags": "change, deep-thoughts, thinking, world"
  },
  {
    "text": "It is our choices, Harry, that show what we truly are.",
    "author": "J.K. Rowling",
    "tags": "abilities, choices"
  }
]
```

**`quotes.csv`**
```
text,author,tags
"The world as we have created it...",Albert Einstein,"change, deep-thoughts, thinking, world"
"It is our choices, Harry...",J.K. Rowling,"abilities, choices"
```

---

## 🛡️ Error Handling

The scraper is built to fail gracefully rather than crash mid-run:

| Scenario | Behavior |
|---|---|
| No internet / connection refused | Logs an error and stops that page cleanly |
| Request timeout | Logs a timeout error and stops that page cleanly |
| HTTP error (404, 500, etc.) | Logs the status code and stops that page cleanly |
| Missing quote/author/tag in HTML | Falls back to `N/A` / `Unknown` instead of crashing |
| No data scraped at all | Exits with a clear error message and non-zero exit code |

---

## 🗺️ Roadmap

- [ ] `requirements.txt` for one-line dependency install
- [ ] Async scraping with `aiohttp` for faster multi-page runs
- [ ] Retry logic with exponential backoff
- [ ] Export to SQLite/Excel
- [ ] Support for additional target sites via config

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](../../issues) or open a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This scraper targets [quotes.toscrape.com](https://quotes.toscrape.com), a site built specifically for scraping practice. Always check a site's `robots.txt` and terms of service before scraping any other website, and scrape responsibly.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built as part of an internship task focused on practical Python web scraping.

<p align="center">Made with ❤️ and Python</p>
