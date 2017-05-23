"""
Plots the bar-chart showing average delay versus carrier

Usage: cat file-name | python plot.py
"""

import sys
import csv
import calendar

from matplotlib import pyplot as plt

reader = csv.reader(sys.stdin, delimiter='\t')

# Apply the top_carriers filter, if reqd
# top_carriers = ["AA", "DL", "WN", "UA", "AS", "CO", "NW"]

data = [[x, y] for (x, y) in reader] # if x in top_carriers]
seperated_data = zip(*data)

# Use different colour for departure and arrival
plt.bar([i for i, x in enumerate(seperated_data[0])], seperated_data[1], color='#ab6e22', align='center', width = 0.67)
plt.xlabel('Carrier')
D = zip(*((i, x) for i, x in enumerate(seperated_data[0])))
plt.xticks(D[0], D[1])
plt.ylabel('Average Delay in Minutes')
# Adjust axis accordingly
plt.axis([-1, len(data), -1, 14])

# Change to arrival or departure as per case
plt.title('Average Departure Delay by Carrier')
plt.show()