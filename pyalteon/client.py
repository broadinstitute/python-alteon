"""Define the pyalteon.client.Client class."""

import logging
import sys

import requests

from . import __version__
from ._compat import urlparse
from ._helpers import HttpError
from ._helpers import traffic_log

LOGGER = logging.getLogger(__name__)


class Client(object):
    """Make HTTP calls to the Radware Alteon REST API."""

    def __init__(self, base_url, username, password, verify_ssl=True):
        """Initialize the class.

        :param string base_url: The base URL of the Alteon device (protocol, hostname, and port only)
        :param string username: The username with which to login
        :param string password: The password with which to login
        :param bool verify_ssl: Verify the certificate on the Alteon device (default: True)
        """
        self.__base_url = base_url
        self.__username = username
        self.__password = password
        self.__verify_ssl = verify_ssl

        # Create a new Requests Session
        self.__session = requests.Session()

        # Set the default HTTP headers
        self.__headers = {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }
        self.__session.headers.update(self.__headers)

        # Setup the authentication
        self.__authstring = requests.auth.HTTPBasicAuth(self.__username, self.__password)

        # Manually build the base URL to find any errors
        url = urlparse(base_url)
        self.__base_url = url.scheme
        self.__base_url += "://" + url.netloc
        self.__base_url += "/config"

        if url.scheme == "https":
            # If verify_ssl is False, also disable the urllib3 warnings
            if not self.__verify_ssl:
                requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member
        else:
            # If not using https, force SSL verification to False
            self.__verify_ssl = False

    @staticmethod
    def __test_200_error(result):
        """Test for a 200-level error that the Alteon can return sometimes."""
        data = result.json()
        if ("status" in data) and (data["status"] == "err"):
            raise HttpError(result)

    @property
    def base_url(self):
        """Return the internal __base_url value."""
        return self.__base_url

    @property
    def user_agent(self):
        """Return a user-agent string including the module version and Python version."""
        ver_info = list(map(str, sys.version_info))
        pyver = ".".join(ver_info[:3])
        useragent = "pyalteon/%s (Python %s)" % (__version__.__version__, pyver)

        return useragent

    @property
    def headers(self):
        """Return the internal __headers value."""
        return self.__headers

    @property
    def session(self):
        """Return the setup internal __session requests.Session object."""
        return self.__session

    def add_headers(self, headers=None):
        """Add the provided headers to the internally stored headers.

        Note: This function will overwrite an existing header if the key in the headers parameter matches one of the
        keys in the internal dictionary of headers.

        :param dict headers: A dictionary where key is the header with its value being the setting for that header.
        """
        if headers:
            head = self.__headers.copy()
            head.update(headers)
            self.__headers = head
            self.__session.headers.update(self.__headers)

    def remove_headers(self, headers=None):
        """Remove the requested header keys from the internally stored headers.

        Note: If any of the headers in provided the list do not exist, the header will be ignored and will not raise
        an exception.

        :param list headers: A list of header keys to delete
        """
        if headers:
            for head in headers:
                if head in self.__headers:
                    del self.__headers[head]
                    del self.__session.headers[head]

    @traffic_log(traffic_logger=LOGGER)
    def get(self, url, headers=None):
        """Submit a GET request to the provided URL.

        :param str url: A URL to query
        :param dict headers: A dictionary with any extra headers to add to the request
        :return obj: A requests.Response object received as a response
        """
        result = self.__session.get(url, auth=self.__authstring, verify=self.__verify_ssl, headers=headers)
        # Raise an exception if the return code is in an error range
        if result.status_code > 299:
            raise HttpError(result)

        # Test for a 200-level error Alteon can throw
        self.__test_200_error(result)

        return result

    @traffic_log(traffic_logger=LOGGER, method="POST")
    def post(self, url, headers=None, data=None):
        """Submit a POST request to the provided URL and data.

        :param str url: A URL to query
        :param dict headers: A dictionary with any extra headers to add to the request
        :param dict data: A dictionary with the data to use for the body of the POST
        :return obj: A requests.Response object received as a response
        """
        result = self.__session.post(url, auth=self.__authstring, verify=self.__verify_ssl, json=data, headers=headers)

        # Raise an exception if the return code is in an error range
        if result.status_code > 299:
            raise HttpError(result)

        # Test for a 200-level error Alteon can throw
        self.__test_200_error(result)

        return result

    @traffic_log(traffic_logger=LOGGER, method="PUT")
    def put(self, url, headers=None, data=None):
        """Submit a PUT request to the provided URL and data.

        :param str url: A URL to query
        :param dict headers: A dictionary with any extra headers to add to the request
        :param dict data: A dictionary with the data to use for the body of the PUT
        :return obj: A requests.Response object received as a response
        """
        result = self.__session.put(url, auth=self.__authstring, verify=self.__verify_ssl, data=data, headers=headers)

        # Raise an exception if the return code is in an error range
        if result.status_code > 299:
            raise HttpError(result)

        # Test for a 200-level error Alteon can throw
        self.__test_200_error(result)

        return result

    @traffic_log(traffic_logger=LOGGER, method="DELETE")
    def delete(self, url, headers=None):
        """Submit a DELETE request to the provided URL.

        :param str url: A URL to query
        :param dict headers: A dictionary with any extra headers to add to the request
        :return obj: A requests.Response object received as a response
        """
        result = self.__session.delete(url, auth=self.__authstring, verify=self.__verify_ssl, headers=headers)

        # Raise an exception if the return code is in an error range
        if result.status_code > 299:
            raise HttpError(result)

        # Test for a 200-level error Alteon can throw
        self.__test_200_error(result)

        return result
