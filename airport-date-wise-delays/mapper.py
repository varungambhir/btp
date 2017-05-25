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
        # 15 for departure, 14 for arrival
        delayed = ("Delayed" if int(row[15]) >= 15 else "Not Delayed")
        if year == "Year":
            continue
        print "%s#%s-%s-%s %s\tX" % (origin, year, month, day, delayed)
    except:
        pass