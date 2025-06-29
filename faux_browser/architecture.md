# Architecture Overview

```
+-----------------+     fetch     +----------------------+    serve   +-------------------+
|  Intermediary   | ------------> |    Local Repository  | ---------> |    Faux Browser   |
|   (Scraper)     |               |    (Sanitized Cache) |            |  (Locked WebView) |
+-----------------+               +----------------------+            +-------------------+
       ^                                                         |
       | audit                                                   |
       +---------------------------------------------------------+
```

1. **Intermediary (Scraper)**
   - Connects to the real Internet under controlled rules.
   - Downloads content from a whitelist of sites.
   - Removes dynamic scripts and stores static copies in the repository.

2. **Local Repository**
   - Directory tree with sanitized HTML, images, and other assets.
   - Indexed for quick retrieval by the faux browser.

3. **Offline Server**
   - Small HTTP server that exposes the repository over `localhost`.
   - Used by the browser to fetch sanitized pages.

4. **Faux Browser**
   - A simple UI (e.g. Electron app) that only points to the offline server.
   - Blocks external URLs at the network level.
   - AI components can synthesize or summarize content when required.
   - User profiles restrict accessible domains.

This layout ensures that the user never directly contacts the Internet, yet can view a curated snapshot of it.

5. **Service Worker Layer**
   - The faux browser registers a service worker that intercepts every request.
   - It serves files from the local repository and injects AI-generated placeholders for missing content.

6. **Audit Trail**
   - All fetcher activities and user navigation events are logged for review.

