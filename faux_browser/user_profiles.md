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

`soft_allow_domains` contains sites that are only accessible with approval.
The server returns a message instead of content when these domains are
requested.

Start the server with the profile. The server shuts down requests once the
configured time limit is reached:

```bash
python offline_server.py --profile profiles/default.json
```
