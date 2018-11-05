try:
    # python 3
    from urllib.parse import (
        urlencode,
        parse_qs,
        urlsplit,
        urlunsplit
    )
except ImportError:
    # python 2
    from urllib import urlencode
    from urlparse import (
        parse_qs,
        urlsplit,
        urlunsplit
    )

try:
    # python 3
    from html import escape
except ImportError:
    # python 2
    from cgi import escape