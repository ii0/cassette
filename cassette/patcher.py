from __future__ import absolute_import

import httplib

from cassette.http_connection import (CassetteHTTPConnection,
                                      CassetteHTTPSConnection)

try:
    import requests
except ImportError:
    pass
else:
    from cassette.http_connection import (UL3CassetteHTTPConnection,
                                          UL3CassetteHTTPSConnection)

try:
    import requests
except ImportError:
    requests = None

unpatched_HTTPConnection = httplib.HTTPConnection
unpatched_HTTPSConnection = httplib.HTTPSConnection

def patch(cassette_library):
    """Replace standard library."""

    # Inspired by vcrpy

    CassetteHTTPConnection._cassette_library = cassette_library
    CassetteHTTPSConnection._cassette_library = cassette_library

    httplib.HTTPConnection = CassetteHTTPConnection
    httplib.HTTP._connection_class = CassetteHTTPConnection
    httplib.HTTPSConnection = CassetteHTTPSConnection
    httplib.HTTPS._connection_class = CassetteHTTPSConnection

    if requests:
        UL3CassetteHTTPConnection._cassette_library = cassette_library
        UL3CassetteHTTPSConnection._cassette_library = cassette_library

        requests.packages.urllib3.connectionpool.HTTPConnectionPool.ConnectionCls = \
            UL3CassetteHTTPConnection
        requests.packages.urllib3.connectionpool.HTTPSConnectionPool.ConnectionCls = \
            UL3CassetteHTTPSConnection

def unpatch():
    """Unpatch standard library."""

    # Inspired by vcrpy

    httplib.HTTPConnection = unpatched_HTTPConnection
    httplib.HTTP._connection_class = unpatched_HTTPConnection
    httplib.HTTPSConnection = unpatched_HTTPSConnection
    httplib.HTTPS._connection_class = unpatched_HTTPSConnection

    if requests:
        requests.packages.urllib3.connection.HTTPConnection = \
            unpatched_HTTPConnection
        requests.packages.urllib3.connection.HTTPSConnection = \
            unpatched_HTTPSConnection