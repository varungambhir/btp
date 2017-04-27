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
	data = [x for x in reader if x[0].startswith("200")]




dates = [datetime.strptime(x[0], '%Y-%m-%d') for x in data]

count = [int(x[1]) for x in data]

events = pd.Series(np.array(count), index=dates)
# for year in xrange(1987, 1991):
# 	calmap.yearplot(events, year=year, cmap="Greens")
# 	ax[0, 0].plot
# 	plt.show()
calmap.calendarplot(events, cmap="Greens")
plt.show()
