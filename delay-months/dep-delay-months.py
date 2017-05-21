import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt # module for plotting
from matplotlib import interactive, font_manager
from matplotlib import rcParams
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.colors import ListedColormap

import itertools
flt2008=[]

with open('FINAL-output-2001-2008-dep-delay', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    flt2008 = [x for x in reader]
months=[]
delay=[]
for i in xrange(0, len(flt2008)):
    months.append(float(flt2008[i][0]))
    delay.append(float(flt2008[i][1]))
    #if (int(flt2008[i][0])>=-25 and int(flt2008[i][0])<=155):
    #    depdelay[flt2008[i][0]]=float((flt2008[i][1]))/float(totflights)
width=1/1.5
plt.figure(figsize=(12, 6))
plt.bar(months, delay,width ,color="blue")

#flt2008[['Month','DepDelay']].groupby('Month').mean().plot(kind='bar', color=dark2_colors[0])
#plt.xticks(rotation=0)
plt.xlabel('Month of Year')
plt.ylabel('Departure Delay in Min')
plt.title('Average Departure Delay by Month')
plt.show()
