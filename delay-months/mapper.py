#!/usr/bin/env python

"""
To create histogram with month number delayed as buckets against avg delay minutes.
Run this job on 2001-2008 data.

Output key is month_no#delay_time
"""

import sys
import csv

reader = csv.reader(sys.stdin)

month_dict = {}

for row in reader:
    try:
        cancelled = row[21]
        # Dep delay 15, Arr delay 14
        delay_time = row[15]
        month = ("0"+row[1])[-2:]
        if cancelled == "1" or delay_time == "NA" or cancelled == "Cancelled":
            continue
        print "%s#%s\tX" % (month, delay_time)
    except:
        pass