import os
import importlib
import inspect
import sys

for module_name in sys.argv[1:]:
    module = importlib.import_module(module_name)
    path = inspect.getsourcefile(module)
    print "build/%s.mkd: %s" % (module_name, path)
    print "\t@mkdir -p $(dir $@)"
    print "\tpython extract.py %s build/" % module_name
