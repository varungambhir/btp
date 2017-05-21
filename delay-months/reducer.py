#!/usr/bin/env python

import sys

prevKey = None
count = 0

for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')

    if prevKey and prevKey != key:
        print "%s\t%d" % (prevKey, count)
        count = 0

    count += 1
    prevKey = key

if prevKey:
    print "%s\t%d" % (prevKey, count)
