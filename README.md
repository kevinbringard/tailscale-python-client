# tailscale-python-client

Python bindings for the [Tailscale API](https://tailscale.com/api).

> **Work in progress** — not all API endpoints are implemented yet.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) (for development)

## Installation

```bash
pip install tailscale-agent
```

## Usage

### API key auth

```python
from tailscale_agent import Tailscale

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
    api_key='',  # placeholder — will be replaced after token exchange
    base_url='https://api.tailscale.com/api/v2',
    tailnet='example.com',
)

# Fetches a token and embeds it into the client for subsequent calls
client.get_oauth_token(
    client_id='your-oauth-client-id',
    client_secret='your-oauth-client-secret',
)

resp = client.get_devices()
```

See the [Tailscale OAuth guide](https://tailscale.com/kb/1215/oauth-clients/) for how to create an OAuth client.

## Available methods

All methods return a [`requests.Response`](https://docs.python-requests.org/en/latest/api/#requests.Response) object. Check `resp.status_code` and call `resp.json()` to inspect the result.

### ACLs
| Method | Description |
|--------|-------------|
| `get_acls()` | Get the tailnet ACL |
| `validate_acls(acl_json)` | Validate ACL JSON against the Tailscale validator |
| `update_acls(acl_json)` | Replace the tailnet ACL |

### Devices
| Method | Description |
|--------|-------------|
| `get_devices()` | List all devices in the tailnet |
| `get_device(device_id)` | Get details for a specific device |
| `authorize_device(device_id)` | Authorize a device (required on tailnets with device authorization enabled) |
| `update_device_tags(device_id, tags)` | Replace the tags on a device |
| `get_device_routes(device_id)` | Get advertised and enabled subnet routes for a device |
| `set_device_routes(device_id, routes)` | Set enabled subnet routes for a device |

### Keys
| Method | Description |
|--------|-------------|
| `get_authorization_keys()` | List auth keys for the tailnet |
| `get_key(key_id)` | Get details for a specific key |
| `create_authorization_key(capabilities, expiry_seconds=None, description=None)` | Create a new auth key |

### DNS
| Method | Description |
|--------|-------------|
| `get_nameservers()` | List DNS nameservers |
| `set_nameservers(nameservers)` | Replace DNS nameservers |
| `get_dns_preferences()` | Get DNS preferences (MagicDNS setting) |
| `set_dns_preferences(dns_preferences)` | Set DNS preferences |
| `get_dns_searchpaths()` | Get DNS search paths |
| `set_dns_searchpaths(dns_searchpaths)` | Replace DNS search paths |

### Logs
| Method | Description |
|--------|-------------|
| `get_audit_logs(starttime, endtime)` | Get audit logs (ISO-8601 timestamps required) |
| `get_network_logs(starttime, endtime)` | Get network flow logs (must be enabled in admin console) |

### Users
| Method | Description |
|--------|-------------|
| `get_users()` | List all users in the tailnet |
| `get_user(user_id)` | Get details for a specific user |
| `update_user_role(user_id, role)` | Update a user's role |

### OAuth
| Method | Description |
|--------|-------------|
| `get_oauth_token(client_id, client_secret, client_embed=True)` | Exchange OAuth credentials for an access token |

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
