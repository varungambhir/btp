"""
Number of flights based plotting
"""
import numpy as np
import random
np.random.seed(sum(map(ord, 'calmap')))
import pandas as pd
import calmap
import matplotlib
from matplotlib import pyplot as plt
import csv
from datetime import datetime
from ggplot import *
import matplotlib.dates as dates

data = []
with open('output-all', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader]

def convert(x):
    num = x.split("#")[1].split("-")
    return float(num[0]) + float(num[1])/53.0 # YEAR + WEEK/53.0

# Extracting data
SFO = [(convert(x[0]), int(x[1])) for x in data if x[0].startswith("SFO")]
JFK = [(convert(x[0]), int(x[1])) for x in data if x[0].startswith("JFK")]
ORD = [(convert(x[0]), int(x[1])) for x in data if x[0].startswith("ORD")]
LAX = [(convert(x[0]), int(x[1])) for x in data if x[0].startswith("LAX")]
# Removing end values
SFO = SFO[1:-1]
JFK = JFK[1:-1]
ORD = ORD[1:-1]
LAX = LAX[1:-1]
matplotlib.style.use('ggplot')
# ALL IN ONE PLOT
# data = zip([x[0] for x in SFO], [x[1] for x in SFO], [x[1] for x in JFK], [x[1] for x in ORD], [x[1] for x in LAX])
# pltd = pd.DataFrame(data=data, columns=["date", "SFO", "JFK", "ORD", "LAX"])
# p = ggplot(pd.melt(pltd, id_vars=['date']), aes(x='date', y='value', color='variable'))
# print (p + geom_point() + geom_line(position = 'jitter'))
#pltd4 = pd.DataFrame(data=LAX, columns=["date", "count"])
#pltd3 = pd.DataFrame(data=ORD, columns=["date", "count"])
#pltd2 = pd.DataFrame(data=JFK, columns=["date", "count"])

pltd1 = pd.DataFrame(data=SFO, columns=["date", "count"])
pltd1.time = pd.to_datetime(pltd1['date'],format='%Y-%m-%d')
pltd1.set_index(['date'],inplace=True)
fig, axes = plt.subplots(nrows=2,ncols=2)
plt.subplots_adjust(hspace=0.4)
#axes.plot(pltd1.index,pltd1.columns,label='line1', c='r')
pltd1.plot(ax=axes[0,0],title='SFO')

pltd2 = pd.DataFrame(data=SFO, columns=["date", "count"])
pltd2.time = pd.to_datetime(pltd2['date'],format='%Y-%m-%d')
pltd2.set_index(['date'],inplace=True)

pltd2.plot(ax=axes[0,1],title='JFK')

pltd3 = pd.DataFrame(data=SFO, columns=["date", "count"])
pltd3.time = pd.to_datetime(pltd3['date'],format='%Y-%m-%d')
pltd3.set_index(['date'],inplace=True)
pltd3.plot(ax=axes[1,0],title='ORD')

pltd4 = pd.DataFrame(data=SFO, columns=["date", "count"])
pltd4.time = pd.to_datetime(pltd4['date'],format='%Y-%m-%d')
pltd4.set_index(['date'],inplace=True)
pltd4.plot(ax=axes[1,1],title='LAX')
plt.show()
#print ggplot(pltd1, aes('date', 'count')) + geom_line('jitter', color='steelblue')


#print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')

#print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')'''
