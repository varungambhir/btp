#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        print "%s->%s\t%s-%s-%s" % (row[16], row[17] + (" Delayed" if int(row[15]) >= 15 else " Not Delayed"), row[0], row[1], row[2])
    except:
        pass
