#!/usr/bin/env python
"""
Pandoc filter to insert automatic links to classes, functions and modules.
"""
import os
from functools import partial

from pandocfilters import toJSONFilter, Code, Link

def autolink(key, value, format, meta, links):
    if key == 'Code':
        # For 'Code', the value has the form (attr_list, str),
        # where attr_list is (identifiers, class_list, kv)
        # and kv is a list of (key, value) tuples
        #
        # For 'Link', the value has the form (children, target)
        # where children is the list of (inline) child nodes
        # and target is a (URL, link_title) tuple.
        #
        # Source:
        # http://hackage.haskell.org/package/pandoc-types-1.12.4.1/docs/Text-Pandoc-Definition.html#t:Inline
        (attr_list, string) = value
        href = None
        if string in links:
            href = links[string]
        else:
            module_name = meta['module']['c'][0]['c']
            # TODO allow '.foo', '..foo.bar', etc.
            link_target = module_name + '.' + string
            if link_target in links:
                href = links[link_target]
        if href is not None:
            return Link([Code(attr_list, string)], [href, ''])  # TODO add title

if __name__ == '__main__':
    links_file = os.getenv('LINKS', 'links')
    links = {}
    with open(links_file) as f:
        for line in f:
            name, target = line.strip().split('|', 1)
            links[name] = target
    action = partial(autolink, links=links)
    toJSONFilter(action)