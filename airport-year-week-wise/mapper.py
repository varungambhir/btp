#!/usr/bin/env python

import sys
import csv
from datetime import date

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        #Getting ISO Week
        year, weekno, weekday = date(int(row[0]), int(row[1]), int(row[2])).isocalendar()
        print "%s#%s-%s\tX" % (row[16], year, ('0' + str(weekno))[-2:])
    except:
        pass