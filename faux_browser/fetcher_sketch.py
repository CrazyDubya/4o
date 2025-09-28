"""Simple sketch of the content fetcher."""

import requests
from pathlib import Path

WHITELIST = [
    "https://example.com",
]

OUTPUT_DIR = Path("repository")


def fetch_site(url: str):
    resp = requests.get(url)
    resp.raise_for_status()
    # This example just writes the raw HTML. In practice, sanitize first.
    domain = url.split("//", 1)[-1].split("/", 1)[0]
    domain_dir = OUTPUT_DIR / "pages" / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    (domain_dir / "index.html").write_text(resp.text)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for url in WHITELIST:
        fetch_site(url)
    print("Fetch complete")


if __name__ == "__main__":
    main()
