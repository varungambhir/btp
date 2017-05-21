"""
Calculates average delay time per weekday.

Usage: cat file-name | python avg.py | cat >>output-file-name
"""

import csv
import sys

data = csv.reader(sys.stdin, delimiter='\t')

weekday_dict = {}

for (x, y) in data:
    weekday, delay_time = x.split("#")
    if weekday == "24":
        weekday = "00"
    count = y
    if weekday in weekday_dict:
        weekday_dict[weekday].append((int(delay_time), int(count)))
    else:
        weekday_dict[weekday] = [(int(delay_time), int(count))]


for weekday in sorted(weekday_dict):
    lst = weekday_dict[weekday]
    numerator = reduce(lambda x ,y: x + y[0]*y[1], lst, 0)
    denominator = sum([y for (x, y) in lst])
    print "%s\t%f" % (weekday, (numerator*1.0)/(denominator*1.0))
