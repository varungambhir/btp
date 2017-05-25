"""
Number of flights based plotting
"""
import pandas as pd
from matplotlib import pyplot as plt
import csv
from ggplot import *

data = []

with open('output-all', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader]

def convert(x):
    num = x.split("#")[1].split("-")
    return float(num[0]) + float(num[1])/53.0 # YEAR + WEEK/53.0

# Extracting data for an airport and removing end values
def extract_by_airport(data, airport):
    # (year+week/53.0, count)
    return [(convert(x[0]), int(x[1])) for x in data if x[0].startswith(airport)][1:-1]

SFO = extract_by_airport(data, "SFO")
OAK = extract_by_airport(data, "OAK")
JFK = extract_by_airport(data, "JFK")
ORD = extract_by_airport(data, "ORD")
LAX = extract_by_airport(data, "LAX")


# ALL IN ONE PLOT
data = zip([x[0] for x in SFO],\
 [x[1] for x in SFO],\
 [x[1] for x in OAK],\
 [x[1] for x in JFK],\
 [x[1] for x in ORD],\
 [x[1] for x in LAX])

pltd = pd.DataFrame(data=data, columns=["date",\
 "SFO",\
 "OAK",\
 "JFK",\
 "ORD",\
 "LAX"])

p = ggplot(pd.melt(pltd, id_vars=['date']), aes(x='date', y='value', color='variable'))
print p + geom_line(position = 'jitter') +\
 scale_x_continuous(limits=(1987.5,2009.2)) +\
 scale_y_continuous(limits=(400,7500))# +\
 # geom_point()