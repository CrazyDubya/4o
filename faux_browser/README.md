# Faux Web Browser Concept

This directory outlines an early conceptual plan for a "faux" web browser. The goal is to render a curated portion of the web without giving users full access to the Internet. Content is served from offline copies or generated with AI so that vulnerable users can browse safely.

## Motivation

* Restrict the user's exposure to unknown sites.
* Protect minors or users with limited capacity from harmful content.
* Prevent fraud, hacking, and other malicious activity by limiting the network surface.

## Core Ideas

1. **Local Mirrors**
   - A scraping service periodically fetches approved websites and stores them in a local cache.
   - Pages are sanitized to remove scripts or forms that make outbound requests.
   - The faux browser only loads content from this cache.

2. **AI-Filled Gaps**
   - When a page element is missing or out of date, the system can generate text or simple imagery using local AI models.
   - This allows the environment to present fresh-looking pages without direct Internet access.

3. **Walled Garden Navigation**
   - The faux browser prevents navigation outside the cached domain list.
   - Links to disallowed domains trigger either an informative message or an AI-generated approximation instead of an external request.

4. **Intermediary Pipeline**
   - A separate service with Internet access updates the local cache.
   - It enforces filtering rules and logs external requests for audit.

## Deployment Sketch

1. **Create the Content Fetcher**
   - Runs on a secure server with controlled network access.
   - Downloads approved sites on a schedule.
   - Sanitizes and indexes the content into the local store.

2. **Offline Content Server**
   - Simple HTTP server that serves the cached pages.
   - May inject AI-generated sections before delivering to the client.

3. **Custom Browser Front-End**
   - Locked-down Electron or WebView application.
   - Hardcoded to request pages only from the offline server.
   - Provides minimal address bar and navigation controls.

4. **User Management and Safety Controls**
   - Profiles define which sites are available for each user.
   - Logs usage and optionally uses AI to flag unusual behavior.

## Next Steps

1. Prototype the content fetcher with a small set of websites.
2. Build a simple static server to host the cached pages.
3. Implement a basic Electron client that loads pages from the static server.
4. Explore offline language models for filling missing text or generating explanations.

This plan is intentionally high-level. The goal is to demonstrate how a limited subset of the web could be served without exposing users directly to the wider Internet.

## Service Worker Strategy

The faux browser can register a service worker that intercepts all navigation requests. The worker checks the local repository first and falls back to an AI-generated response when needed. This keeps the browsing experience seamless even when pages are partially missing.

## Example Fetch Command

The project provides a small CLI fetcher. Give it a text file of URLs and an
output directory:

```bash
python fetcher.py --sites whitelist.txt --output repository/
```

`whitelist.txt` lists the allowed domains. Each run stores the downloaded files
and records the fetch in the repository metadata.

## Mini Garden Proof of Concept

To collect a small sample set of pages without accessing the wider Internet,
use the provided helper script:

```bash
./mini_garden_fetch.sh
```

The script fetches `example.com` and IANA's example domain page via `curl`. The
files are stored under `repository/pages/` and a simple log is written to
`repository/metadata/fetch_log.txt`. Because the repository directory is listed
in `.gitignore`, these fetched files are not tracked by Git and can be
regenerated at any time.

## Local Offline Server

Once pages have been fetched, you can serve them locally using a small
HTTP server:

```bash
python offline_server.py --repo repository --port 8000
```

This starts a server at `http://localhost:8000/` that hosts the cached
content. Open `http://localhost:8000/pages/example.com/` in your browser to
view the sample page.
## Screenshot Fetcher

The optional `screenshot_fetcher.py` script uses `pyppeteer` to capture images of the sample domains.
Run:
```bash
python screenshot_fetcher.py
```
Screenshots are saved under `repository/screenshots/`.


## Ongoing Checklist

- use the new `fetcher.py` CLI to populate the repository
- generate `manifest.json` with hashes for each file
- sanitize pages and insert AI placeholders when needed
- create a simple Electron client bound to the offline server
- add profile-based access controls and auditing

