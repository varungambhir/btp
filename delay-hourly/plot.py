"""
Plots the bar-chart showing average delay versus hour_of_the_day

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
plt.bar(data_dict.keys(), data_dict.values(), color='#ab6e22', align='center', width = 0.67)
plt.xlabel('Hour of the day')
plt.xticks(xrange(0, 24))
plt.ylabel('Average Delay in Minutes')
# Adjust axis accordingly (16 for dep, 14 for arr)
plt.axis([-1, 24, 0, 16])

# Change to arrival or departure as per case
plt.title('Average Departure Delay by Hour')
plt.show()