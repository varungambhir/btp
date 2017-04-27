#!/usr/bin/env python

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:
    try:
    	hour = row[5]
    	if len(hour) < 2:
    		hour = '0' + hour + '00'
    	elif len(hour) < 4:
    		hour = '0' + hour
    	hour = hour[0:2]
        print "%s %s\tX" % (hour, (" Delayed" if int(row[15]) >= 15 else " Not Delayed"))
    except:
        pass