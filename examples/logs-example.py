#!/usr/bin/env python

import json
import os
import sys

from tailscale_agent.tailscale_agent import Tailscale

# Base URL for the API. The default should work unless
# you have some special setup
BASE_URL = 'https://api.tailscale.com/api/v2'

# Name of your tailnet, or grab it from the environment
TAILNET = os.getenv('tailscale_tailnet')

# Can be found/generated here: https://login.tailscale.com/admin/settings/keys
# If you're using an OAuth client set this to None.
API_KEY = 'YOUR_API_KEY'

# If you're using an OAuth client, you can set the ID and secret here. Your location may vary.
# You will also need to uncomment the 'client.get_oauth_token' code below.
OAUTH_CLIENT_ID = os.getenv('tailscale_oauth_client_id')
OAUTH_CLIENT_SECRET = os.getenv('tailscale_oauth_client_secret')

client = Tailscale(API_KEY, BASE_URL, TAILNET)
# If you're using an Oauth Client values, then this will cause the client to grab a scoped token
client.get_oauth_token(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET)

# Grab the network-logs via the 'network-logs' endpoint and print them
network_logs = client.get_network_logs("2023-05-12T14:29:00Z", "2023-05-12T14:29:10Z")
print(json.dumps(network_logs.json(), indent=2))

# Grab the audit logs and via the 'logs' endpoint and print them
# Deprecated but left for now for backward compat
# audit_logs = client.get_logs("2023-05-12T16:58:00Z", "2023-05-12T17:00:00Z")
# New preferred way
audit_logs = client.get_audit_logs("2023-05-12T16:58:00Z", "2023-05-12T17:00:00Z")
print(json.dumps(audit_logs.json(), indent=2))