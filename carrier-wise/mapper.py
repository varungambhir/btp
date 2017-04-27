#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    print "%s\t%s-%s-%s" % (row[8], row[0], row[1], row[2])
