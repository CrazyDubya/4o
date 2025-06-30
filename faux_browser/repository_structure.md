# Local Repository Structure

This document describes the layout of the sanitized content store used by the faux browser.

```
repository/
  manifest.json        # Maps original URLs to cached files
  pages/
    example.com/
      index.html
      images/
        logo.png
  metadata/        # Default log directory (configurable)
    fetch_log.json     # Records timestamps and fetch status
    server_access.log  # HTTP requests served by the offline server
    approval_requests.log # Soft-allow domain attempts
  profiles/
    default.json       # Example user profile
electron_frontend/    # Minimal Electron client
```

- **manifest.json** lists each allowed URL, the local path of the cached copy, the SHA-256 hash, and when it was fetched.
- **pages/** holds directories for each domain with sanitized HTML and assets.
  - **metadata/** contains logs produced by the fetcher and server for auditing
    (or another directory if `--log-dir` is used). Files include `fetch_log.txt`,
    `server_access.log`, and `approval_requests.log`.
- **profiles/** stores JSON files listing allowed domains and time limits for each user.
- The offline server can optionally verify each file against `manifest.json` when serving content.

Keeping a clear structure makes it easy for the offline server and browser to resolve requests without contacting the real Internet.
