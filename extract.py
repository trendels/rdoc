"""
Usage: convert.py <module-name> <output-dir>

Prints documentation from in `module-name` to stdout using pandoc's markdown.
"""
import importlib
import inspect
import os
import sys
from StringIO import StringIO

# TODO
#   - Drop the custom json format, just inspect the modules again.
#   - We don't even need to resolve references here. It's all done by the
#     pandoc filter (TBD). The only place we need refs is imported members
#     that are also in `__all__`. For these, just drop the complete name
#     in `````s, and let the filter resolve them later.
#   - Structure: write to 2 stringIO instances, one for the ToC and one for
#     the docs. We can add another one for the index later.
#   - Document module and class variables (no docstrings, just show contents)?
#   - Skip undocumented functions, methods, descriptors, classes, etc.

def format_docstring(f, obj):
    docstring = inspect.getdoc(obj)
    if docstring:
        f.write('<div class="docstring">\n%s\n</div>\n' % docstring)


# TODO process signature override from 1st line of docstring
def format_method(f, fn, name, class_name):
    argspec = inspect.getargspec(fn)
    argspec = argspec._replace(args=argspec.args[1:]) # skip 'self'
    signature = name + inspect.formatargspec(*argspec)
    f.write('\n#### `%(signature)s`{.python} {#%(class_name)s.%(name)s}\n\n'
            % {'signature': signature, 'class_name': class_name, 'name': name})
    format_docstring(f, fn)


def format_descriptor(f, descriptor, name, class_name):
    f.write('\n#### `%(name)s` {#%(class_name)s.%(name)s}\n\n'
            % {'class_name': class_name, 'name': name})
    format_docstring(f, descriptor)


def format_alias(f, alias):
    f.write('Alias for `%s`.\n' % alias)


def format_class_members(f, cls, class_name):
    if inspect.ismethod(cls.__init__):  # False for object.__init__
        format_method(f, cls.__init__, '__init__', class_name)
    for name in dir(cls):
        if name.startswith('_'):
            continue
        attr = getattr(cls, name)
        if inspect.ismethod(attr):  # method or classmethod
            format_method(f, attr, name, class_name)
        elif inspect.isfunction(attr):  # staticmethod
            format_method(f, attr, name, class_name)
        elif inspect.isdatadescriptor(attr):  # descriptor, e.g. property
            format_descriptor(f, attr, name, class_name)


def format_module_docs(module_name):
    toc = StringIO()
    doc = StringIO()

    module = importlib.import_module(module_name)
    source = inspect.getsourcefile(module)
    doc.write('# Module `%(name)s` {#%(name)s}\n' % {'name': module_name})
    toc.write('[Module `%(name)s`](#%(name)s)\n\n' % {'name':  module_name})

    format_docstring(doc, module)

    if hasattr(module, '__all__'):
        members = module.__all__
    else:
        members = sorted([name for name in dir(module)
                          if not name.startswith('_')])

    classes, functions, exceptions = [], [], []
    for name in members:
        attr = getattr(module, name)
        try:
            is_local = inspect.getsourcefile(attr) == source
        except TypeError:
            is_local = False
        if not is_local and name not in getattr(module, '__all__', []):
            continue
        if is_local:
            alias = None
        else:
            other_module = inspect.getmodule(attr)
            alias = other_module.__name__ + '.' + attr.__name__
        if inspect.isclass(attr):
            if issubclass(attr, Exception):
                exceptions.append((name, attr, alias))
            else:
                classes.append((name, attr, alias))
        elif inspect.isfunction(attr):
            functions.append((name, attr, alias))

    if classes:
        doc.write('\n## Classes\n\n')
        toc.write('\n[Classes](#classes)\n\n')
        for name, cls, alias in classes:
            doc.write('\n### `class %(name)s`{.python} {#%(name)s}\n\n'
                    % {'name': name})
            toc.write('  - [%(name)s](#%(name)s)\n' % {'name': name})
            if alias:
                format_alias(doc, alias)
            else:
                # TODO document base classes
                format_docstring(doc, cls)
                format_class_members(doc, cls, name)

    if functions:
        doc.write('\n## Functions\n\n')
        toc.write('\n[Functions](#functions)\n\n')
        for name, fn, alias in functions:
            # TODO process signature override from 1st line of docstring
            signature = name + inspect.formatargspec(*inspect.getargspec(fn))
            doc.write('\n### `%(signature)s`{.python} {#%(name)s}\n\n'
                    % {'signature': signature, 'name': name})
            toc.write('  - [%(name)s](#%(name)s)\n' % {'name': name})
            if alias:
                format_alias(doc, alias)
            else:
                format_docstring(doc, fn)

    if exceptions:
        doc.write('\n## Exceptions\n\n')
        toc.write('\n[Exceptions](#exceptions)\n\n')
        for name, cls, alias in exceptions:
            doc.write('\n### `class %(name)s`{.python} {#%(name)s}\n\n'
                    % {'name': name})
            toc.write('  - [%(name)s](#%(name)s)\n' % {'name': name})
            if alias:
                format_alias(doc, alias)
            else:
                format_docstring(doc, cls)

    return doc, toc

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage = __doc__.strip()
        sys.exit(usage)

    module_name, output_dir = sys.argv[1:]
    mkd_path = os.path.join(output_dir, module_name + '.mkd')
    doc, toc = format_module_docs(module_name)

    with open(mkd_path, 'w') as f:
        f.write('<div id="module-toc">\n' + toc.getvalue() + '\n</div>')
        f.write('\n')
        f.write(doc.getvalue())
