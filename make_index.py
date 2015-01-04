import sys

print "---\ntitle: API Documentation\n---\n"
for module_name in sys.argv[1:]:
    print "  - `%s`" % module_name
