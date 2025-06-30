# Logging and Auditing Strategy

This document outlines how the faux browser components record activity for later review.

## Fetcher Logs

- The `mini_garden_fetch.sh` helper records each successful fetch to
  `repository/metadata/fetch_log.txt`.
- The Python `fetcher.py` script updates `manifest.json` with a timestamp and
  SHA-256 hash whenever it stores a page.

## Offline Server Logs

- Every HTTP request handled by `offline_server.py` is appended to
  `repository/metadata/server_access.log` with an ISO timestamp and the path
  requested.
- Attempts to access soft-allow domains are written to
  `repository/metadata/approval_requests.log` for later review.
- Missing pages are also logged so you can identify gaps in the repository.
- When run with `--verify`, the server checks file hashes and notes mismatches.

These logs provide an audit trail showing what content was fetched and which
pages users attempted to view. They can be rotated or archived periodically to
maintain a history without consuming excessive disk space.
