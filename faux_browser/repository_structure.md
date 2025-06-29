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
  metadata/
    fetch_log.json     # Records timestamps and fetch status
```

- **manifest.json** lists each allowed URL, the local path of the cached copy, and when it was fetched.
- **pages/** holds directories for each domain with sanitized HTML and assets.
- **metadata/** contains logs produced by the fetcher for audit and troubleshooting.

Keeping a clear structure makes it easy for the offline server and browser to resolve requests without contacting the real Internet.
