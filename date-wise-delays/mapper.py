#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        print "%s-%s-%s %s\tX" % (row[0], ('0'+row[1])[-2:],\
         ('0'+row[2])[-2:], (" Delayed" if int(row[15]) >= 15 else " Not Delayed"))
    except:
        pass