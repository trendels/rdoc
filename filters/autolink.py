#!/usr/bin/env python
"""
Pandoc filter to insert automatic links to classes, functions and modules.
"""
import os.path

from pandocfilters import toJSONFilter, Code, Link

# FIXME don't hardcode path 'modules/' in autolink()

def autolink(key, value, format, meta):
    links = meta['links']['c']
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
            href = 'modules/' + links[string]['c'][0]['c']
        elif 'module' in meta:
            module_name = meta['module']['c'][0]['c']
            # TODO allow '.foo', '..foo.bar', etc.
            link_target = module_name + '.' + string
            if link_target in links:
                href = 'modules/' + links[link_target]['c'][0]['c']
        if href is not None:
            if 'link_prefix' in meta:
                link_prefix = meta['link_prefix']['c']
                if '#' in href:
                    path, anchor = href.split('#', 1)
                else:
                    path, anchor = href, None
                href = link_prefix + path
                if anchor:
                    href += '#' + anchor
            return Link([Code(attr_list, string)], [href, ''])  # TODO add title

if __name__ == '__main__':
    toJSONFilter(autolink)
