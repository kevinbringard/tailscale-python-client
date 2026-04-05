# tailscale-python-client — Claude Code Instructions

## Tech stack

- **Language:** Python 3.11+
- **HTTP:** `requests` library (raw `requests.Response` objects returned — no parsing, no raising on error status)
- **Packaging:** Poetry (`pyproject.toml`)
- **Tests:** pytest

## Commands

```bash
# Install dependencies
poetry install

# Run unit tests (no credentials required)
poetry run pytest tests/ -v -m "not smoke"

# Run smoke tests (live API — requires env vars below)
poetry run pytest tests/test_smoke.py -v -m smoke
```

Smoke test env vars: `TAILSCALE_OAUTH_CLIENT_ID`, `TAILSCALE_OAUTH_CLIENT_SECRET`, `TAILSCALE_TAILNET`

## Layout

```
tailscale_agent/tailscale_agent.py   # All client code — single Tailscale class
tests/test_tailscale_agent.py        # Unit tests (mocked)
tests/test_smoke.py                  # Live API smoke tests
```

## Tailscale API reference

- **Full API docs:** https://tailscale.com/api
- **OAuth guide:** https://tailscale.com/kb/1215/oauth-clients/
- **Base URL in production:** `https://api.tailscale.com/api/v2`

Always check the API docs for required/optional fields before adding or fixing a method.

## Non-obvious design decisions

**Auth:** `_auth` holds an `HTTPBasicAuth(api_key, '')` object. `get_oauth_token()` with `client_embed=True` (the default) replaces `_auth` in-place with the returned token — callers don't need to re-instantiate.

**ACL methods use `data=` not `json=`:** `validate_acls` and `update_acls` pass the ACL body as binary data (`data=acl_json`). This is intentional — the Tailscale API requires the raw file bytes, not a re-serialized JSON object. Don't change this to `json=`.

**Deprecated aliases:** `get_keys()` → `get_authorization_keys()`, `get_logs()` → `get_audit_logs()`. Both emit `DeprecationWarning`. Prefer the descriptive names when adding new code or tests.

**Naming convention:** Use the more descriptive method name when there's a choice (e.g. `get_authorization_keys` over `get_keys`).
