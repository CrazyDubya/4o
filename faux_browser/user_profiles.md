# User Profiles

Profiles define which domains a user is allowed to browse and optionally how long a session may last. The offline server reads the profile JSON when it starts.

Example file `profiles/default.json`:

```json
{
  "allowed_domains": ["example.com"],
  "soft_allow_domains": ["www.iana.org"],
  "time_limit_minutes": 30
}
```

`soft_allow_domains` contains sites that are only accessible with approval. The server returns a message instead of content when these domains are requested.

Start the server with a profile and it will stop serving once the time limit is reached:

```bash
python offline_server.py --profile profiles/default.json
```

Several fully defined example profiles live in the same directory. Each contains
an expanded set of allowed and soft-allow domains:

- `kids.json` – safe browsing for children
- `research.json` – reference-focused garden for students or professionals
- `library.json` – curated sites for public terminals

Use any of these files with the `--profile` option to try different domain sets.
