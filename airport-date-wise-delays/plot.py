"""
Number of flights based plotting
"""
import pandas as pd
from matplotlib import pyplot as plt
import csv
from datetime import datetime
from ggplot import *


holidays_list = {}


holidays_list["2001"] = ["01/01/2001", "01/15/2001", "02/19/2001", "05/28/2001", "07/04/2001", "09/03/2001", "10/08/2001", "11/12/2001", "11/22/2001", "12/25/2001"]
holidays_list["2002"] = ["01/01/2002", "01/21/2002", "02/18/2002", "05/27/2002", "07/04/2002", "09/02/2002", "10/14/2002", "11/11/2002", "11/28/2002", "12/25/2002"]
holidays_list["2003"] = ["01/01/2003", "01/20/2003", "02/17/2003", "05/26/2003", "07/04/2003", "09/01/2003", "10/13/2003", "11/11/2003", "11/27/2003", "12/25/2003"]
holidays_list["2004"] = ["01/01/2004", "01/19/2004", "02/16/2004", "05/31/2004", "07/05/2004", "09/06/2004", "10/11/2004", "11/11/2004", "11/25/2004", "12/24/2004", "12/31/2004"]
holidays_list["2005"] = ["01/17/2005", "02/21/2005", "05/30/2005", "07/04/2005", "09/05/2005", "10/10/2005", "11/11/2005", "11/24/2005", "12/26/2005"]
holidays_list["2006"] = ["01/02/2006", "01/16/2006", "02/20/2006", "05/29/2006", "07/04/2006", "09/04/2006", "10/09/2006", "11/10/2006", "11/23/2006", "12/25/2006"]
holidays_list["2007"] = ["01/01/2007", "01/15/2007", "02/19/2007", "05/28/2007", "07/04/2007", "09/03/2007", "10/08/2007" ,"11/11/2007", "11/22/2007", "12/25/2007"]
holidays_list["2008"] = ["01/01/2008", "01/21/2008", "02/18/2008", "05/26/2008", "07/04/2008", "09/01/2008", "10/13/2008" ,"11/11/2008", "11/27/2008", "12/25/2008"]
DIR = "plots/"
YEAR = "2001"

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
    start_date = datetime.strptime(YEAR + "-01-01", "%Y-%m-%d").date()
    end_date = datetime.strptime(YEAR + "-12-31", "%Y-%m-%d").date()
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
    return list(map(lambda x: (x[0][0], float(x[0][1]/(float(x[0][1]+x[1][1]))) ) , zip(airport_list_del, airport_list_nd)))

SFO = calculate_delay_percentage(SFO)
OAK = calculate_delay_percentage(OAK)
JFK = calculate_delay_percentage(JFK)
ORD = calculate_delay_percentage(ORD)
LAX = calculate_delay_percentage(LAX)


# Plotting

ln = geom_vline(x=[datetime.strptime(x, "%m/%d/%Y").date() for x in holidays_list[YEAR]], linetype='dotted')

col1 = "Date"
col2 = "Percentage of flights delayed"

pltd = pd.DataFrame(data=SFO, columns=[col1, col2])
p = ggplot(pltd, aes(col1, col2))\
 + geom_line('jitter', color='#ff0000')\
 + ln + ggtitle("SFO " + YEAR)\
 + theme(x_axis_text = element_text(angle = 30, vjust = 0.5, hjust=1))
p.save(DIR + YEAR + "-" + "SFO" + ".png")


pltd = pd.DataFrame(data=OAK, columns=[col1, col2])
p = ggplot(pltd, aes(col1, col2))\
 + geom_line('jitter', color='#00ff00')\
 + ln + ggtitle("OAK " + YEAR)\
 + theme(x_axis_text = element_text(angle = 30, vjust = 0.5, hjust=1))
p.save(DIR + YEAR + "-" + "OAK" + ".png")

pltd = pd.DataFrame(data=JFK, columns=[col1, col2])
p = ggplot(pltd, aes(col1, col2))\
 + geom_line('jitter', color='#0000ff')\
 + ln + ggtitle("JFK " + YEAR)\
 + theme(x_axis_text = element_text(angle = 30, vjust = 0.5, hjust=1))
p.save(DIR + YEAR + "-" + "JFK" + ".png")

pltd = pd.DataFrame(data=ORD, columns=[col1, col2])
p = ggplot(pltd, aes(col1, col2))\
 + geom_line('jitter', color='#ff00ab')\
 + ln + ggtitle("ORD " + YEAR)\
 + theme(x_axis_text = element_text(angle = 30, vjust = 0.5, hjust=1))
p.save(DIR + YEAR + "-" + "ORD" + ".png")

pltd = pd.DataFrame(data=LAX, columns=[col1, col2])
p = ggplot(pltd, aes(col1, col2))\
 + geom_line('jitter', color='#ab00ff')\
 + ln + ggtitle("LAX " + YEAR)\
 + theme(x_axis_text = element_text(angle = 30, vjust = 0.5, hjust=1))
p.save(DIR + YEAR + "-" + "LAX" + ".png")