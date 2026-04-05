# tailscale-python-client

Python bindings for the [Tailscale API](https://tailscale.com/api).

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) (for development)

## Installation

```bash
pip install tailscale-agent
```

## Quick start

### API key auth

```python
from tailscale_agent.tailscale_agent import Tailscale

client = Tailscale(
    api_key='tskey-api-...',
    base_url='https://api.tailscale.com/api/v2',
    tailnet='example.com',
)

resp = client.get_devices()
print(resp.json())
```

### OAuth auth

```python
client = Tailscale(
    api_key='',  # replaced after token exchange
    base_url='https://api.tailscale.com/api/v2',
    tailnet='example.com',
)
client.get_oauth_token(
    client_id='your-oauth-client-id',
    client_secret='your-oauth-client-secret',
)
```

See the [Tailscale OAuth guide](https://tailscale.com/kb/1215/oauth-clients/) for how to create an OAuth client.

## Documentation

- [Method reference](docs/methods.md) — all available methods grouped by resource
- [Examples](docs/examples.md) — practical recipes for common tasks

## Development with AI assistance

This project was developed with the assistance of [Claude Code](https://claude.ai/code) by Anthropic.

## Development

```bash
# Install dependencies
poetry install

# Run unit tests
poetry run pytest tests/ -v -m "not smoke"

# Run live smoke tests (requires credentials)
export TAILSCALE_OAUTH_CLIENT_ID=...
export TAILSCALE_OAUTH_CLIENT_SECRET=...
export TAILSCALE_TAILNET=...
poetry run pytest tests/test_smoke.py -v -m smoke
```
