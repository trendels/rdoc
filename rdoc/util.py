from __future__ import absolute_import

import textwrap

def usage(fn):
    return textwrap.dedent(fn.__doc__).strip()

