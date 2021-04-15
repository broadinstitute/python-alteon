# -*- coding: utf-8 -*-
"""Define the pyalteon.vx.vadc.VADC class."""

import logging

from pyalteon._endpoint import Endpoint

LOGGER = logging.getLogger(__name__)


class VADC(Endpoint):
    """Query the Radware Alteon REST API of a hardware appliance for vADC configurations."""

    def __init__(self, client):
        """Initialize the class.

        :param object client: An instantiated pyalteon.Client object
        """
        super().__init__(client=client)

        self._network = None
        self._system = None
        self._users = None

    @property
    def all(self):
        """Retrieve the list of all vADCs on the VX device."""
        endpoint = "VADCNewCfgTable"
        return self._all(endpoint)

    @property
    def system(self):
        """Retrieve the system configurations for all vADCs."""
        # Return the cached copy if we've already fetched it
        if self._system:
            return self._system

        endpoint = "VADCNewCfgSysTable"
        self._system = self._get_endpoint(endpoint)

        return self._system

    @property
    def network(self):
        """Retrieve the network configurations for all vADCs."""
        # Return the cached copy if we've already fetched it
        if self._network:
            return self._network

        endpoint = "VADCNewCfgNetTable"
        self._network = self._get_endpoint(endpoint)

        return self._network

    @property
    def users(self):
        """Retrieve the network configurations for all vADCs."""
        # Return the cached copy if we've already fetched it
        if self._users:
            return self._users

        endpoint = "VADCUsersPswdTable"
        self._users = self._get_endpoint(endpoint)

        return self._users
