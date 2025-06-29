#!/usr/bin/env python3
"""CLI tool to fetch whitelisted sites into the local repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import requests


def read_sites(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def sanitize_html(html: str) -> str:
    """Placeholder for HTML sanitization."""
    return html


def fetch_site(url: str, output_dir: Path) -> None:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    domain = url.split("//", 1)[-1].split("/", 1)[0]
    dest = output_dir / "pages" / domain
    dest.mkdir(parents=True, exist_ok=True)
    sanitized = sanitize_html(resp.text)
    (dest / "index.html").write_text(sanitized, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch whitelisted sites")
    parser.add_argument("--sites", required=True, help="Path to file listing allowed URLs")
    parser.add_argument("--output", default="repository", help="Repository directory")
    args = parser.parse_args()

    sites_path = Path(args.sites)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    for url in read_sites(sites_path):
        fetch_site(url, output_dir)

    print(f"Fetched sites from {sites_path} into {output_dir}")


if __name__ == "__main__":
    main()
