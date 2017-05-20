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
from ggplot import *

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


# ALL IN ONE PLOT
# data = zip([x[0] for x in SFO], [x[1] for x in SFO], [x[1] for x in JFK], [x[1] for x in ORD], [x[1] for x in LAX])
# pltd = pd.DataFrame(data=data, columns=["date", "SFO", "JFK", "ORD", "LAX"])
# p = ggplot(pd.melt(pltd, id_vars=['date']), aes(x='date', y='value', color='variable'))
# print (p + geom_point() + geom_line(position = 'jitter'))

pltd = pd.DataFrame(data=SFO, columns=["date", "count"])
print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')

pltd = pd.DataFrame(data=JFK, columns=["date", "count"])
print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')

pltd = pd.DataFrame(data=ORD, columns=["date", "count"])
print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')

pltd = pd.DataFrame(data=LAX, columns=["date", "count"])
print ggplot(pltd, aes('date', 'count')) + geom_line('jitter', color='steelblue')

