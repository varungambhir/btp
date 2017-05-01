"""
Distance vs On-time arrival performance By Airlines
"""
import numpy as np
np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
from matplotlib import pyplot as plt
import csv

data = []
# For departure output-all-dep-delays
with open('output-all-arr-delays', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader]


airlines = {}
for x in data:
    airline_code, dist_bucket, status = x[0].split('-')
    count = int(x[1])
    dist_bucket = int(dist_bucket)
    if airline_code in airlines:
        if status in airlines[airline_code]:
            airlines[airline_code][status].append((dist_bucket, count))
        else:
            airlines[airline_code][status] = [(dist_bucket, count)]
    else:
        airlines[airline_code] = {status: [(dist_bucket, count)]}

# Filtering
top_airlines = ["AA", "DL", "WN", "UA", "AS", "CO", "NW"]
airlines = dict((key, value) for key, value in airlines.iteritems() if key in top_airlines)

# Sorting buckets
for airline in airlines:
    for status in airlines[airline]:
        airlines[airline][status].sort()

plt_data = {}
# Extracting for plotting
for airline in airlines:
    lst = []
    for i in xrange(0, len(airlines[airline]["Delayed"])):
        value = float(airlines[airline]["Not Delayed"][i][1])/(float(airlines[airline]["Delayed"][i][1]) + float(airlines[airline]["Not Delayed"][i][1]))
        lst.append((airlines[airline]["Delayed"][i][0], value))
    plt_data[airline] = lst

# for x in plt_data:
#     print x, plt_data[x]

import matplotlib.pyplot as plt
radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]
square = [1.0, 4.0, 9.0, 16.0, 25.0, 36.0]
for airline in plt_data:
    plt.plot([x for x,y in plt_data[airline]], [y for x,y in plt_data[airline]], label=airline)

print plt.xticks()
plt.xlabel('Distance Group')
plt.ylabel('On-time percentage')
plt.title('Distance V.S. Arrival On-Time Performance of Airlines')
plt.legend()
plt.xticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600], ["< 200", "200-400", "400-600", "600-800", "800-1000", "1000-1200", "1200-1400", "1400-1600", "> 1600"])
plt.show()