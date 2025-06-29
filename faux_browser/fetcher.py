#!/usr/bin/env python3
"""CLI tool to fetch whitelisted sites into the local repository."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone
import requests


def read_sites(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def sanitize_html(html: str) -> str:
    """Placeholder for HTML sanitization."""
    return html


def file_hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_manifest(manifest: Path, url: str, file_path: Path) -> None:
    manifest_data = {}
    if manifest.exists():
        manifest_data = json.loads(manifest.read_text())

    relative = file_path.relative_to(manifest.parent)
    manifest_data[url] = {
        "path": str(relative),
        "sha256": file_hash(file_path),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

    manifest.write_text(json.dumps(manifest_data, indent=2))


def fetch_site(url: str, output_dir: Path, manifest: Path) -> None:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    domain = url.split("//", 1)[-1].split("/", 1)[0]
    dest = output_dir / "pages" / domain
    dest.mkdir(parents=True, exist_ok=True)
    sanitized = sanitize_html(resp.text)
    html_path = dest / "index.html"
    html_path.write_text(sanitized, encoding="utf-8")
    update_manifest(manifest, url, html_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch whitelisted sites")
    parser.add_argument("--sites", required=True, help="Path to file listing allowed URLs")
    parser.add_argument("--output", default="repository", help="Repository directory")
    args = parser.parse_args()

    sites_path = Path(args.sites)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = output_dir / "manifest.json"

    for url in read_sites(sites_path):
        fetch_site(url, output_dir, manifest)

    print(f"Fetched sites from {sites_path} into {output_dir}")


if __name__ == "__main__":
    main()
