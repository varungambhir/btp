"""
Number of flights based plotting
"""
import pandas as pd
from matplotlib import pyplot as plt
import csv
from datetime import datetime
from ggplot import *

data = []

with open('output-all', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    data = [x for x in reader]

def convert(x):
    date = x.split("#")[1]
    return datetime.strptime(date, "%Y-%m-%d").date()



# Extracting data for an airport
def extract_by_airport(data, airport):
    # (date, count)
    return [(convert(x[0]), int(x[1])) for x in data if x[0].startswith(airport)]

SFO = extract_by_airport(data, "SFO")
OAK = extract_by_airport(data, "OAK")
JFK = extract_by_airport(data, "JFK")
ORD = extract_by_airport(data, "ORD")
LAX = extract_by_airport(data, "LAX")


# Filtering for one year
def filter_by_date(airport_list):
    # Choose start_date and end_date as per plot
    start_date = datetime.strptime("2005-01-01", "%Y-%m-%d").date()
    end_date = datetime.strptime("2005-12-31", "%Y-%m-%d").date()
    return filter(lambda x: start_date <= x[0] and x[0] <= end_date, airport_list)

SFO = filter_by_date(SFO)
OAK = filter_by_date(OAK)
JFK = filter_by_date(JFK)
ORD = filter_by_date(ORD)
LAX = filter_by_date(LAX)



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
print p + geom_line(position = 'jitter')# +\
 # scale_x_continuous(limits=(1987.5,2009.2)) +\
 # scale_y_continuous(limits=(400,7500))# +\
 # geom_point()