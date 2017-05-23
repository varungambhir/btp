"""
Plots the bar-chart showing average delay versus month

Usage: cat file-name | python plot.py
"""

import sys
import csv
import calendar

from matplotlib import pyplot as plt

reader = csv.reader(sys.stdin, delimiter='\t')
data = [[x, y] for (x, y) in reader]

data_dict = {int(k): float(v) for k,v in data}

# Use different colour for departure and arrival
plt.bar(data_dict.keys(), data_dict.values(), color='#aa00ff', align='center', width = 0.67)
plt.xlabel('Month')
plt.xticks(xrange(1, 13), [calendar.month_abbr[x] for x in xrange(1, 13)])
plt.ylabel('Average Delay in Minutes')
# Adjust axis accordingly
plt.axis([0, 13, 0, 14])

# Change to arrival or departure as per case
plt.title('Average Departure Delay by Month')
plt.show()