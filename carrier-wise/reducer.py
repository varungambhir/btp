#!/usr/bin/env python

import sys

prevCarrier = None
count = 0

for line in sys.stdin:
    line = line.strip()
    carrier, date = line.split('\t')

    if prevCarrier and prevCarrier != carrier:
        print "%s\t%d" % (prevCarrier, count)
        count = 0

    count += 1
    prevCarrier = carrier

if prevCarrier:
    print "%s\t%d" % (prevCarrier, count)
