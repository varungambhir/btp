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

data = [(x[0].split('#')[0],\
 x[0].split('#')[1].split(' ')[0],\
 x[0].split('#')[1].split(' ')[1],\
 int(x[1])) for x in data]

def convert(x):
    return datetime.strptime(x, "%Y-%m-%d").date()




# Extracting data for an airport
def extract_by_airport(data, airport):
    # (date, delayed_or_not, count)
    return [(convert(x[1]), x[2], int(x[3])) for x in data if x[0] == airport]

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

# Computes the percentage delayed list
def calculate_delay_percentage(airport_list):
    airport_list_del = [(x[0], x[2]) for x in airport_list if x[1] == "Delayed"]
    airport_list_nd = [(x[0], x[2]) for x in airport_list if x[1] == "Not"]
    # print airport_list_del
    # print airport_list_nd
    return list(map(lambda x: (x[0][0], float(x[0][1]/(float(x[0][1]+x[1][1]))) ) , zip(airport_list_del, airport_list_nd)))

SFO = calculate_delay_percentage(SFO)
OAK = calculate_delay_percentage(OAK)
JFK = calculate_delay_percentage(JFK)
ORD = calculate_delay_percentage(ORD)
LAX = calculate_delay_percentage(LAX)


# Plotting

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