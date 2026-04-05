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

def test_repr_redacts_api_key(client):
    result = repr(client)
    assert API_KEY not in result
    assert '********' + API_KEY[-4:] in result


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

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_preview_acl_rules(self, mock_post, client):
        mock_post.return_value = mock_response()
        acl = b'{"acls": []}'
        client.preview_acl_rules(acl, acl_type='user', preview_for='user@example.com')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/acl/preview?type=user&previewFor=user@example.com',
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

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_device(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_device('device-123')
        mock_delete.assert_called_once_with(
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
    def test_expire_device_key(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.expire_device_key('device-123')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/expire',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_device_name(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_device_name('device-123', 'my-device')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/name',
            auth=client._auth,
            headers=client._headers,
            json={'name': 'my-device'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_update_device_key(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.update_device_key('device-123', key_expiry_disabled=True)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/key',
            auth=client._auth,
            headers=client._headers,
            json={'keyExpiryDisabled': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_device_ipv4(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_device_ipv4('device-123', '100.64.0.1')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/ip',
            auth=client._auth,
            headers=client._headers,
            json={'ipv4': '100.64.0.1'},
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
# Device Posture Attribute methods
# ---------------------------------------------------------------------------

class TestDevicePostureAttributes:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_device_posture_attributes(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_device_posture_attributes('device-123')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/device/device-123/attributes',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_device_posture_attribute(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_device_posture_attribute('device-123', 'custom:compliant', True)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/attributes/custom:compliant',
            auth=client._auth,
            headers=client._headers,
            json={'value': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_device_posture_attribute_with_options(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_device_posture_attribute('device-123', 'custom:score', 42,
                                             expiry='2026-12-31T00:00:00Z', comment='audit')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/attributes/custom:score',
            auth=client._auth,
            headers=client._headers,
            json={'value': 42, 'expiry': '2026-12-31T00:00:00Z', 'comment': 'audit'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_device_posture_attribute(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_device_posture_attribute('device-123', 'custom:compliant')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/device/device-123/attributes/custom:compliant',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_batch_update_device_posture_attributes(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        nodes = {'device-123': {'custom:compliant': True}, 'device-456': {'custom:compliant': False}}
        client.batch_update_device_posture_attributes(nodes)
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/device-attributes',
            auth=client._auth,
            headers=client._headers,
            json={'nodes': nodes},
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_batch_update_device_posture_attributes_with_comment(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        nodes = {'device-123': {'custom:compliant': True}}
        client.batch_update_device_posture_attributes(nodes, comment='quarterly audit')
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/device-attributes',
            auth=client._auth,
            headers=client._headers,
            json={'nodes': nodes, 'comment': 'quarterly audit'},
        )


# ---------------------------------------------------------------------------
# Device Invite methods
# ---------------------------------------------------------------------------

class TestDeviceInvites:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_list_device_invites(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.list_device_invites('device-123')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/device/device-123/device-invites',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_device_invites(self, mock_post, client):
        mock_post.return_value = mock_response()
        invites = [{'email': 'friend@example.com', 'allowExitNode': False}]
        client.create_device_invites('device-123', invites)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device/device-123/device-invites',
            auth=client._auth,
            headers=client._headers,
            json=invites,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_device_invite(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_device_invite('invite-abc')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/device-invites/invite-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_device_invite(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_device_invite('invite-abc')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/device-invites/invite-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_resend_device_invite(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.resend_device_invite('invite-abc')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device-invites/invite-abc/resend',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_accept_device_invite(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.accept_device_invite('https://invite.tailscale.com/abc123')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/device-invites/-/accept',
            auth=client._auth,
            headers=client._headers,
            json={'invite': 'https://invite.tailscale.com/abc123'},
        )


# ---------------------------------------------------------------------------
# Key methods
# ---------------------------------------------------------------------------

class TestKeys:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_keys_deprecated(self, mock_get, client):
        mock_get.return_value = mock_response()
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            client.get_keys()
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "get_authorization_keys" in str(w[0].message)
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

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_authorization_key(self, mock_post, client):
        mock_post.return_value = mock_response()
        capabilities = {'devices': {'create': {'reusable': False, 'ephemeral': False, 'preauthorized': False}}}
        client.create_authorization_key(capabilities)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys',
            auth=client._auth,
            headers=client._headers,
            json={'capabilities': capabilities},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_authorization_key_with_options(self, mock_post, client):
        mock_post.return_value = mock_response()
        capabilities = {'devices': {'create': {'reusable': True, 'ephemeral': False, 'preauthorized': True}}}
        client.create_authorization_key(capabilities, expiry_seconds=3600, description='test key')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys',
            auth=client._auth,
            headers=client._headers,
            json={'capabilities': capabilities, 'expirySeconds': 3600, 'description': 'test key'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_key(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_key('key-abc')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys/key-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.put')
    def test_update_key(self, mock_put, client):
        mock_put.return_value = mock_response()
        client.update_key('key-abc', key_type='client', scopes=['devices:read'])
        mock_put.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys/key-abc',
            auth=client._auth,
            headers=client._headers,
            json={'keyType': 'client', 'scopes': ['devices:read']},
        )

    @patch('tailscale_agent.tailscale_agent.requests.put')
    def test_update_key_with_options(self, mock_put, client):
        mock_put.return_value = mock_response()
        client.update_key('key-abc', key_type='federated', scopes=['devices:read'],
                          description='ci key', issuer='https://issuer.example.com',
                          subject='repo:org/repo:ref:refs/heads/main')
        mock_put.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/keys/key-abc',
            auth=client._auth,
            headers=client._headers,
            json={
                'keyType': 'federated',
                'scopes': ['devices:read'],
                'description': 'ci key',
                'issuer': 'https://issuer.example.com',
                'subject': 'repo:org/repo:ref:refs/heads/main',
            },
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

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_split_dns(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_split_dns()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/split-dns',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_split_dns(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        split = {'internal.example.com': ['192.168.1.1']}
        client.update_split_dns(split)
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/split-dns',
            auth=client._auth,
            headers=client._headers,
            json=split,
        )

    @patch('tailscale_agent.tailscale_agent.requests.put')
    def test_set_split_dns(self, mock_put, client):
        mock_put.return_value = mock_response()
        split = {'internal.example.com': ['192.168.1.1']}
        client.set_split_dns(split)
        mock_put.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/split-dns',
            auth=client._auth,
            headers=client._headers,
            json=split,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_dns_configuration(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_dns_configuration()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/configuration',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_dns_configuration(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_dns_configuration(
            nameservers=['1.1.1.1'],
            split_dns={'corp.example.com': ['10.0.0.1']},
            search_paths=['example.com'],
            preferences={'magicDNS': True},
        )
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/configuration',
            auth=client._auth,
            headers=client._headers,
            json={
                'nameservers': ['1.1.1.1'],
                'splitDNS': {'corp.example.com': ['10.0.0.1']},
                'searchPaths': ['example.com'],
                'preferences': {'magicDNS': True},
            },
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_set_dns_configuration_partial(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.set_dns_configuration(nameservers=['8.8.8.8'])
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/dns/configuration',
            auth=client._auth,
            headers=client._headers,
            json={'nameservers': ['8.8.8.8']},
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

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_log_stream_status(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_log_stream_status('configuration')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/logging/configuration/stream/status',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_log_stream_config(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_log_stream_config('network')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/logging/network/stream',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.put')
    def test_set_log_stream_config(self, mock_put, client):
        mock_put.return_value = mock_response()
        client.set_log_stream_config('configuration', 'splunk', 'https://splunk.example.com', token='mytoken')
        mock_put.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/logging/configuration/stream',
            auth=client._auth,
            headers=client._headers,
            json={'destinationType': 'splunk', 'url': 'https://splunk.example.com', 'token': 'mytoken'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_log_stream_config(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_log_stream_config('network')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/logging/network/stream',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_get_aws_external_id(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.get_aws_external_id()
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/aws-external-id',
            auth=client._auth,
            headers=client._headers,
            json={},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_get_aws_external_id_reusable(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.get_aws_external_id(reusable=True)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/aws-external-id',
            auth=client._auth,
            headers=client._headers,
            json={'reusable': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_validate_aws_trust_policy(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.validate_aws_trust_policy('ext-id-123', 'arn:aws:iam::123456789012:role/MyRole')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/aws-external-id/ext-id-123/validate-aws-trust-policy',
            auth=client._auth,
            headers=client._headers,
            json={'roleArn': 'arn:aws:iam::123456789012:role/MyRole'},
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
            f'{BASE_URL}/oauth/token',
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
# Tailnet Settings methods
# ---------------------------------------------------------------------------

class TestTailnetSettings:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_tailnet_settings(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_tailnet_settings()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/settings',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_tailnet_settings(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        client.update_tailnet_settings(devices_approval_on=True, https_enabled=True)
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/settings',
            auth=client._auth,
            headers=client._headers,
            json={'devicesApprovalOn': True, 'httpsEnabled': True},
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_tailnet_settings_omits_none(self, mock_patch, client):
        """None params must not appear in the request body."""
        mock_patch.return_value = mock_response()
        client.update_tailnet_settings(network_flow_logging_on=True)
        body = mock_patch.call_args.kwargs['json']
        assert body == {'networkFlowLoggingOn': True}
        assert 'devicesApprovalOn' not in body


# ---------------------------------------------------------------------------
# Contacts methods
# ---------------------------------------------------------------------------

class TestContacts:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_contacts(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_contacts()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/contacts',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_contact(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        client.update_contact('security', 'security@example.com')
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/contacts/security',
            auth=client._auth,
            headers=client._headers,
            json={'email': 'security@example.com'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_resend_contact_verification(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.resend_contact_verification('support')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/contacts/support/resend-verification-email',
            auth=client._auth,
            headers=client._headers,
        )


# ---------------------------------------------------------------------------
# Device Posture Integration methods
# ---------------------------------------------------------------------------

class TestPostureIntegrations:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_list_posture_integrations(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.list_posture_integrations()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/posture/integrations',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_posture_integration(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.create_posture_integration('intune', 'client-id', 'client-secret', tenant_id='tenant-123')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/posture/integrations',
            auth=client._auth,
            headers=client._headers,
            json={'provider': 'intune', 'clientId': 'client-id', 'clientSecret': 'client-secret', 'tenantId': 'tenant-123'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_posture_integration(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_posture_integration('integration-abc')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/posture/integrations/integration-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_posture_integration(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        client.update_posture_integration('integration-abc', client_secret='new-secret')
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/posture/integrations/integration-abc',
            auth=client._auth,
            headers=client._headers,
            json={'clientSecret': 'new-secret'},
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_posture_integration(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_posture_integration('integration-abc')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/posture/integrations/integration-abc',
            auth=client._auth,
            headers=client._headers,
        )


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

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_approve_user(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.approve_user('user-456')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/users/user-456/approve',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_suspend_user(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.suspend_user('user-456')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/users/user-456/suspend',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_restore_user(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.restore_user('user-456')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/users/user-456/restore',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_delete_user(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.delete_user('user-456')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/users/user-456/delete',
            auth=client._auth,
            headers=client._headers,
        )


# ---------------------------------------------------------------------------
# User Invite methods
# ---------------------------------------------------------------------------

class TestUserInvites:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_list_user_invites(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.list_user_invites()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/user-invites',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_user_invites(self, mock_post, client):
        mock_post.return_value = mock_response()
        invites = [{'role': 'member', 'email': 'new@example.com'}]
        client.create_user_invites(invites)
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/user-invites',
            auth=client._auth,
            headers=client._headers,
            json=invites,
        )

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_user_invite(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_user_invite('invite-xyz')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/user-invites/invite-xyz',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_user_invite(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_user_invite('invite-xyz')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/user-invites/invite-xyz',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_resend_user_invite(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.resend_user_invite('invite-xyz')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/user-invites/invite-xyz/resend',
            auth=client._auth,
            headers=client._headers,
        )


# ---------------------------------------------------------------------------
# Webhook methods
# ---------------------------------------------------------------------------

class TestWebhooks:
    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_list_webhooks(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.list_webhooks()
        mock_get.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/webhooks',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_webhook(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.create_webhook('https://hooks.example.com/ts', ['nodeCreated', 'nodeDeleted'])
        mock_post.assert_called_once_with(
            f'{BASE_URL}/tailnet/{TAILNET}/webhooks',
            auth=client._auth,
            headers=client._headers,
            json={'endpointUrl': 'https://hooks.example.com/ts', 'subscriptions': ['nodeCreated', 'nodeDeleted']},
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_create_webhook_with_provider(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.create_webhook('https://hooks.slack.com/...', ['nodeCreated'], provider_type='slack')
        body = mock_post.call_args.kwargs['json']
        assert body['providerType'] == 'slack'

    @patch('tailscale_agent.tailscale_agent.requests.get')
    def test_get_webhook(self, mock_get, client):
        mock_get.return_value = mock_response()
        client.get_webhook('endpoint-abc')
        mock_get.assert_called_once_with(
            f'{BASE_URL}/webhooks/endpoint-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.patch')
    def test_update_webhook(self, mock_patch, client):
        mock_patch.return_value = mock_response()
        client.update_webhook('endpoint-abc', ['nodeCreated'])
        mock_patch.assert_called_once_with(
            f'{BASE_URL}/webhooks/endpoint-abc',
            auth=client._auth,
            headers=client._headers,
            json={'subscriptions': ['nodeCreated']},
        )

    @patch('tailscale_agent.tailscale_agent.requests.delete')
    def test_delete_webhook(self, mock_delete, client):
        mock_delete.return_value = mock_response()
        client.delete_webhook('endpoint-abc')
        mock_delete.assert_called_once_with(
            f'{BASE_URL}/webhooks/endpoint-abc',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_rotate_webhook_secret(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.rotate_webhook_secret('endpoint-abc')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/webhooks/endpoint-abc/rotate',
            auth=client._auth,
            headers=client._headers,
        )

    @patch('tailscale_agent.tailscale_agent.requests.post')
    def test_test_webhook(self, mock_post, client):
        mock_post.return_value = mock_response()
        client.test_webhook('endpoint-abc')
        mock_post.assert_called_once_with(
            f'{BASE_URL}/webhooks/endpoint-abc/test',
            auth=client._auth,
            headers=client._headers,
        )
