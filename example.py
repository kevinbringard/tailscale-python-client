#!/usr/bin/env python

# This example will take in a file with your ACLs
# and validate it against the TailScale API's validator
# If it passes the vaidation (receives a 200 response)
# then it will update the ACLs with what is in the file.
# If that that succeeds it will pretty dump the new ACLs
# as returned by the TS API.
#
# It is worth noting this does a complete update and
# not a diff. What you have in your ACL file should be the
# entire ACL blob as you want it to exist then the operation
# is complete

import json
import os

from tailscale_agent.tailscale import Tailscale

# Base URL for the API. The default should work unless
# you have some special setup
BASE_URL = 'https://api.tailscale.com/api/v2'

# Can be found/generated here: https://login.tailscale.com/admin/settings/keys
API_KEY = 'YOUR_API_KEY'

# The name of the tailnet upon which you wish to operate.
# Can be found in the upper left hand corner of your TailScale dashboard
# If you signed up with a gmail account, for example, it will likely be
# your full gmail address
TAILNET = 'YOUR_TAILNET_NAME'

# JSON file with the ACLs you wish to validate/update
ACL_JSON_FILE = os.path.abspath("./test.json")

# Create the tailscale client using the values from above
client = Tailscale(API_KEY, BASE_URL, TAILNET)

# Open the ACL_JSON_FILE defined above
with open(ACL_JSON_FILE) as f:
    acl_json = f.read()

# Validate the JSON with the TS API
print('Validating ACL JSON...')
validation = client.validate_acls(acl_json)

# If it validates then go on to updating it
if validation.status_code == 200:
    print('JSON validated, updating ACLs...')
    update = client.update_acls(acl_json)

    # If the update succeeded then huzza!
    # Print the response JSON (which should be the new ACLs)
    if update.status_code == 200:
        print('ACLs updated!')
        print(json.dumps(update.json(), indent=2))
