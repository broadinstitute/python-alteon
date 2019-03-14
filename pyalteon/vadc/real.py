"""Define the pyalteon.vadc.real.Real class."""

import logging

from pyalteon._endpoint import Endpoint

LOGGER = logging.getLogger(__name__)


class Real(Endpoint):
    """Query the Radware Alteon REST API for real server configuration."""

    def __init__(self, client):
        """Initialize the class.

        :param object client: An instantiated pyalteon.Client object
        """
        super(Real, self).__init__(client=client)

        self._combined = None

    @property
    def all(self):
        """Retrieve the real servers list."""
        endpoint = "SlbNewCfgEnhRealServerTable"
        return self._all(endpoint)

    @property
    def combined(self):
        """Retrieve the real servers configuration from multiple endpoints and merge into one dictionary."""
        # Return the cached copy if we've already fetched it
        if self._combined:
            return self._combined

        endpoint_list = [
            "SlbNewCfgEnhRealServerTable",
            "SlbNewCfgEnhRealServerSecondPartTable",
            "SlbNewCfgEnhRealServerThirdPartTable",
        ]

        ret = {}
        for endp in endpoint_list:
            data = self._get_endpoint(endp)

            # Cycle through and merge the dictionaries together
            for srv in data:
                index = srv["Index"]
                if index not in ret:
                    ret[index] = srv
                else:
                    ret[index].update(srv)

        self._combined = ret

        return self._combined
