# Walled Garden Strategy

This document records several curated domain lists ("walled gardens") that can be used as starting points when creating user profiles. Each example corresponds to a JSON file in `profiles/` so the offline server can enforce it directly. Feel free to modify these lists as the project evolves.

## Domain Categories

- **Allowed Domains** – Pages that are always accessible once mirrored locally.
- **Soft-Allow Domains** – Sites that require explicit approval. The server denies them by default and logs the attempt.
- **Blocked Domains** – Pages that should never be served to the user. They are removed from the repository and requests are logged.

## Example Gardens

### Kids Garden (`profiles/kids.json`)
A safe browsing environment for young users.

- `allowed_domains` include educational and age-appropriate entertainment:
  - `kids.nationalgeographic.com`
  - `pbskids.org`
  - `khanacademy.org`
  - `www.coolmathgames.com`
- `soft_allow_domains` require a parent's approval:
  - `www.youtube.com`
  - `en.wikipedia.org`
  - `code.org`
- `time_limit_minutes`: `60`

### Research Garden (`profiles/research.json`)
Designed for students or researchers who need reference material.

- `allowed_domains`:
  - `arxiv.org`
  - `doi.org`
  - `www.wikipedia.org`
  - `www.python.org`
  - `docs.python.org`
- `soft_allow_domains`:
  - `news.ycombinator.com`
  - `github.com`
- `time_limit_minutes`: `180`

### Library Garden (`profiles/library.json`)
For shared devices in a community space such as a public library.

- `allowed_domains`:
  - `www.local-library.gov`
  - `openlibrary.org`
  - `archive.org`
  - `gutenberg.org`
- `soft_allow_domains`:
  - `www.nytimes.com`
  - `www.wikipedia.org`
- `time_limit_minutes`: `90`

Each of these gardens illustrates how the faux browser can be tailored for different audiences. The lists are intentionally conservative and can be expanded as needed. When the offline server starts with one of these profile files, it enforces the domain rules and logs any attempts to visit soft-allow or blocked sites.
