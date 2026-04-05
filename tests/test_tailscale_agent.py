from unittest.mock import patch, MagicMock

import pytest

from tailscale_agent import __version__
from tailscale_agent.tailscale_agent import Tailscale


BASE_URL = 'https://api.tailscale.com/api/v2'
TAILNET = 'example.com'
API_KEY = 'tskey-test-abc123'


@pytest.fixture
def client():
    return Tailscale(api_key=API_KEY, base_url=BASE_URL, tailnet=TAILNET)


def mock_response(status_code=200, json_data=None):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data or {}
    return mock


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

def test_version():
    assert __version__ == '0.7.0'


# ---------------------------------------------------------------------------
# Constructor
# ---------------------------------------------------------------------------

def test_custom_headers_merged(client):
    custom = Tailscale(api_key=API_KEY, base_url=BASE_URL, tailnet=TAILNET,
                       headers={'X-Custom': 'value'})
    assert custom._headers['Accept'] == 'application/json'
    assert custom._headers['X-Custom'] == 'value'


def test_custom_headers_can_override_defaults():
    custom = Tailscale(api_key=API_KEY, base_url=BASE_URL,
                       headers={'Accept': 'text/hcl'})
    assert custom._headers['Accept'] == 'text/hcl'


# ---------------------------------------------------------------------------
# ACL methods
# ---------------------------------------------------------------------------

class TestAcls:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_acls_url(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_acls()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/acl',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_validate_acls(self, mock_post, client):
        mock_post.return_value = mock_response()
        acl = b'{"acls": []}'
        client.validate_acls(acl)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/acl/validate',
            auth=client._auth,
            headers=client._headers,
            data=acl,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_update_acls(self, mock_post, client):
        mock_post.return_value = mock_response()
        acl = b'{"acls": []}'
        client.update_acls(acl)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/acl',
            auth=client._auth,
            headers=client._headers,
            data=acl,
        )


# ---------------------------------------------------------------------------
# Device methods
# ---------------------------------------------------------------------------

class TestDevices:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_devices(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_devices()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/devices',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_device(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_device('device-123')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/device/device-123',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_authorize_device(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.authorize_device('device-123')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/authorized',
            auth=client._auth,
            headers=client._headers,
            json={'authorized': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_update_device_tags(self, mock_post, client):
        mock_post.return_value = mock_response()
        tags = ['tag:foo', 'tag:bar']
        client.update_device_tags('device-123', tags)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/tags',
            auth=client._auth,
            headers=client._headers,
            json={'tags': tags},
        )


# ---------------------------------------------------------------------------
# Device route methods
# ---------------------------------------------------------------------------

class TestDeviceRoutes:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_device_routes(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_device_routes('device-123')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/device/device-123/routes',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_device_routes(self, mock_post, client):
        mock_post.return_value = mock_response()
        routes = ['10.0.1.0/24', '192.168.1.0/24']
        client.set_device_routes('device-123', routes)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/routes',
            auth=client._auth,
            headers=client._headers,
            json={'routes': routes},
        )


# ---------------------------------------------------------------------------
# Key methods
# ---------------------------------------------------------------------------

class TestKeys:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_keys(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_keys()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_key(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_key('key-abc')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys/key-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_authorization_keys(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_authorization_keys()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys',
            auth=client._auth,
            headers=client._headers,
        )


# ---------------------------------------------------------------------------
# DNS methods
# ---------------------------------------------------------------------------

class TestDns:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_nameservers(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_nameservers()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/nameservers',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_nameservers(self, mock_post, client):
        mock_post.return_value = mock_response()
        ns = ['1.1.1.1', '8.8.8.8']
        client.set_nameservers(ns)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/nameservers',
            auth=client._auth,
            headers=client._headers,
            json={'dns': ns},
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_dns_preferences(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_dns_preferences()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/preferences',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_dns_preferences(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_dns_preferences(True)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/preferences',
            auth=client._auth,
            headers=client._headers,
            json={'magicDNS': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_dns_searchpaths(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_dns_searchpaths()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/searchpaths',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_dns_searchpaths_uses_post(self, mock_post, client):
        """set_dns_searchpaths must POST, not GET."""
        mock_post.return_value = mock_response()
        paths = ['example.com', 'internal.example.com']
        client.set_dns_searchpaths(paths)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/searchpaths',
            auth=client._auth,
            headers=client._headers,
            json={'searchPaths': paths},
        )


# ---------------------------------------------------------------------------
# Logs methods
# ---------------------------------------------------------------------------

class TestLogs:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_audit_logs(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_audit_logs('2024-01-01T00:00:00Z', '2024-01-02T00:00:00Z')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/logs?start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_logs_alias(self, mock_get, client):
        """get_logs should be an alias for get_audit_logs."""
        mock_get.return_value = mock_response()
        client.get_logs('2024-01-01T00:00:00Z', '2024-01-02T00:00:00Z')
        mock_get.assert_called_once()

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_network_logs(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_network_logs('2024-01-01T00:00:00Z', '2024-01-02T00:00:00Z')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/network-logs?start=2024-01-01T00:00:00Z&end=2024-01-02T00:00:00Z',
            auth=client._auth,
            headers=client._headers,
        )


# ---------------------------------------------------------------------------
# OAuth methods
# ---------------------------------------------------------------------------

class TestOAuth:
    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_get_oauth_token_no_embed(self, mock_post, client):
        mock_post.return_value = mock_response(json_data={'access_token': 'new-token'})
        client.get_oauth_token('client-id', 'client-secret', client_embed=False)
        mock_post.assert_called_once_with(
            'https://api.tailscale.com/api/v2/oauth/token',
            headers=client._headers,
            data={'client_id': 'client-id', 'client_secret': 'client-secret'},
        )
        assert client._api_key == API_KEY  # unchanged

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_get_oauth_token_embeds_token(self, mock_post, client):
        mock_post.return_value = mock_response(json_data={'access_token': 'new-token'})
        client.get_oauth_token('client-id', 'client-secret', client_embed=True)
        assert client._api_key == 'new-token'
        assert client._auth.username == 'new-token'

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_get_oauth_token_bad_response_does_not_raise(self, mock_post, client):
        """If the token response is missing access_token, it should print and not crash."""
        mock_post.return_value = mock_response(json_data={'error': 'bad credentials'})
        # Should not raise — just print a message
        client.get_oauth_token('bad-id', 'bad-secret', client_embed=True)
        assert client._api_key == API_KEY  # unchanged


# ---------------------------------------------------------------------------
# User methods
# ---------------------------------------------------------------------------

class TestUsers:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_users(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_users()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/users',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_user(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_user('user-456')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/users/user-456',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_update_user_role(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.update_user_role('user-456', 'admin')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/users/user-456/role',
            auth=client._auth,
            headers=client._headers,
            json={'role': 'admin'},
        )
