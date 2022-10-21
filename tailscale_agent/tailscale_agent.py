import requests

from requests.auth import HTTPBasicAuth

class Tailscale:

    def __init__(self, api_key, base_url, tailnet=None, headers=None):
        """ Constructor for the Tailscale class
        :param api_key: The API key with which to authenticate against the tailscale API
        :param base_url: The tailscale API url and path to use when making calls from this client
        :param tailnet: The tailnet to perform our operations on from this client

        """

        self._api_key = api_key
        self._base_url = base_url
        self._tailnet = tailnet
        self._auth = HTTPBasicAuth(api_key, '')
        self._headers = {
            'Accept':'application/json'
        }


    def __repr__(self):

        return(f'Tailscale(self._api_key={self._api_key},'
               f'self._base_url={self._base_url},'
               f'self._tailnet={self._tailnet},'
               f'self._auth={self._auth}),'
               f'self._headers={self._headers}')


    # ACL related methods
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

    # Device related methods
    def get_devices(self):
        """ List the devices for the tailnet defined in the Tailscale client object

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/devices'
        response = requests.get(url, auth=self._auth)

        return response


    def get_device(self, device_id):
        """ Get detailed for a specific device based on device_id

         :param device_id: ID of the device for which you wish to get details

         :return: The requests response object

        """

        url = f'{self._base_url}/device/{device_id}'
        response = requests.get(url, auth=self._auth)

        return response

    def authorize_device(self, device_id):
        """
        Take a device ID and authorize the device into the Tailnet
         This is only necessary on Tailnets where device authorization
         is required

         :param device_id: the ID of the device to authorize

         :return: The requests response object

        """

        authorized_data = {
            "authorized": true
        }

        url = f'{self._base_url}/device/{device_id}/authorized'

        response = requests.post(url, auth=self._auth, headers=self._headers, data=authorized_data)

        return(response)

    def update_device_tags(self, device_id, tags):
        """

         Update the specified device with the specified tags.

         :param device_id: the ID of the device to authorize
         :tags: list of tags to apply to the device
             should be in the correct tag form. For example:
             ["tag:foo", "tag:bar"] or ["tag:load-balancer", "tag:ingress"]

         :return: The requests response object

        """

        tags_data = {
            "tags": tags
        }

        url = f'{self._base_url}/device/{device_id}/tags'

        response = requests.post(url, auth=self._auth, headers=self._headers, data=tags_data)

        return(response)

    # Device Route methods
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

        routes_data = {
            'routes': routes
        }

        url = f'{self._base_url}/device/{device_id}/routes'
        response = requests.post(url, auth=self._auth, headers=self._headers, data=routes_data)

        return response


    # Tailnet related methods
    def get_keys(self):
        """ List the keys for the tailnet defined in the Tailscale client object

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys'
        response = requests.get(url, auth=self._auth, headers=self._headers)

        return response


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


    def create_authorization_key(self):
        """
        Create a new key in a tailnet associated with the user who owns the API key used to perform this request.

        Returns a JSON object with the provided capabilities in addition to the generated key.
          The key should be recorded and kept safe and secure as it wields the capabilities specified in the request.
          The identity of the key is embedded in the key itself and can be used to perform operations on the key
          (e.g., revoking it or retrieving information about it).
          The full key can no longer be retrieved by the server so be sure you do something with the response

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys'

        response = requests.post(url, auth=self._auth, headers=self._headers, data=tags_data)

        return(response)


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

        response = requests.post(url, auth=self._auth, headers=self._headers, data=nameservers_data)

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

        response = requests.post(url, auth=self._auth, headers=self._headers, data=dns_preferences_data)

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

        response = requests.get(url, auth=self._auth, headers=self._headers, data=dns_searchpaths_data)

        return(response)

    # Logs related methods
    def get_logs(self, starttime, endtime):
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
