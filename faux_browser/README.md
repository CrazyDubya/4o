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
3. Implement a basic Electron client that loads pages from the static server (done).
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
and updates `manifest.json` with the local paths and SHA-256 hashes. The HTML is
sanitized to strip scripts and forms before being written to disk.

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
If a requested file cannot be found, the server now returns a simple HTML
placeholder instead of an error. This keeps navigation smooth and will later
allow AI helpers to fill in missing content.
Pass `--verify` to have the server check each file's SHA-256 against
`manifest.json`. If the hash does not match, a 500 error is returned.
The server also tracks how long it has been running and stops responding once
the user's configured time limit elapses.
All requests are logged to `repository/metadata/server_access.log` for auditing.
## Screenshot Fetcher

The optional `screenshot_fetcher.py` script uses `pyppeteer` to capture images of the sample domains.
Run:
```bash
python screenshot_fetcher.py
```
Screenshots are saved under `repository/screenshots/`.

## User Profiles

The offline server can enforce a profile of allowed domains, soft-permissive
domains, and session duration. Start the server with a JSON file defining
permissions and a time limit:

```bash
python offline_server.py --profile profiles/default.json
```

See [user_profiles.md](user_profiles.md) for details.
For ideas on tailoring domain lists for different audiences, check
[walled_gardens.md](walled_gardens.md).

## Electron Client

A small Electron application can display the cached pages in a locked-down
window. Install dependencies and start it from the `electron_frontend` directory:

```bash
cd electron_frontend
npm install
npm start
```

The client simply loads `http://localhost:8000/` and exposes minimal navigation
controls.


## Logging and Auditing

Activity logs live under `repository/metadata/`:

- `fetch_log.txt` records when pages were downloaded.
- `server_access.log` stores every offline server request.

See [auditing.md](auditing.md) for details.


## Ongoing Checklist

- use the new `fetcher.py` CLI to populate the repository
- generate `manifest.json` with hashes for each file (done)
- sanitize pages (done) and insert AI placeholders when needed
- create a simple Electron client bound to the offline server (done)
- add profile-based access controls and auditing (done)
- verify file hashes when serving (done)
- enforce session time limits from profile (done)

