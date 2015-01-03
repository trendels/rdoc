"""
Usage: relpath.py <path> <start>

Return a version of <path> relative to path <start>.
"""
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage = __doc__.strip()
        sys.exit(usage)
    path, start = sys.argv[1:]
    print os.path.relpath(path, os.path.dirname(start))
