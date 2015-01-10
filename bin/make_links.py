#!/usr/bin/env python
import os
import sys

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
