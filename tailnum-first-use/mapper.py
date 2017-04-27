#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        print "%s\t%s-%s-%s" % (row[10], row[0], ('0'+row[1])[-2:], ('0'+row[2])[-2:])
    except:
        pass
