#!/usr/bin/env python
import importlib
import inspect
import sys

for module_name in sys.argv[1:]:
    module = importlib.import_module(module_name)
    path = inspect.getsourcefile(module)
    print "build/modules/%(name)s.mkd build/modules/%(name)s.links: %(path)s" \
            % {'name': module_name, 'path': path}
    print "\t@mkdir -p $(dir $@)"
    print "\tpython bin/extract.py %s build/modules/" % module_name
