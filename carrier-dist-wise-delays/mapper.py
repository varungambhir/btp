#!/usr/bin/env python

import sys
import csv
from bisect import bisect_left

reader = csv.reader(sys.stdin)
distances = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600]

for row in reader:
    try:
        carrier_code = row[8]
        dist = int(row[18])
        delay = ("Delayed" if int(row[14]) >= 15 else "Not Delayed")
        distance_bucket = distances[bisect_left(distances, dist)-1]
        print "%s-%s-%s\tX" % (carrier_code, distance_bucket, delay)
    except:
        pass