#!/usr/bin/env python
"""
Pandoc filter to insert automatic links to classes, functions and modules.
"""
import os.path

from pandocfilters import toJSONFilter, Code, Link, Str

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
        if '|' in string:
            target, text = string.split('|', 1)
        else:
            target, text = string, None
        if target in links:
            href = 'modules/' + links[string]['c'][0]['c']
        elif 'module' in meta:
            module_name = meta['module']['c'][0]['c']
            # TODO allow '.foo', '..foo.bar', etc.
            target = module_name + '.' + target
            if target in links:
                href = 'modules/' + links[target]['c'][0]['c']
        if href is not None:
            if 'link_prefix' in meta:
                link_prefix = meta['link_prefix']['c']
                href = link_prefix + href
            if text is None:
                link = Code(attr_list, target)
            else:
                link = Str(text)
            return Link([link], [href, ''])  # TODO add title

if __name__ == '__main__':
    toJSONFilter(autolink)
