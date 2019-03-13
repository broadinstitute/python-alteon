"""Create a compatibility layer between Python 2 and 3."""
# pylint: disable=unused-import
# pylint: disable=no-name-in-module

import sys

if sys.version_info[0] > 2:
    from urllib.parse import unquote
    from urllib.parse import urlparse
else:
    from urllib import unquote
    from urlparse import urlparse
