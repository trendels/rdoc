import importlib
import inspect
import sys

for module_name in sys.argv[1:]:
    module = importlib.import_module(module_name)
    path = inspect.getsourcefile(module)
    print "build/api/%(name)s.mkd build/api/%(name)s.links: %(path)s" \
            % {'name': module_name, 'path': path}
    print "\t@mkdir -p $(dir $@)"
    print "\tpython extract.py %s build/api/" % module_name
