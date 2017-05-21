"""
Calculates average delay time per month.

Usage: cat file-name | python avg.py | cat >>output-file-name
"""

import csv
import sys

data = csv.reader(sys.stdin, delimiter='\t')

month_dict = {}

for (x, y) in data:
    month, delay_time = x.split("#")
    count = y
    if month in month_dict:
        month_dict[month].append((int(delay_time), int(count)))
    else:
        month_dict[month] = [(int(delay_time), int(count))]

for month in sorted(month_dict):
    lst = month_dict[month]
    numerator = reduce(lambda x ,y: x + y[0]*y[1], lst, 0)
    denominator = sum([y for (x, y) in lst])
    print "%s\t%f" % (month, (numerator*1.0)/(denominator*1.0))
