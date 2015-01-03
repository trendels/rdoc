import sys

print "% API Documentation\n"
for module_name in sys.argv[1:]:
    print "  - `%s`" % module_name
