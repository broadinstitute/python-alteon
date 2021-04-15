# -*- coding: utf-8 -*-
"""Define the pyalteon._endpoint.Endpoint base class."""

import logging

LOGGER = logging.getLogger(__name__)


class Endpoint(object):  # pylint: disable=too-few-public-methods
    """Act as a superclass for all Radware Alteon REST API endpoints."""

    def __init__(self, client):
        """Initialize the class.

        :param object client: An instantiated cert_manager.Client object
        """
        self._client = client
        self.__all = None

    def _url(self, suffix):
        """Build the endpoint URL based on the API URL inside this object.

        :param str suffix: The suffix of the URL you wish to create
        :return str: The full URL
        """
        url = self._client.base_url
        url += "/" + suffix.strip("/")
        LOGGER.debug("URL created: %s", url)

        return url

    def _all(self, endpoint):
        """Retrieve all data from a given endpoint, return it as a dictionary, and internal __all."""
        # Return the cached copy if we've already fetched it
        if self.__all:
            return self.__all

        self.__all = self._get_endpoint(endpoint)

        return self.__all

    def _get_endpoint(self, endpoint):
        """Retrieve all data from a given endpoint and return it as a dictionary."""
        url = self._url(endpoint)
        data = self._client.get(url).json()

        # JSON returned has a top-level key that is the name of the endpoint, so return the list under that.
        return data[endpoint]
