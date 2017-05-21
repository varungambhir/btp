#!/usr/bin/env python

"""
To create histogram with number of minutes delayed as buckets.
Run this job on 2001-2008 data

NOTE:- Strip off extreme values for better graph
"""

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
    	cancelled = row[21]
    	# Dep delay 15, Arr delay 14
    	delay_time = row[15]
    	if cancelled == "1" or delay_time == "NA":
    		continue
        print "%s\tX" % (delay_time)
    except:
        pass