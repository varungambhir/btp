"""
Calculates average delay time per carrier.

Usage: cat file-name | python avg.py | cat >>output-file-name
"""

import csv
import sys

data = csv.reader(sys.stdin, delimiter='\t')

carrier_dict = {}

for (x, y) in data:
    carrier, delay_time = x.split("#")
    if carrier == "24":
        carrier = "00"
    count = y
    if carrier in carrier_dict:
        carrier_dict[carrier].append((int(delay_time), int(count)))
    else:
        carrier_dict[carrier] = [(int(delay_time), int(count))]


for carrier in sorted(carrier_dict):
    lst = carrier_dict[carrier]
    numerator = reduce(lambda x ,y: x + y[0]*y[1], lst, 0)
    denominator = sum([y for (x, y) in lst])
    print "%s\t%f" % (carrier, (numerator*1.0)/(denominator*1.0))
