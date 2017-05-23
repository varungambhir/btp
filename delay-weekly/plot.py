"""
Plots the bar-chart showing average delay versus weekday

Usage: cat file-name | python plot.py
"""

import sys
import csv
import calendar

from matplotlib import pyplot as plt

reader = csv.reader(sys.stdin, delimiter='\t')
data = [[x, y] for (x, y) in reader]

data_dict = {int(k)-1: float(v) for k,v in data}

# Use different colour for departure and arrival
plt.bar(data_dict.keys(), data_dict.values(), color='#ab6e22', align='center', width = 0.67)
plt.xlabel('Day')
plt.xticks(xrange(0, 7), [calendar.day_abbr[x] for x in xrange(0, 7)])
plt.ylabel('Average Delay in Minutes')

# Change to arrival or departure as per case
plt.title('Average Departure Delay by Day')
plt.show()