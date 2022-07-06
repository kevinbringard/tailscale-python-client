import requests

from requests.auth import HTTPBasicAuth

class Tailscale:

    def __init__(self, api_key, base_url, tailnet=None):
        """ Constructor for the Tailscale class
        :param api_key: The API key with which to authenticate against the tailscale API
        :param base_url: The tailscale API url and path to use when making calls from this client
        :param tailnet: The tailnet to perform our operations on from this client

        """

        self._api_key = api_key
        self._base_url = base_url
        self._tailnet = tailnet
        self._auth = HTTPBasicAuth(api_key, '')


    def __repr__(self):

        return(f'Tailscale(self._api_key={self._api_key},'
               f'self._base_url={self._base_url},'
               f'self._tailnet={self._tailnet},'
               f'self._auth={self._auth})')


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


    def get_keys(self):
        """ List the keys for the tailnet defined in the Tailscale client object

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys'
        response = requests.get(url, auth=self._auth)

        return response


    def get_key(self, key_id):
        """ Get a specific key_id for the tailnet defined in the Tailscale client object

        :param key_id: ID of the key to retrieve

        :return: The requests response object

        """

        url = f'{self._base_url}/tailnet/{self._tailnet}/keys/{key_id}'
        response = requests.get(url, auth=self._auth)

        return response


    def get_acls(self):
        """ Get the ACLs for the tailed defined in the Tailscale client object

        :return: The requests response object

        """

        headers = {
            'Accept':'application/json'
        }

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl'
        response = requests.get(url, auth=self._auth, headers=headers)

        return response

    def validate_acls(self, acl_json):
        """ Validate the ACL JSON with the Tailscale API's validator

        :param acl_json: The JSON data to be validated

        :return: The requests response object

        """

        headers = {
            'Accept':'application/json'
        }
        url = f'{self._base_url}/tailnet/{self._tailnet}/acl/validate'

        response = requests.post(url, auth=self._auth, headers=headers, data=acl_json)

        return(response)

    def update_acls(self, acl_json):
        """ Update the Access Controls with the specified JSON.

        It's worth noting the JSON wants to be posted as --data-binary
        so you'll want to pass it in from f.open() and not json.loads()

        :param acl_json: binary representation of the JSON to be passed as binary-data to requests

        :return: The requests response object

        """

        headers = {
            'Accept':'application/json'
        }

        url = f'{self._base_url}/tailnet/{self._tailnet}/acl'

        response = requests.post(url, auth=self._auth, headers=headers, data=acl_json)

        return(response)
