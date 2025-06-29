# User Profiles

Profiles define which domains a user is allowed to browse and optionally how long a session may last. The offline server reads the profile JSON when it starts.

Example file `profiles/default.json`:

```json
{
  "allowed_domains": ["example.com"],
  "time_limit_minutes": 30
}
```

Start the server with the profile:

```bash
python offline_server.py --profile profiles/default.json
```
