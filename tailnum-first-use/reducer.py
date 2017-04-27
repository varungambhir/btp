#!/usr/bin/env python

import sys
from datetime import datetime

prevKey = None
minDate = datetime.strptime("2099-01-01", "%Y-%m-%d")

for line in sys.stdin:
    line = line.strip()
    try:
        key, date = line.split('\t')
        key = key.encode().decode('utf-8')
    except:
        continue
    #key = key.encode().decode('utf-8')
    date = datetime.strptime(date, "%Y-%m-%d")

    if prevKey and prevKey != key:
        print "%s\t%s" % (prevKey, minDate.strftime("%Y-%m-%d"))
        minDate = datetime.strptime("2099-01-01", "%Y-%m-%d")

    minDate = min(minDate, date)
    prevKey = key

if prevKey:
    print "%s\t%s" % (prevKey, minDate.strftime("%Y-%m-%d"))
