from __future__ import absolute_import

import importlib
import inspect
import os
import shutil
import sys

from .util import usage

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

DATA_FILES = '''\
Makefile
meta.yml
modules
filters/autolink.py
filters/highlight_builtins.py
src/index.mkd
static/style.css
templates/rdoc.html5
'''.split()

__version__ = '0.1'

def relpath():
    """
    Usage: relpath <path> <start>

    Print a version of <path> relative to path <start>.
    """
    if len(sys.argv) != 3:
        sys.exit(usage(relpath))
    path, start = sys.argv[1:]
    print os.path.relpath(path, os.path.dirname(start))


def make_index():
    print "% Module Index\n"
    for module_name in sys.argv[1:]:
        print "  - `%s`" % module_name


def make_links():
    links = {}
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                identifier, url = line.strip().split('|', 1)
                links[identifier] = url
    print '---'
    print 'links:'
    for identifier, url in sorted(links.iteritems()):
        print "  '%s': '%s'" % (identifier, url)
    print '...'


def make_rules():
    for module_name in sys.argv[1:]:
        module = importlib.import_module(module_name)
        path = inspect.getsourcefile(module)
        print "build/modules/%(name)s.mkd build/modules/%(name)s.links: %(path)s" % {'name': module_name, 'path': path}
        print "\t@mkdir -p $(dir $@)"
        print "\trdoc-extract %s build/modules/" % module_name


def init():
    # Recursively copy all fies from the data directory to the current
    # directory. Skip destination files that already exist.
    cwd = os.getcwd()
    print "Copying files ..."
    for path in DATA_FILES:
        src = os.path.join(DATA_DIR, path)
        dest = os.path.join(cwd, path)
        if os.path.exists(dest):
            print "  skipping '%s': file exists" % dest
            continue
        dirname = os.path.dirname(dest)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        print "  %s" % dest
        shutil.copy(src, dest)
    print "Done."
