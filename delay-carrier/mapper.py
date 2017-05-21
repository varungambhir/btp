#!/usr/bin/env python

"""
To create bar chart with avg delay minutes vs carrier.
Run this job on 2001-2008 data.

Output key is carrier#delay_time
"""

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        cancelled = row[21]
        # Dep delay 15, Arr delay 14
        delay_time = row[14]
        carrier = row[8]
        if cancelled == "1" or delay_time == "NA" or cancelled == "Cancelled":
            continue
        print "%s#%s\tX" % (carrier, delay_time)
    except:
        pass