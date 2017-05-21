#!/usr/bin/env python

"""
To create bar chart with avg delay minutes vs weekday.
Run this job on 2001-2008 data.

Output key is weekday#delay_time
"""

import sys
import csv

reader = csv.reader(sys.stdin)

month_dict = {}

for row in reader:
    try:
        cancelled = row[21]
        # Dep delay 15, Arr delay 14
        delay_time = row[14]
        weekday = row[3]
        if cancelled == "1" or delay_time == "NA" or cancelled == "Cancelled":
            continue
        print "%s#%s\tX" % (weekday, delay_time)
    except:
        pass