import requests

from requests.auth import HTTPBasicAuth

class Tailscale:

    def __init__(self, api_key, base_url, tailnet=None, headers=None):
        """ Constructor for the Tailscale class
        :param api_key: The API key with which to authenticate against the tailscale API
        :param base_url: The tailscale API url and path to use when making calls from this client
        :param tailnet: The tailnet to perform our operations on from this client
        :param headers: Optional additional headers to merge into every request

        """

        self._api_key = api_key
        self._base_url = base_url
        self._tailnet = tailnet
        self._auth = HTTPBasicAuth(api_key, '')
        self._headers = {'Accept': 'application/json'}
        if headers:
            self._headers.update(headers)


    def __repr__(self):

        redacted = f'{"*" * 8}{self._api_key[-4:]}' if self._api_key else 'None'
        return(f'Tailscale(self._api_key={redacted},'
               f'self._base_url={self._base_url},'
               f'self._tailnet={self._tailnet},'
               f'self._headers={self._headers})')


    # ---------------------------------------------------------------------------
    # ACL / Policy File methods
    # ---------------------------------------------------------------------------

    def get_acls(self):
        """ Get the ACLs for the tailed defined in the Tailscale client object

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def validate_acls(self, acl_json):
        """ Validate the ACL JSON with the Tailscale API's validator

        :param acl_json: The JSON data to be validated

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl/validate'
        response = requests.post(url, auth=self._auth, headers=self._headers, data=acl_json)

        return(response)


    def update_acls(self, acl_json):
        """ Update the Access Controls with the specified JSON.

            It's worth noting the JSON wants to be posted as --data-binary
            so you'll want to pass it in from f.open() and not json.loads()

        :param acl_json: binary representation of the JSON to be passed as binary-data to requests

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl'
        response = requests.post(url, auth=self._auth, headers=self._headers, data=acl_json)

        return(response)


    def preview_acl_rules(self, policy_json, acl_type, preview_for):
        """ Preview which rules in a policy file apply to a specific resource.

        :param policy_json: The policy file content (binary/HuJSON) to preview
        :param acl_type: The resource type to preview — either 'user' or 'ipport'
        :param preview_for: The resource to preview rules for (user email or IP:port string)

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl/preview?type={acl_type}&previewFor={preview_for}'
        response = requests.post(url, auth=self._auth, headers=self._headers, data=policy_json)

        return response


    # ---------------------------------------------------------------------------
    # Device methods
    # ---------------------------------------------------------------------------

    def get_devices(self):
        """ List the devices for the tailnet defined in the Tailscale client object

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/devices'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def get_device(self, device_id):
        """ Get detailed for a specific device based on device_id

         :param device_id: ID of the device for which you wish to get details

         :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def delete_device(self, device_id):
        """ Delete a device from the tailnet.

        :param device_id: ID of the device to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def authorize_device(self, device_id):
        """
        Take a device ID and authorize the device into the Tailnet
         This is only necessary on Tailnets where device authorization
         is required

         :param device_id: the ID of the device to authorize

         :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/authorized'

        response = requests.post(url, auth=self._auth, headers=self._headers, json={"authorized": True})

        return(response)


    def expire_device_key(self, device_id):
        """ Mark a device's node key as expired, forcing reauthentication.

        :param device_id: ID of the device whose key should be expired

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/expire'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def set_device_name(self, device_id, name):
        """ Set the name of a device.

        :param device_id: ID of the device to rename
        :param name: The new name for the device

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/name'
        response = requests.post(url, auth=self._auth, headers=self._headers, json={'name': name})

        return response


    def update_device_key(self, device_id, key_expiry_disabled):
        """ Update device key expiry settings.

        :param device_id: ID of the device to update
        :param key_expiry_disabled: If True, disables key expiry for the device

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/key'
        response = requests.post(url, auth=self._auth, headers=self._headers,
                                 json={'keyExpiryDisabled': key_expiry_disabled})

        return response


    def set_device_ipv4(self, device_id, ipv4):
        """ Set the Tailscale IPv4 address of a device.

        :param device_id: ID of the device to update
        :param ipv4: The new IPv4 address to assign

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/ip'
        response = requests.post(url, auth=self._auth, headers=self._headers, json={'ipv4': ipv4})

        return response


    def update_device_tags(self, device_id, tags):
        """

         Update the specified device with the specified tags.

         :param device_id: the ID of the device to authorize
         :tags: list of tags to apply to the device
             should be in the correct tag form. For example:
             ["tag:foo", "tag:bar"] or ["tag:load-balancer", "tag:ingress"]

         :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/tags'

        response = requests.post(url, auth=self._auth, headers=self._headers, json={"tags": tags})

        return(response)


    # ---------------------------------------------------------------------------
    # Device Route methods
    # ---------------------------------------------------------------------------

    def get_device_routes(self, device_id):
        """
        Retrieves the list of subnet routes that a device is advertising, as well as those that are enabled for it.
        Enabled routes are not necessarily advertised (e.g. for pre-enabling), and likewise, advertised routes are not necessarily enabled.

        :param device_id: The ID of the device for which you wish to get the routes

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/routes'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def set_device_routes(self, device_id, routes):
        """
        Sets which subnet routes are enabled to be routed by a device by replacing the existing list of subnet routes with the supplied parameters.
        Routes can be enabled without a device advertising them (e.g. for preauth). Returns a list of enabled subnet routes and a list of advertised subnet routes for a device.

        :param device_id: The ID of the device for which you wish to set the routes
        :param routes: The routes you wish to set. This should be a list of addresses in CIDR format. For example: ["10.0.1.0/24", "1.2.0.0/16", "2.0.0.0/24"]

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/routes'
        response = requests.post(url, auth=self._auth, headers=self._headers, json={'routes': routes})

        return response


    # ---------------------------------------------------------------------------
    # Device Posture Attribute methods
    # ---------------------------------------------------------------------------

    def get_device_posture_attributes(self, device_id):
        """ Retrieve all posture attributes for the specified device.

        :param device_id: ID of the device

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/attributes'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def set_device_posture_attribute(self, device_id, attribute_key, value, expiry=None, comment=None):
        """ Create or update a custom posture attribute on a device.

        :param device_id: ID of the device
        :param attribute_key: The attribute key (e.g. 'custom:myAttribute')
        :param value: The attribute value (string, number, or boolean)
        :param expiry: Optional ISO-8601 datetime string after which the attribute is removed
        :param comment: Optional reason for setting the attribute (max 200 chars)

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/attributes/{attribute_key}'
        body = {'value': value}
        if expiry is not None:
            body['expiry'] = expiry
        if comment is not None:
            body['comment'] = comment

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def delete_device_posture_attribute(self, device_id, attribute_key):
        """ Delete a custom posture attribute from a device.

        :param device_id: ID of the device
        :param attribute_key: The attribute key to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/attributes/{attribute_key}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def batch_update_device_posture_attributes(self, nodes, comment=None):
        """ Batch update posture attributes across multiple devices.

        :param nodes: A dict mapping device IDs to their attribute dicts
        :param comment: Optional audit log reason (max 200 chars)

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/device-attributes'
        body = {'nodes': nodes}
        if comment is not None:
            body['comment'] = comment

        response = requests.patch(url, auth=self._auth, headers=self._headers, json=body)

        return response


    # ---------------------------------------------------------------------------
    # Device Invite methods
    # ---------------------------------------------------------------------------

    def list_device_invites(self, device_id):
        """ List all share invites for a device.

        :param device_id: ID of the device

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/device-invites'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def create_device_invites(self, device_id, invites):
        """ Create new share invites for a device.

        :param device_id: ID of the device to share
        :param invites: List of invite dicts. Each may contain:
            - multiUse (bool): allow multiple acceptances
            - allowExitNode (bool): permit exit node usage
            - email (str): email address to send the invite to

        :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}/device-invites'
        response = requests.post(url, auth=self._auth, headers=self._headers, json=invites)

        return response


    def get_device_invite(self, device_invite_id):
        """ Retrieve a specific device invite.

        :param device_invite_id: ID of the device invite

        :return: The requests response object

        """

        url = f'{self._base_url}/device-invites/{device_invite_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def delete_device_invite(self, device_invite_id):
        """ Delete a specific device invite.

        :param device_invite_id: ID of the device invite to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/device-invites/{device_invite_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def resend_device_invite(self, device_invite_id):
        """ Resend a device invite email.

        :param device_invite_id: ID of the device invite to resend

        :return: The requests response object

        """

        url = f'{self._base_url}/device-invites/{device_invite_id}/resend'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def accept_device_invite(self, invite):
        """ Accept an invitation to share a device.

        :param invite: The invite URL or code from the invitation

        :return: The requests response object

        """

        url = f'{self._base_url}/device-invites/-/accept'
        response = requests.post(url, auth=self._auth, headers=self._headers, json={'invite': invite})

        return response


    # ---------------------------------------------------------------------------
    # Key methods
    # ---------------------------------------------------------------------------

    def get_keys(self):
        """ List the keys for the tailnet defined in the Tailscale client object.

        .. deprecated::
            Use :meth:`get_authorization_keys` instead.

        :return: The requests response object

        """
        import warnings
        warnings.warn(
            "get_keys() is deprecated; use get_authorization_keys() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_authorization_keys()


    def get_key(self, key_id):
        """ Get a specific key_id for the tailnet defined in the Tailscale client object

        :param key_id: ID of the key to retrieve

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys/{key_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def get_authorization_keys(self):
        """
        Returns a list of active keys for a tailnet for the user who owns the API key used to perform this query.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return(response)


    def create_authorization_key(self, capabilities, expiry_seconds=None, description=None):
        """
        Create a new key in a tailnet associated with the user who owns the API key used to perform this request.

        Returns a JSON object with the provided capabilities in addition to the generated key.
          The key should be recorded and kept safe and secure as it wields the capabilities specified in the request.
          The identity of the key is embedded in the key itself and can be used to perform operations on the key
          (e.g., revoking it or retrieving information about it).
          The full key can no longer be retrieved by the server so be sure you do something with the response

        :param capabilities: A dict describing the key's capabilities (e.g. ``{"devices": {"create": {...}}}``)
        :param expiry_seconds: Optional lifetime of the key in seconds
        :param description: Optional human-readable description for the key
        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys'

        body = {'capabilities': capabilities}
        if expiry_seconds is not None:
            body['expirySeconds'] = expiry_seconds
        if description is not None:
            body['description'] = description

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def delete_key(self, key_id):
        """ Delete a specific auth key or API access token.

        :param key_id: ID of the key to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys/{key_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def update_key(self, key_id, key_type, scopes, description=None, tags=None,
                   issuer=None, subject=None, audience=None, custom_claim_rules=None):
        """ Set the configuration for an existing OAuth client or federated identity credential.

        :param key_id: ID of the key to update
        :param key_type: Key type — 'client' or 'federated'
        :param scopes: List of scopes to grant
        :param description: Optional human-readable description
        :param tags: Optional list of associated tags
        :param issuer: Optional OIDC issuer URI (federated keys only)
        :param subject: Optional OIDC subject pattern (federated keys only)
        :param audience: Optional OIDC audience claim (federated keys only)
        :param custom_claim_rules: Optional dict of custom OIDC claim patterns (federated keys only)

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys/{key_id}'
        body = {'keyType': key_type, 'scopes': scopes}
        if description is not None:
            body['description'] = description
        if tags is not None:
            body['tags'] = tags
        if issuer is not None:
            body['issuer'] = issuer
        if subject is not None:
            body['subject'] = subject
        if audience is not None:
            body['audience'] = audience
        if custom_claim_rules is not None:
            body['customClaimRules'] = custom_claim_rules

        response = requests.put(url, auth=self._auth, headers=self._headers, json=body)

        return response


    # ---------------------------------------------------------------------------
    # DNS methods
    # ---------------------------------------------------------------------------

    def get_nameservers(self):
        """
         List the DNS nameservers for a tailnet

         Lists the DNS nameservers for a tailnet. Supply the tailnet of interest in the path.

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/nameservers'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return(response)


    def set_nameservers(self, nameservers):
        """
        Replaces the list of DNS nameservers for a tailnet

        Replaces the list of DNS nameservers for the given tailnet with the list supplied by the user.
        Supply the tailnet of interest in the path.
        Note that changing the list of DNS nameservers may also affect the status of MagicDNS (if MagicDNS is on).

        Passing an empty list will remove all nameservers and disable MagicDNS

        :param nameservers: List of nameservers to replace the existing nameservers with

        :return: requests response object

        """

        nameservers_data = {
            "dns": nameservers
        }

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/nameservers'

        response = requests.post(url, auth=self._auth, headers=self._headers, json=nameservers_data)

        return(response)


    def get_dns_preferences(self):
        """
        retrieves the DNS preferences for a tailnet

        Retrieves the DNS preferences that are currently set for the given tailnet.
        Supply the tailnet of interest in the path.

        :return: requests response object
        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/preferences'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return(response)


    def set_dns_preferences(self, dns_preferences):
        """
        Replaces the DNS preferences for a tailnet

        Replaces the DNS preferences for a tailnet, specifically, the MagicDNS setting.
        Note that MagicDNS is dependent on DNS servers.

        If there is at least one DNS server, then MagicDNS can be enabled.
        Otherwise, it returns an error. Note that removing all nameservers will turn off MagicDNS.
        To reenable it, nameservers must be added back, and MagicDNS must be explicitly turned on.

        :param dns_preferences: Boolean setting magic DNS to true or false
        :return: requests response object
        """

        dns_preferences_data = {
            "magicDNS": dns_preferences
        }

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/preferences'

        response = requests.post(url, auth=self._auth, headers=self._headers, json=dns_preferences_data)

        return(response)


    def get_dns_searchpaths(self):
        """
        retrieves the search paths for a tailnet

        Retrieves the list of search paths that is currently set for the given tailnet.
        Supply the tailnet of interest in the path.

        :return: requests response object
        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/searchpaths'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return(response)


    def set_dns_searchpaths(self, dns_searchpaths):
        """
        Replaces the search paths for a tailnet

        Replaces the list of searchpaths with the list supplied by the user and returns an error otherwise.

        :param dns_searchpaths: List of searchpaths to set/replace in the Tailnet
        :return: requests response object
        """

        dns_searchpaths_data = {
            "searchPaths": dns_searchpaths
        }

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/searchpaths'

        response = requests.post(url, auth=self._auth, headers=self._headers, json=dns_searchpaths_data)

        return(response)


    def get_split_dns(self):
        """ Retrieve the split DNS settings for the tailnet.

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/split-dns'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def update_split_dns(self, split_dns):
        """ Partially update split DNS settings (merge with existing config).

        :param split_dns: A dict mapping domain names to lists of nameserver addresses.
            Pass None as a value to clear nameservers for that domain.

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/split-dns'
        response = requests.patch(url, auth=self._auth, headers=self._headers, json=split_dns)

        return response


    def set_split_dns(self, split_dns):
        """ Replace the split DNS settings entirely.

        :param split_dns: A dict mapping domain names to lists of nameserver addresses.
            Pass None as a value to clear nameservers for that domain.

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/split-dns'
        response = requests.put(url, auth=self._auth, headers=self._headers, json=split_dns)

        return response


    def get_dns_configuration(self):
        """ Retrieve the full DNS configuration for the tailnet.

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/configuration'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def set_dns_configuration(self, nameservers=None, split_dns=None, search_paths=None, preferences=None):
        """ Replace the full DNS configuration for the tailnet in a single call.

        :param nameservers: Optional list of global DNS nameserver addresses
        :param split_dns: Optional dict mapping domains to nameserver lists
        :param search_paths: Optional list of DNS search domain strings
        :param preferences: Optional dict with MagicDNS/override settings (e.g. {'magicDNS': True})

        :return: requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/dns/configuration'
        body = {}
        if nameservers is not None:
            body['nameservers'] = nameservers
        if split_dns is not None:
            body['splitDNS'] = split_dns
        if search_paths is not None:
            body['searchPaths'] = search_paths
        if preferences is not None:
            body['preferences'] = preferences

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    # ---------------------------------------------------------------------------
    # Logs methods
    # ---------------------------------------------------------------------------

    def get_audit_logs(self, starttime, endtime):
        """
        Get Audit logs from the logs/ API endpoint.

        You *must* specify a start time and an end time to scope the query, and they
        *must* be in the format "1990-01-01T00:00:00Z" or the API will reject it as
        invalid

        :param starttime: Start time in ISO-8601 format. For example: 1990-01-01T00:00:00Z
        :param endtime: End time in ISO-8601 format. For example: 1991-01-01T00:00:00Z

        :return: requests response object, or None if the date strings are invalid

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/logs?start={starttime}&end={endtime}'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response

    # Create an alias for backward compatibility
    # This will be deprecated at some point in the future
    get_logs = get_audit_logs


    def get_network_logs(self, starttime, endtime):
        """

        Get Network Audit logs from the network-logs/ API endpoint.

        You *must* specify a start time and an end time to scope the query, and they
        *must* be in the format "1990-01-01T00:00:00Z" or the API will reject it as
        invalid

        You must also have network flow logs enabled in the logs section of your tailnet's admin console

        :param starttime: Start time in ISO-8601 format. For example: 1990-01-01T00:00:00Z
        :param endtime: End time in ISO-8601 format. For example: 1991-01-01T00:00:00Z

        :return: requests response object, or None if the date strings are invalid

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/network-logs?start={starttime}&end={endtime}'

        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def get_log_stream_status(self, log_type):
        """ Retrieve the log streaming status for a given log type.

        :param log_type: The log type — either 'configuration' or 'network'

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/logging/{log_type}/stream/status'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def get_log_stream_config(self, log_type):
        """ Retrieve the log streaming configuration for a given log type.

        :param log_type: The log type — either 'configuration' or 'network'

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/logging/{log_type}/stream'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def set_log_stream_config(self, log_type, destination_type, url, user=None, token=None):
        """ Set the log streaming configuration for a given log type.

        :param log_type: The log type — either 'configuration' or 'network'
        :param destination_type: The destination endpoint type (e.g. 'splunk', 'elastic', 'panther', 's3')
        :param url: The destination endpoint URL
        :param user: Optional authentication username
        :param token: Optional authentication token

        :return: The requests response object

        """

        endpoint_url = f'{self._base_url}/tailnet/{self._tailnet}/logging/{log_type}/stream'
        body = {'destinationType': destination_type, 'url': url}
        if user is not None:
            body['user'] = user
        if token is not None:
            body['token'] = token

        response = requests.put(endpoint_url, auth=self._auth, headers=self._headers, json=body)

        return response


    def delete_log_stream_config(self, log_type):
        """ Disable log streaming for a given log type by deleting its configuration.

        :param log_type: The log type — either 'configuration' or 'network'

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/logging/{log_type}/stream'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def get_aws_external_id(self, reusable=None):
        """ Get an AWS external ID for use in S3 log streaming IAM trust policies.

        :param reusable: If True, the same external ID is returned across multiple calls

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/aws-external-id'
        body = {}
        if reusable is not None:
            body['reusable'] = reusable

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def validate_aws_trust_policy(self, external_id, role_arn):
        """ Validate that an AWS IAM role trust policy correctly references the external ID.

        :param external_id: The AWS external ID previously obtained via get_aws_external_id
        :param role_arn: The AWS IAM role ARN to validate

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/aws-external-id/{external_id}/validate-aws-trust-policy'
        response = requests.post(url, auth=self._auth, headers=self._headers, json={'roleArn': role_arn})

        return response


    # ---------------------------------------------------------------------------
    # OAuth token support
    # ---------------------------------------------------------------------------

    def get_oauth_token(self, client_id, client_secret, client_embed=True):
        """
        Use a static oauth client id and secret to generate scoped API tokens

        https://tailscale.com/kb/1215/oauth-clients/

        You can also update the client's self._auth value with the returned token
        by setting client_embed = True

        :param client_id: The OAuth Client ID you generated via the TailScale dashboard
        :param client_secret: The OAuth Client Secret associated with the Client ID above
        :param client_embed: "Should we embed the returned token into the client object
            for subsequent

        :return: requests response object

        """

        oauth_client_data = {
            "client_id": client_id,
            "client_secret": client_secret
        }

        url = f'{self._base_url}/oauth/token'

        response = requests.post(url, headers=self._headers, data=oauth_client_data)

        if not client_embed:
            return response

        try:
            access_token = response.json()['access_token']
            self._api_key = access_token
            self._auth = HTTPBasicAuth(access_token, '')
        except (KeyError, ValueError):
            print('I was not able to set the access token.')
            print('Please ensure you have your OAuth client set '
                  'correctly and it has the necessary permissions.')

        return response


    # ---------------------------------------------------------------------------
    # Tailnet Settings methods
    # ---------------------------------------------------------------------------

    def get_tailnet_settings(self):
        """ Get the settings for the tailnet.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/settings'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def update_tailnet_settings(self, acls_externally_managed_on=None, acls_external_link=None,
                                devices_approval_on=None, devices_auto_updates_on=None,
                                devices_key_duration_days=None, users_approval_on=None,
                                users_role_allowed_to_join_external_tailnets=None,
                                network_flow_logging_on=None, regional_routing_on=None,
                                posture_identity_collection_on=None, https_enabled=None):
        """ Update settings for the tailnet. Only provided fields are changed.

        :param acls_externally_managed_on: If True, ACLs are managed externally
        :param acls_external_link: URL to externally managed ACLs
        :param devices_approval_on: If True, new devices require approval
        :param devices_auto_updates_on: If True, devices auto-update
        :param devices_key_duration_days: Key expiry duration in days
        :param users_approval_on: If True, new users require approval
        :param users_role_allowed_to_join_external_tailnets: Role allowed to join external tailnets
        :param network_flow_logging_on: If True, network flow logging is enabled
        :param regional_routing_on: If True, regional routing is enabled
        :param posture_identity_collection_on: If True, posture identity collection is enabled
        :param https_enabled: If True, HTTPS is enabled for the tailnet

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/settings'
        body = {}
        if acls_externally_managed_on is not None:
            body['aclsExternallyManagedOn'] = acls_externally_managed_on
        if acls_external_link is not None:
            body['aclsExternalLink'] = acls_external_link
        if devices_approval_on is not None:
            body['devicesApprovalOn'] = devices_approval_on
        if devices_auto_updates_on is not None:
            body['devicesAutoUpdatesOn'] = devices_auto_updates_on
        if devices_key_duration_days is not None:
            body['devicesKeyDurationDays'] = devices_key_duration_days
        if users_approval_on is not None:
            body['usersApprovalOn'] = users_approval_on
        if users_role_allowed_to_join_external_tailnets is not None:
            body['usersRoleAllowedToJoinExternalTailnets'] = users_role_allowed_to_join_external_tailnets
        if network_flow_logging_on is not None:
            body['networkFlowLoggingOn'] = network_flow_logging_on
        if regional_routing_on is not None:
            body['regionalRoutingOn'] = regional_routing_on
        if posture_identity_collection_on is not None:
            body['postureIdentityCollectionOn'] = posture_identity_collection_on
        if https_enabled is not None:
            body['httpsEnabled'] = https_enabled

        response = requests.patch(url, auth=self._auth, headers=self._headers, json=body)

        return response


    # ---------------------------------------------------------------------------
    # Contacts methods
    # ---------------------------------------------------------------------------

    def get_contacts(self):
        """ Get contact preferences for the tailnet.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/contacts'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def update_contact(self, contact_type, email):
        """ Update the email address for a specific contact type.

        :param contact_type: The contact type — one of 'account', 'support', or 'security'
        :param email: The new email address for this contact

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/contacts/{contact_type}'
        response = requests.patch(url, auth=self._auth, headers=self._headers, json={'email': email})

        return response


    def resend_contact_verification(self, contact_type):
        """ Resend the verification email for a contact.

        :param contact_type: The contact type — one of 'account', 'support', or 'security'

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/contacts/{contact_type}/resend-verification-email'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    # ---------------------------------------------------------------------------
    # Device Posture Integration methods
    # ---------------------------------------------------------------------------

    def list_posture_integrations(self):
        """ List all device posture integrations for the tailnet.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/posture/integrations'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def create_posture_integration(self, provider, client_id, client_secret,
                                   cloud_id=None, tenant_id=None):
        """ Create a new device posture integration.

        :param provider: The posture provider (e.g. 'falcon', 'intune', 'jamfpro', 'kandji', 'kolide', 'sentinelone', 'workspace_one')
        :param client_id: OAuth client ID for the provider
        :param client_secret: OAuth client secret for the provider
        :param cloud_id: Optional cloud ID (required for some providers, e.g. CrowdStrike)
        :param tenant_id: Optional tenant ID (required for some providers, e.g. Intune)

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/posture/integrations'
        body = {'provider': provider, 'clientId': client_id, 'clientSecret': client_secret}
        if cloud_id is not None:
            body['cloudId'] = cloud_id
        if tenant_id is not None:
            body['tenantId'] = tenant_id

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def get_posture_integration(self, integration_id):
        """ Get a specific device posture integration.

        :param integration_id: ID of the posture integration

        :return: The requests response object

        """

        url = f'{self._base_url}/posture/integrations/{integration_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def update_posture_integration(self, integration_id, client_secret=None, cloud_id=None,
                                   client_id=None, tenant_id=None):
        """ Update a device posture integration.

        :param integration_id: ID of the posture integration to update
        :param client_secret: Optional new client secret
        :param cloud_id: Optional new cloud ID
        :param client_id: Optional new client ID
        :param tenant_id: Optional new tenant ID

        :return: The requests response object

        """

        url = f'{self._base_url}/posture/integrations/{integration_id}'
        body = {}
        if client_secret is not None:
            body['clientSecret'] = client_secret
        if cloud_id is not None:
            body['cloudId'] = cloud_id
        if client_id is not None:
            body['clientId'] = client_id
        if tenant_id is not None:
            body['tenantId'] = tenant_id

        response = requests.patch(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def delete_posture_integration(self, integration_id):
        """ Delete a device posture integration.

        :param integration_id: ID of the posture integration to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/posture/integrations/{integration_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    # ---------------------------------------------------------------------------
    # User methods
    # ---------------------------------------------------------------------------

    def get_users(self):
        """ Get a list of all users of a tailnet

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/users'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response

    def get_user(self, user_id):
        """ Get details about the specified user

         :param user_id: ID of the user for which you wish to get details

         :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response

    def update_user_role(self, user_id, role):
        """

         Update the specified user with the specified role.

         :param user_id: the ID of the user for which you wish to update the role
         :param role: The name of the role
             should be in string format and be one of "owner", "member", "admin", "it-admin", "network-admin", "billing-admin", or "auditor".
             For example: "owner"

         :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}/role'

        response = requests.post(url, auth=self._auth, headers=self._headers, json={"role": role})

        return response


    def approve_user(self, user_id):
        """ Approve a pending user, allowing them to join the tailnet.

        :param user_id: ID of the user to approve

        :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}/approve'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def suspend_user(self, user_id):
        """ Suspend a user, preventing them from accessing the tailnet.

        :param user_id: ID of the user to suspend

        :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}/suspend'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def restore_user(self, user_id):
        """ Restore a previously suspended user.

        :param user_id: ID of the user to restore

        :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}/restore'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def delete_user(self, user_id):
        """ Delete a user from the tailnet.

        :param user_id: ID of the user to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/users/{user_id}/delete'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    # ---------------------------------------------------------------------------
    # User Invite methods
    # ---------------------------------------------------------------------------

    def list_user_invites(self):
        """ List all open (not yet accepted) user invites to the tailnet.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/user-invites'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def create_user_invites(self, invites):
        """ Create, and optionally email out, new user invites.

        :param invites: List of invite dicts. Each may contain:
            - role (str): one of 'member', 'admin', 'it-admin', 'network-admin', 'billing-admin', 'auditor' (default: 'member')
            - email (str): email address to send the invite to

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/user-invites'
        response = requests.post(url, auth=self._auth, headers=self._headers, json=invites)

        return response


    def get_user_invite(self, user_invite_id):
        """ Retrieve a specific user invite.

        :param user_invite_id: ID of the user invite

        :return: The requests response object

        """

        url = f'{self._base_url}/user-invites/{user_invite_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def delete_user_invite(self, user_invite_id):
        """ Delete a specific user invite.

        :param user_invite_id: ID of the user invite to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/user-invites/{user_invite_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def resend_user_invite(self, user_invite_id):
        """ Resend a user invite email.

        :param user_invite_id: ID of the user invite to resend

        :return: The requests response object

        """

        url = f'{self._base_url}/user-invites/{user_invite_id}/resend'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    # ---------------------------------------------------------------------------
    # Webhook methods
    # ---------------------------------------------------------------------------

    def list_webhooks(self):
        """ List all webhooks configured for the tailnet.

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/webhooks'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def create_webhook(self, endpoint_url, subscriptions, provider_type=None):
        """ Create a new webhook endpoint.

        :param endpoint_url: The URL to deliver webhook events to
        :param subscriptions: List of event types to subscribe to
        :param provider_type: Optional provider type for pre-configured integrations (e.g. 'slack', 'mattermost')

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/webhooks'
        body = {'endpointUrl': endpoint_url, 'subscriptions': subscriptions}
        if provider_type is not None:
            body['providerType'] = provider_type

        response = requests.post(url, auth=self._auth, headers=self._headers, json=body)

        return response


    def get_webhook(self, endpoint_id):
        """ Get a specific webhook endpoint.

        :param endpoint_id: ID of the webhook endpoint

        :return: The requests response object

        """

        url = f'{self._base_url}/webhooks/{endpoint_id}'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


    def update_webhook(self, endpoint_id, subscriptions):
        """ Update the subscriptions for a webhook endpoint.

        :param endpoint_id: ID of the webhook endpoint to update
        :param subscriptions: New list of event types to subscribe to

        :return: The requests response object

        """

        url = f'{self._base_url}/webhooks/{endpoint_id}'
        response = requests.patch(url, auth=self._auth, headers=self._headers,
                                  json={'subscriptions': subscriptions})

        return response


    def delete_webhook(self, endpoint_id):
        """ Delete a webhook endpoint.

        :param endpoint_id: ID of the webhook endpoint to delete

        :return: The requests response object

        """

        url = f'{self._base_url}/webhooks/{endpoint_id}'
        response = requests.delete(url, auth=self._auth, headers=self._headers)

        return response


    def rotate_webhook_secret(self, endpoint_id):
        """ Rotate the secret for a webhook endpoint.

        :param endpoint_id: ID of the webhook endpoint

        :return: The requests response object

        """

        url = f'{self._base_url}/webhooks/{endpoint_id}/rotate'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response


    def test_webhook(self, endpoint_id):
        """ Send a test event to a webhook endpoint.

        :param endpoint_id: ID of the webhook endpoint to test

        :return: The requests response object

        """

        url = f'{self._base_url}/webhooks/{endpoint_id}/test'
        response = requests.post(url, auth=self._auth, headers=self._headers)

        return response
