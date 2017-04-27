"""
Percentage of delays per source airport based plotting
"""
import numpy as np
np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
from matplotlib import pyplot as plt
import csv
from datetime import datetime


def consolidate(delayed, not_delayed, threshold):
    i = 0
    j = 0
    consolidated = []
    while(i < len(delayed) and j < len(not_delayed)):
        if delayed[i][0] == not_delayed[j][0]:
            delay = float(delayed[i][1])
            total = float(delay + float(not_delayed[j][1]))
            consolidated.append([delayed[i][0], delay/total])
            i += 1
            j += 1
        elif delayed[i][0] <= not_delayed[j][0]:
            i += 1
        else:
            j += 1
    consolidated = filter(lambda x: x[1] >= threshold, consolidated)
    consolidated.sort(key=lambda x: x[1], reverse=True)
    return consolidated


"""
CALCULATE GAUSSIAN TOO
"""
data = []
SRC = "ORD"
with open('output-all', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader if x[0].startswith(SRC)]


delayed = [[x[0].split()[0].split('->')[1], x[1]] for x in data if x[0].split()[1] == "Delayed"]
not_delayed = [[x[0].split()[0].split('->')[1], x[1]] for x in data if x[0].split()[1] == "Not"]

consolidated = consolidate(delayed, not_delayed, 0.25)


# consolidated = consolidated[0:len(consolidated)/16]
# plt.xticks([x for x in xrange(len(consolidated))], [x[0] for x in consolidated])
# plt.bar([x for x in xrange(len(consolidated))], [x[1] for x in consolidated])
# plt.show()



############################# PLOTTING ON MAP
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import math


# create the map
map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# load the shapefile, use the name 'states'
map.readshapefile('../../basemap-1.0.7/examples/st99_d00', name='states', drawbounds=True)

scale = 5


airports = {}
with open('../../other-data/airports.csv', 'r') as f:
    reader = csv.reader(f)
    airports = dict((row[0], row[5:]) for row in reader)

# Get the location of each city and plot it
for (airport_code, count) in consolidated:
    lat, lon = airports[airport_code]
    x, y = map(float(lon), float(lat))
    map.plot(x, y, marker='o',color='Red',markersize=scale)

lat_src, lon_src = airports[SRC]
x_src, y_src = map(float(lon_src), float(lat_src))
map.plot(x_src, y_src, marker='o',color='Green', markersize=scale)

plt.show()
