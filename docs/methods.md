# Method Reference

All methods return a [`requests.Response`](https://docs.python-requests.org/en/latest/api/#requests.Response) object. Check `resp.status_code` and call `resp.json()` to inspect the result.

## ACLs / Policy File
| Method | Description |
|--------|-------------|
| `get_acls()` | Get the tailnet ACL |
| `validate_acls(acl_json)` | Validate ACL JSON without applying it |
| `update_acls(acl_json)` | Replace the tailnet ACL |
| `preview_acl_rules(policy_json, acl_type, preview_for)` | Preview which rules apply to a user or IP:port |

## Devices
| Method | Description |
|--------|-------------|
| `get_devices()` | List all devices in the tailnet |
| `get_device(device_id)` | Get details for a specific device |
| `delete_device(device_id)` | Delete a device from the tailnet |
| `authorize_device(device_id)` | Authorize a device |
| `expire_device_key(device_id)` | Expire a device's node key, forcing reauthentication |
| `set_device_name(device_id, name)` | Rename a device |
| `update_device_key(device_id, key_expiry_disabled)` | Enable or disable key expiry for a device |
| `set_device_ipv4(device_id, ipv4)` | Set a device's Tailscale IPv4 address |
| `update_device_tags(device_id, tags)` | Replace the tags on a device |
| `get_device_routes(device_id)` | Get advertised and enabled subnet routes |
| `set_device_routes(device_id, routes)` | Set enabled subnet routes |

## Device Posture Attributes
| Method | Description |
|--------|-------------|
| `get_device_posture_attributes(device_id)` | Get all posture attributes for a device |
| `set_device_posture_attribute(device_id, attribute_key, value, expiry=None, comment=None)` | Create or update a custom posture attribute |
| `delete_device_posture_attribute(device_id, attribute_key)` | Delete a custom posture attribute |
| `batch_update_device_posture_attributes(nodes, comment=None)` | Batch update posture attributes across devices |

## Device Invites
| Method | Description |
|--------|-------------|
| `list_device_invites(device_id)` | List all share invites for a device |
| `create_device_invites(device_id, invites)` | Create new share invites for a device |
| `get_device_invite(device_invite_id)` | Get a specific device invite |
| `delete_device_invite(device_invite_id)` | Delete a device invite |
| `resend_device_invite(device_invite_id)` | Resend a device invite email |
| `accept_device_invite(invite)` | Accept a device share invitation |

## Keys
| Method | Description |
|--------|-------------|
| `get_authorization_keys()` | List auth keys for the tailnet |
| `get_key(key_id)` | Get details for a specific key |
| `create_authorization_key(capabilities, expiry_seconds=None, description=None)` | Create a new auth key |
| `delete_key(key_id)` | Delete an auth key or API access token |
| `update_key(key_id, key_type, scopes, ...)` | Update an OAuth client or federated identity credential |

## DNS
| Method | Description |
|--------|-------------|
| `get_nameservers()` | List global DNS nameservers |
| `set_nameservers(nameservers)` | Replace global DNS nameservers |
| `get_dns_preferences()` | Get DNS preferences (MagicDNS setting) |
| `set_dns_preferences(dns_preferences)` | Set DNS preferences |
| `get_dns_searchpaths()` | Get DNS search paths |
| `set_dns_searchpaths(dns_searchpaths)` | Replace DNS search paths |
| `get_split_dns()` | Get split DNS settings |
| `update_split_dns(split_dns)` | Partially update split DNS settings |
| `set_split_dns(split_dns)` | Replace split DNS settings entirely |
| `get_dns_configuration()` | Get the full DNS configuration |
| `set_dns_configuration(nameservers, split_dns, search_paths, preferences)` | Replace the full DNS configuration in one call |

## Logs
| Method | Description |
|--------|-------------|
| `get_audit_logs(starttime, endtime)` | Get configuration audit logs (ISO-8601 timestamps required) |
| `get_network_logs(starttime, endtime)` | Get network flow logs |
| `get_log_stream_status(log_type)` | Get log streaming status |
| `get_log_stream_config(log_type)` | Get log streaming configuration |
| `set_log_stream_config(log_type, destination_type, url, user=None, token=None)` | Configure log streaming |
| `delete_log_stream_config(log_type)` | Disable log streaming |
| `get_aws_external_id(reusable=None)` | Get an AWS external ID for S3 log streaming |
| `validate_aws_trust_policy(external_id, role_arn)` | Validate an AWS IAM role trust policy |

## Tailnet Settings
| Method | Description |
|--------|-------------|
| `get_tailnet_settings()` | Get tailnet-wide settings |
| `update_tailnet_settings(...)` | Update tailnet settings (device approval, auto-updates, MagicDNS, etc.) |

## Contacts
| Method | Description |
|--------|-------------|
| `get_contacts()` | Get tailnet contact preferences |
| `update_contact(contact_type, email)` | Update the email for a contact (account/support/security) |
| `resend_contact_verification(contact_type)` | Resend verification email for a contact |

## Device Posture Integrations
| Method | Description |
|--------|-------------|
| `list_posture_integrations()` | List all posture integrations |
| `create_posture_integration(provider, client_id, client_secret, ...)` | Create a posture integration (Intune, Jamf, CrowdStrike, etc.) |
| `get_posture_integration(integration_id)` | Get a specific posture integration |
| `update_posture_integration(integration_id, ...)` | Update a posture integration |
| `delete_posture_integration(integration_id)` | Delete a posture integration |

## Users
| Method | Description |
|--------|-------------|
| `get_users()` | List all users in the tailnet |
| `get_user(user_id)` | Get details for a specific user |
| `update_user_role(user_id, role)` | Update a user's role |
| `approve_user(user_id)` | Approve a pending user |
| `suspend_user(user_id)` | Suspend a user |
| `restore_user(user_id)` | Restore a suspended user |
| `delete_user(user_id)` | Delete a user from the tailnet |

## User Invites
| Method | Description |
|--------|-------------|
| `list_user_invites()` | List all open user invites |
| `create_user_invites(invites)` | Create user invites (optionally emailed) |
| `get_user_invite(user_invite_id)` | Get a specific user invite |
| `delete_user_invite(user_invite_id)` | Delete a user invite |
| `resend_user_invite(user_invite_id)` | Resend a user invite email |

## Webhooks
| Method | Description |
|--------|-------------|
| `list_webhooks()` | List all webhook endpoints |
| `create_webhook(endpoint_url, subscriptions, provider_type=None)` | Create a webhook endpoint |
| `get_webhook(endpoint_id)` | Get a specific webhook endpoint |
| `update_webhook(endpoint_id, subscriptions)` | Update webhook subscriptions |
| `delete_webhook(endpoint_id)` | Delete a webhook endpoint |
| `rotate_webhook_secret(endpoint_id)` | Rotate the webhook signing secret |
| `test_webhook(endpoint_id)` | Send a test event to a webhook |

## OAuth
| Method | Description |
|--------|-------------|
| `get_oauth_token(client_id, client_secret, client_embed=True)` | Exchange OAuth credentials for an access token |
