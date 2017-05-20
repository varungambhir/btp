"""
Number of flights based plotting
"""
import numpy as np
np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
from matplotlib import pyplot as plt
import csv
from datetime import datetime

data = []

with open('output-all', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader]

# data = [x for x in data if x[0].startswith("198")] # FOR FILTERING

# dates = [datetime.strptime(x[0], '%Y-%m-%d') for x in data]
# count = [int(x[1]) for x in data]
# events = pd.Series(np.array(count), index=dates)
# calmap.calendarplot(events, cmap='YlGn', fillcolor='grey', linewidth=0, daylabels='')
# plt.show()

for i in xrange(1987, 2008, 3):
    # Filtering Data for 3 years only
    dates = [datetime.strptime(x[0], '%Y-%m-%d') for x in data if x[0] >= (str(i) + "-01-01") and x[0] <= (str(i+2) + "-12-31")]
    count = [int(x[1]) for x in data if x[0] >= (str(i) + "-01-01") and x[0] <= (str(i+2) + "-12-31")]
    events = pd.Series(np.array(count), index=dates)
    calmap.calendarplot(events, cmap='YlGn', fillcolor='grey', linewidth=0, daylabels='')
    plt.show()
