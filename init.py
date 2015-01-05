#!/usr/bin/env python
"""
Usage: init.py <directory>
"""
import os
import shutil
import sys

file_list = '''
extract.py
filters/autolink.py
filters/highlight_builtins.py
Makefile
make_index.py
make_rules.py
meta.yml
modules
pandoc.html5
relpath.py
src/index.mkd
static/style.css
'''.split()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = __doc__.strip()
        sys.exit(usage)

    root = sys.argv[1]
    if os.path.exists(root):
        sys.exit("Directory '%s' already exists. Exiting." % root)

    print "Copying files ..."

    for path in file_list:
        dest_path = os.path.join(root, path)
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        print dest_path
        shutil.copy(path, dest_dir)

    print "... done."
