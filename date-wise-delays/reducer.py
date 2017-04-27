#!/usr/bin/env python

import sys

prevAirport = None
count = 0

for line in sys.stdin:
    line = line.strip()
    airport, date = line.split('\t')

    if prevAirport and prevAirport != airport:
        print "%s\t%d" % (prevAirport, count)
        count = 0

    count += 1
    prevAirport = airport

if prevAirport:
    print "%s\t%d" % (prevAirport, count)
