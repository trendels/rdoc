#!/usr/bin/env python
"""
Pandoc filter to highlight bare python builtins.

For example, `` `int` `` is transformed to `` `int`{.python} ``.
"""
from pandocfilters import toJSONFilter, Code

builtins = set(dir(__builtins__))

def highlight_builtins(key, value, format, meta):
    if key == 'Code':
        # For 'Code', the value has the form (attr_list, str),
        # where attr_list is (identifiers, class_list, kv)
        # and kv is a list of (key, value) tuples
        #
        # Source:
        # http://hackage.haskell.org/package/pandoc-types-1.12.4.1/docs/Text-Pandoc-Definition.html#t:Inline
        ((identifier, classes, kv), string) = value
        if string in builtins and not classes:
            return Code((identifier, ['python'], kv), string)

if __name__ == '__main__':
    toJSONFilter(highlight_builtins)
