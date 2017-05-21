#!/usr/bin/env python

"""
To create bar chart with avg delay minutes vs hour_of_the_day.
Run this job on 2001-2008 data.

Output key is hour_of_the_day#delay_time
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
        if cancelled == "1" or delay_time == "NA" or cancelled == "Cancelled":
            continue    
        # CRSDepTime 5, CRSArrTime 7
        hour = int(row[7])/100
        hour = ("0" + str(hour))[-2:]
        print "%s#%s\tX" % (hour, delay_time)
    except:
        pass