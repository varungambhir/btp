#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        print "%s\tX" % (row[3])
    except:
        pass