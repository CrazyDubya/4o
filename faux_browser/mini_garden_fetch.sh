#!/bin/bash
# Fetch a small set of sample pages for the faux browser repository.
set -euo pipefail

OUTPUT_DIR="${1:-faux_browser/repository}"
PAGES_DIR="$OUTPUT_DIR/pages"
LOG_DIR="$OUTPUT_DIR/metadata"
mkdir -p "$PAGES_DIR" "$LOG_DIR"
LOG_FILE="$LOG_DIR/fetch_log.txt"

fetch_site() {
    local url="$1"
    local domain
    domain=$(echo "$url" | awk -F/ '{print $3}')
    local target_dir="$PAGES_DIR/$domain"
    mkdir -p "$target_dir"
    curl -Ls "$url" -o "$target_dir/index.html"
    echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') fetched $url" >> "$LOG_FILE"
}

fetch_site "https://example.com"
fetch_site "https://www.iana.org/domains/example"

echo "Pages stored in $PAGES_DIR" && ls -R "$PAGES_DIR"
