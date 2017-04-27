#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        print "%s#%s-%s\tX" % (row[16], row[0], ('0'+row[1])[-2:])
    except:
        pass