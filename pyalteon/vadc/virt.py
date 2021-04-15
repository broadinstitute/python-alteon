# -*- coding: utf-8 -*-
"""Define the pyalteon.vadc.virt.Virt class."""

import logging

from pyalteon._endpoint import Endpoint

LOGGER = logging.getLogger(__name__)


class Virt(Endpoint):
    """Query the Radware Alteon REST API for virtual service configuration."""

    def __init__(self, client):
        """Initialize the class.

        :param object client: An instantiated pyalteon.Client object
        """
        super().__init__(client=client)

        self._combined = None

    @staticmethod
    def index_name(index):
        """Build an index name based on the index passed."""
        # This API is gross!!
        index_names = ["", "SecondPart", "ThirdPart", "FourthPart", "FifthPart", "SixthPart", "SeventhPart"]
        idx = "%sIndex" % index_names[index]

        return idx

    @property
    def all(self):
        """Retrieve the virtual servers list."""
        endpoint = "SlbNewCfgEnhVirtServerTable"
        return self._all(endpoint)

    @property
    def combined(self):
        """Retrieve the virtual services configuration from multiple endpoints and merge into one dictionary."""
        if self._combined:
            return self._combined

        # See what I mean...
        endpoint_list = [
            "SlbNewCfgEnhVirtServicesTable",
            "SlbNewCfgEnhVirtServicesSecondPartTable",
            "SlbNewCfgEnhVirtServicesThirdPartTable",
            "SlbNewCfgEnhVirtServicesFourthPartTable",
            "SlbNewCfgEnhVirtServicesFifthPartTable",
            "SlbNewCfgEnhVirtServicesSixthPartTable",
            "SlbNewCfgEnhVirtServicesSeventhPartTable",
        ]

        ret = {}
        i = 0
        for endp in endpoint_list:
            idx = "Serv" + self.index_name(i)
            data = self._get_endpoint(endp)

            # Cycle through and merge the dictionaries together
            for srv in data:
                index = srv[idx]
                if index not in ret:
                    ret[index] = {}
                if i not in ret[index]:
                    ret[index][i] = []

                ret[index][i].append(srv)

            i = i + 1

        self._combined = ret

        return self._combined
