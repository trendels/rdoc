#!/usr/bin/env python
import sys

print "% Module Index\n"
for module_name in sys.argv[1:]:
    print "  - `%s`" % module_name
