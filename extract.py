#!/usr/bin/env python
"""
Usage: extract.py <module-name> <output-dir>

Extracts documentation from <module-name> to files <module_name>.mkd
and <module_name>.links in <output_dir>.
"""
import importlib
import inspect
import os
import sys
from collections import namedtuple
from StringIO import StringIO

output = namedtuple('output', 'doc toc links module_name')


def format_docstring(out, obj):
    docstring = inspect.getdoc(obj)
    if docstring:
        out.doc.write('<div class="docstring">\n%s\n</div>\n' % docstring)


def format_method(out, fn, name, class_name):
    argspec = inspect.getargspec(fn)
    argspec = argspec._replace(args=argspec.args[1:]) # skip 'self'
    signature = name + inspect.formatargspec(*argspec)
    method_name = '%s.%s' % (class_name, name)
    out.doc.write('\n#### `%(signature)s`{.python} {#%(method_name)s}\n\n'
            % {'signature': signature, 'method_name': method_name})
    out.links.write('%(module_name)s.%(method_name)s'
            '|%(module_name)s.html#%(method_name)s\n'
            % {'module_name': out.module_name, 'method_name': method_name})
    format_docstring(out, fn)


def format_descriptor(out, descriptor, name, class_name):
    descriptor_name = '%s.%s' % (class_name, name)
    out.doc.write('\n#### `%(name)s` {#%(descriptor_name)s}\n\n'
            % {'name': name, 'descriptor_name': descriptor_name})
    out.links.write('%(module_name)s.%(descriptor_name)s'
            '|%(module_name)s.html#%(descriptor_name)s\n'
            % {'module_name': out.module_name,
               'descriptor_name': descriptor_name})
    format_docstring(out, descriptor)


def format_alias(out, alias):
    out.doc.write('Alias for `%s`.\n' % alias)


def format_class_members(out, cls, class_name):
    if inspect.ismethod(cls.__init__):  # False for object.__init__
        format_method(out, cls.__init__, '__init__', class_name)
    for name in dir(cls):
        if name.startswith('_'):
            continue
        attr = getattr(cls, name)
        if name not in cls.__dict__:
            continue
        if not inspect.getdoc(attr):
            continue
        if inspect.ismethod(attr):  # method or classmethod
            format_method(out, attr, name, class_name)
        elif inspect.isfunction(attr):  # staticmethod
            format_method(out, attr, name, class_name)
        elif inspect.isdatadescriptor(attr):  # descriptor, e.g. property
            format_descriptor(out, attr, name, class_name)


def format_module_docs(module_name):
    out = output(
        doc=StringIO(),
        toc=StringIO(),
        links=StringIO(),
        module_name=module_name)

    module = importlib.import_module(module_name)
    out.doc.write('# Module `%(name)s` {#%(name)s}\n'
            % {'name': module_name})
    out.toc.write('  - [Module `%(name)s`](#%(name)s)\n'
            % {'name':  module_name})
    out.links.write('%(name)s|%(name)s.html#%(name)s\n'
            % {'name': module_name})

    format_docstring(out, module)

    if hasattr(module, '__all__'):
        members = module.__all__
    else:
        members = sorted([name for name in dir(module)
                          if not name.startswith('_')])

    classes, functions, exceptions = [], [], []
    for name in members:
        attr = getattr(module, name)
        try:
            is_local = inspect.getmodule(attr) is module
        except TypeError:
            is_local = False
        if name not in getattr(module, '__all__', []):
            if not is_local or not inspect.getdoc(attr):
                continue
        alias = None
        if not is_local:
            try:
                # Only works for (non-C) functions and classes
                other_module = inspect.getmodule(attr)
                alias = other_module.__name__ + '.' + attr.__name__
            except:
                pass
        if inspect.isclass(attr):
            if issubclass(attr, Exception):
                exceptions.append((name, attr, alias))
            else:
                classes.append((name, attr, alias))
        elif inspect.isfunction(attr):
            functions.append((name, attr, alias))

    if classes:
        out.doc.write('\n## Classes\n\n')
        out.toc.write('      - [Classes](#classes)\n')
        for name, cls, alias in classes:
            out.doc.write('\n### `class %(name)s`{.python} {#%(name)s}\n\n'
                    % {'name': name})
            out.toc.write('          - `%(name)s`\n' % {'name': name})
            out.links.write('%(module_name)s.%(name)s'
                    '|%(module_name)s.html#%(name)s\n'
                    % {'module_name': module_name, 'name': name})
            if alias:
                format_alias(out, alias)
            else:
                format_docstring(out, cls)
                format_class_members(out, cls, name)

    if functions:
        out.doc.write('\n## Functions\n\n')
        out.toc.write('      - [Functions](#functions)\n')
        for name, fn, alias in functions:
            signature = name + inspect.formatargspec(*inspect.getargspec(fn))
            out.doc.write('\n### `%(signature)s`{.python} {#%(name)s}\n\n'
                    % {'signature': signature, 'name': name})
            out.toc.write('          - `%(name)s`\n' % {'name': name})
            out.links.write('%(module_name)s.%(name)s'
                    '|%(module_name)s.html#%(name)s\n'
                    % {'module_name': module_name, 'name': name})
            if alias:
                format_alias(out, alias)
            else:
                format_docstring(out, fn)

    if exceptions:
        out.doc.write('\n## Exceptions\n\n')
        out.toc.write('      - [Exceptions](#exceptions)\n')
        for name, cls, alias in exceptions:
            out.doc.write('\n### `class %(name)s`{.python} {#%(name)s}\n\n'
                    % {'name': name})
            out.toc.write('          - `%(name)s`\n' % {'name': name})
            out.links.write('%(module_name)s.%(name)s'
                    '|%(module_name)s.html#%(name)s\n'
                    % {'module_name': module_name, 'name': name})
            if alias:
                format_alias(out, alias)
            else:
                format_docstring(out, cls)

    return out

meta_template = '''\
---
pagetitle: %(module_name)s
module: %(module_name)s
toc: false
...
'''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage = __doc__.strip()
        sys.exit(usage)

    module_name, output_dir = sys.argv[1:]
    mkd_path = os.path.join(output_dir, module_name + '.mkd')
    link_path = os.path.join(output_dir, module_name + '.links')
    out = format_module_docs(module_name)

    with open(mkd_path, 'w') as f:
        f.write(meta_template % {'module_name': module_name})
        f.write('<div id="module-toc">\n' + out.toc.getvalue() + '\n</div>\n')
        f.write('\n')
        f.write(out.doc.getvalue())

    with open(link_path, 'w') as f:
        f.write(out.links.getvalue())
