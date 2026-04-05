"""
Smoke tests against the live Tailscale API.

Requires environment variables:
  TAILSCALE_OAUTH_CLIENT_ID     - OAuth client ID from the Tailscale admin console
  TAILSCALE_OAUTH_CLIENT_SECRET - OAuth client secret
  TAILSCALE_TAILNET             - Tailnet name (e.g. example.com)

Run with: pytest -m smoke
"""

import os
import pytest

from tailscale_agent.tailscale_agent import Tailscale


BASE_URL = 'https://api.tailscale.com/api/v2'


@pytest.fixture(scope='module')
def live_client():
    client_id = os.environ['TAILSCALE_OAUTH_CLIENT_ID']
    client_secret = os.environ['TAILSCALE_OAUTH_CLIENT_SECRET']
    tailnet = os.environ['TAILSCALE_TAILNET']

    client = Tailscale(api_key='', base_url=BASE_URL, tailnet=tailnet)
    resp = client.get_oauth_token(client_id, client_secret, client_embed=True)
    assert resp.status_code == 200, f'OAuth token exchange failed: {resp.text}'

    return client


@pytest.mark.smoke
def test_oauth_token_exchange(live_client):
    assert live_client._api_key != ''


@pytest.mark.smoke
def test_get_devices(live_client):
    resp = live_client.get_devices()
    assert resp.status_code == 200
    assert 'devices' in resp.json()


@pytest.mark.smoke
def test_get_acls(live_client):
    resp = live_client.get_acls()
    assert resp.status_code == 200


@pytest.mark.smoke
def test_get_keys(live_client):
    resp = live_client.get_keys()
    assert resp.status_code == 200


@pytest.mark.smoke
def test_get_nameservers(live_client):
    resp = live_client.get_nameservers()
    assert resp.status_code == 200
    assert 'dns' in resp.json()


@pytest.mark.smoke
def test_get_dns_preferences(live_client):
    resp = live_client.get_dns_preferences()
    assert resp.status_code == 200
    assert 'magicDNS' in resp.json()


@pytest.mark.smoke
def test_get_dns_searchpaths(live_client):
    resp = live_client.get_dns_searchpaths()
    assert resp.status_code == 200


@pytest.mark.smoke
def test_get_users(live_client):
    resp = live_client.get_users()
    assert resp.status_code == 200
    assert 'users' in resp.json()
