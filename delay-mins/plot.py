"""
Plots the histogram showing percentage of flights against minutes delayed

Usage: cat file-name | python plot.py
"""

import sys
import csv

from matplotlib import pyplot as plt

reader = csv.reader(sys.stdin, delimiter='\t')
data = [[x, y] for (x, y) in reader]

total = float(sum([int(y) for (x, y) in data]))
data_dict = {int(k): float(v)/total for k,v in data}

lower_lim = -5.0
upper_lim = 100.0

data_dict = {k: v for k, v in data_dict.items() if lower_lim <= k and k <= upper_lim}

plt.bar(data_dict.keys(), data_dict.values(), width=1.0, color='b')
plt.show()