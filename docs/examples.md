# Examples

Practical recipes for common tasks. All examples assume:

```python
from tailscale_agent.tailscale_agent import Tailscale
import os

client = Tailscale(
    api_key=os.environ['TAILSCALE_API_KEY'],
    base_url='https://api.tailscale.com/api/v2',
    tailnet=os.environ['TAILSCALE_TAILNET'],
)
```

To use OAuth instead of an API key, see [OAuth authentication](#oauth-authentication) below.

---

## OAuth authentication

```python
client = Tailscale(
    api_key='',  # replaced after token exchange
    base_url='https://api.tailscale.com/api/v2',
    tailnet=os.environ['TAILSCALE_TAILNET'],
)
client.get_oauth_token(
    client_id=os.environ['TAILSCALE_OAUTH_CLIENT_ID'],
    client_secret=os.environ['TAILSCALE_OAUTH_CLIENT_SECRET'],
)
# client is now authenticated for subsequent calls
```

---

## Devices

### List all devices

```python
resp = client.get_devices()
for device in resp.json()['devices']:
    print(device['hostname'], device['addresses'])
```

### Authorize a new device

```python
resp = client.authorize_device('123456789')
print(resp.status_code)  # 200 on success
```

### Tag devices for ACL matching

```python
client.update_device_tags('123456789', ['tag:server', 'tag:production'])
```

### Expire a device key (force reauthentication)

```python
client.expire_device_key('123456789')
```

### Disable key expiry for a device

```python
client.update_device_key('123456789', key_expiry_disabled=True)
```

### Enable subnet routes for a device

```python
client.set_device_routes('123456789', ['10.0.0.0/24', '192.168.1.0/24'])
```

### Remove a device from the tailnet

```python
resp = client.delete_device('123456789')
print(resp.status_code)  # 200 on success
```

---

## Device posture attributes

### Check compliance status across devices

```python
# Set a custom compliance attribute on a device
client.set_device_posture_attribute(
    device_id='123456789',
    attribute_key='custom:compliant',
    value=True,
    comment='Passed quarterly audit',
)

# Batch update multiple devices at once
client.batch_update_device_posture_attributes(
    nodes={
        '123456789': {'custom:compliant': True},
        '987654321': {'custom:compliant': False},
    },
    comment='Q1 2026 audit run',
)
```

---

## Device invites (sharing)

### Share a device with an external user

```python
resp = client.create_device_invites('123456789', [
    {'email': 'contractor@external.com', 'allowExitNode': False},
])
invite = resp.json()[0]
print('Invite URL:', invite['inviteUrl'])
```

### List and clean up old invites

```python
invites = client.list_device_invites('123456789').json()
for invite in invites:
    if invite['accepted']:
        client.delete_device_invite(invite['id'])
```

---

## Auth keys

### Create a reusable, preauthorized auth key

```python
resp = client.create_authorization_key(
    capabilities={
        'devices': {
            'create': {
                'reusable': True,
                'ephemeral': False,
                'preauthorized': True,
                'tags': ['tag:ci'],
            }
        }
    },
    expiry_seconds=86400,
    description='CI pipeline key',
)
key = resp.json()
print('Key:', key['key'])  # save this — it cannot be retrieved again
```

### List and delete expired keys

```python
keys = client.get_authorization_keys().json()['keys']
for k in keys:
    if k.get('expires') and k['expires'] < '2026-01-01T00:00:00Z':
        client.delete_key(k['id'])
```

---

## DNS

### Enable MagicDNS with custom nameservers

```python
client.set_nameservers(['1.1.1.1', '8.8.8.8'])
client.set_dns_preferences(True)  # enable MagicDNS
```

### Configure split DNS for an internal domain

```python
# Route corp.example.com queries to an internal resolver
client.update_split_dns({'corp.example.com': ['10.0.0.53']})
```

### Replace the entire DNS configuration in one call

```python
client.set_dns_configuration(
    nameservers=['1.1.1.1'],
    split_dns={'corp.example.com': ['10.0.0.53']},
    search_paths=['corp.example.com'],
    preferences={'magicDNS': True},
)
```

---

## ACLs

### Validate and deploy an ACL file

```python
with open('acl.hujson', 'rb') as f:
    acl = f.read()

validation = client.validate_acls(acl)
if validation.status_code == 200:
    client.update_acls(acl)
    print('ACL deployed')
else:
    print('Validation failed:', validation.json())
```

### Preview which rules apply to a user

```python
with open('acl.hujson', 'rb') as f:
    acl = f.read()

resp = client.preview_acl_rules(acl, acl_type='user', preview_for='alice@example.com')
print(resp.json())
```

---

## Tailnet settings

### Require device and user approval

```python
client.update_tailnet_settings(
    devices_approval_on=True,
    users_approval_on=True,
)
```

### Enable HTTPS and network flow logging

```python
client.update_tailnet_settings(
    https_enabled=True,
    network_flow_logging_on=True,
)
```

---

## Contacts

### Update security contact

```python
client.update_contact('security', 'security-team@example.com')
```

### Get all contacts

```python
contacts = client.get_contacts().json()
for contact_type, info in contacts.items():
    print(contact_type, info.get('email'), info.get('verified'))
```

---

## Users

### List and approve pending users

```python
users = client.get_users().json()['users']
pending = [u for u in users if u['status'] == 'pending']
for user in pending:
    client.approve_user(user['id'])
    print('Approved:', user['loginName'])
```

### Invite new users to the tailnet

```python
client.create_user_invites([
    {'role': 'member', 'email': 'newuser@example.com'},
    {'role': 'admin', 'email': 'newadmin@example.com'},
])
```

### Suspend and restore a user

```python
client.suspend_user('user-123')
# later...
client.restore_user('user-123')
```

---

## Webhooks

### Create a webhook for node events

```python
resp = client.create_webhook(
    endpoint_url='https://hooks.example.com/tailscale',
    subscriptions=['nodeCreated', 'nodeDeleted', 'nodeApproved'],
)
endpoint = resp.json()
print('Endpoint ID:', endpoint['endpointId'])
print('Secret:', endpoint['secret'])  # save this for signature verification
```

### Create a Slack-integrated webhook

```python
client.create_webhook(
    endpoint_url='https://hooks.slack.com/services/...',
    subscriptions=['nodeCreated', 'userApproved'],
    provider_type='slack',
)
```

### Rotate a webhook secret

```python
resp = client.rotate_webhook_secret('endpoint-abc')
print('New secret:', resp.json()['secret'])
```

---

## Log streaming

### Stream configuration logs to Splunk

```python
client.set_log_stream_config(
    log_type='configuration',
    destination_type='splunk',
    url='https://splunk.example.com:8088/services/collector',
    token='splunk-hec-token',
)
```

### Check streaming status

```python
status = client.get_log_stream_status('configuration').json()
print(status)
```

### Stream to S3 via AWS role

```python
# Step 1: get an external ID to put in your IAM trust policy
ext_id_resp = client.get_aws_external_id(reusable=True)
external_id = ext_id_resp.json()['externalId']
print('Add this to your IAM trust policy as the external ID:', external_id)

# Step 2: after updating the IAM role, validate the trust policy
client.validate_aws_trust_policy(external_id, 'arn:aws:iam::123456789012:role/TailscaleLogs')
```

---

## Device posture integrations

### Connect CrowdStrike Falcon

```python
client.create_posture_integration(
    provider='falcon',
    client_id=os.environ['CROWDSTRIKE_CLIENT_ID'],
    client_secret=os.environ['CROWDSTRIKE_CLIENT_SECRET'],
    cloud_id='us-2',
)
```

### Connect Microsoft Intune

```python
client.create_posture_integration(
    provider='intune',
    client_id=os.environ['INTUNE_CLIENT_ID'],
    client_secret=os.environ['INTUNE_CLIENT_SECRET'],
    tenant_id=os.environ['INTUNE_TENANT_ID'],
)
```
