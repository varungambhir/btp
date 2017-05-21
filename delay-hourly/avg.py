"""
Calculates average delay time per hour_of_the_day.

Usage: cat file-name | python avg.py | cat >>output-file-name
"""

import csv
import sys

data = csv.reader(sys.stdin, delimiter='\t')

hour_dict = {}

for (x, y) in data:
    hour, delay_time = x.split("#")
    if hour == "24":
        hour = "00"
    count = y
    if hour in hour_dict:
        hour_dict[hour].append((int(delay_time), int(count)))
    else:
        hour_dict[hour] = [(int(delay_time), int(count))]


for hour in sorted(hour_dict):
    lst = hour_dict[hour]
    numerator = reduce(lambda x ,y: x + y[0]*y[1], lst, 0)
    denominator = sum([y for (x, y) in lst])
    print "%s\t%f" % (hour, (numerator*1.0)/(denominator*1.0))
