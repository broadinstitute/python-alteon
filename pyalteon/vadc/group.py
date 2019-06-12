"""Define the pyalteon.vadc.group.Group class."""

from copy import deepcopy
import logging

from pyalteon._endpoint import Endpoint

LOGGER = logging.getLogger(__name__)


class Group(Endpoint):
    """Query the Radware Alteon REST API for group configurations."""

    def __init__(self, client):
        """Initialize the class.

        :param object client: An instantiated pyalteon.Client object
        """
        super(Group, self).__init__(client=client)

        self._reals = None

    @property
    def all(self):
        """Retrieve the groups list."""
        endpoint = "SlbNewCfgEnhGroupTable"
        return self._all(endpoint)

    @property
    def servers(self):
        """Retrieve the real servers that are in the SLB groups."""
        # Return the cached copy if we've already fetched it
        if self._reals:
            return self._reals

        endpoint = "SlbOperEnhGroupRealServerTable"
        data = self._get_endpoint(endpoint)

        # JSON returned has a top-level key that is the name of the endpoint, so return the list under that.
        self._reals = data

        return self._reals

    @property
    def all_combined(self):
        """Combine the groups list and the real server linking data into one dictionary."""
        # Create a deepcopy of all the groups so we can modify the dictionaries in the list
        groups = deepcopy(self.all)
        servers = self.servers

        for group in groups:
            index = group["Index"]
            # Create a new index for the real server info
            group["RealServers"] = []
            for real in servers:
                if real["RealServGroupIndex"] == index:
                    group["RealServers"].append(real)

        return groups
