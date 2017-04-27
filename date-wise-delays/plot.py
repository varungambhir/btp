"""
Percentage of delays based plotting
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

delayed = [[x[0].split()[0], x[1]] for x in data if x[0].split()[0].startswith("198") and x[0].split()[1] == "Delayed"]
not_delayed = [[x[0].split()[0], x[1]] for x in data if x[0].split()[0].startswith("198") and x[0].split()[1] == "Not"]

dates = [datetime.strptime(x[0], '%Y-%m-%d') for x in delayed]

count = []
for i in xrange(0, len(delayed)):
	delay = int(delayed[i][1])
	not_d = int(not_delayed[i][1])
	count.append(float(delay)/float(delay+not_d))
# print count
events = pd.Series(np.array(count), index=dates)
# for year in xrange(1987, 1991):
# 	calmap.yearplot(events, year=year, cmap="Greens")
# 	ax[0, 0].plot
# 	plt.show()
calmap.calendarplot(events)#, cmap="Pastel1")
plt.show()
