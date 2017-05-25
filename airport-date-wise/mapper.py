#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        origin = row[16]
        year = row[0]
        month = ("0" + row[1])[-2:]
        day = ("0" + row[2])[-2:]

        if year == "Year":
            continue
        print "%s#%s-%s-%s\tX" % (origin, year, month, day)
    except:
        pass