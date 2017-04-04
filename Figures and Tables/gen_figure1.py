# -*- coding: utf-8 -*-
"""
Figure 1.

Utilization

"""

fname = 'V1DATA_SAMPLE_SIZE_PROJECT.xlsx'


##############################################################################
# Import Libraries
##############################################################################

# Figure formatting
import matplotlib
matplotlib.rc('font', **{'family':'Times New Roman', 'weight':'normal', 'size':20})
import matplotlib.pyplot as plt

##############################################################################
# GENERATE FIGURE 2 (ALL STRATA)
##############################################################################
# 0. load data
import pandas as pd

try:
    print(df.dtypes)
except NameError:    
    df = pd.read_excel(fname)        # see loadsasdata.py for other possible data reading methods; had trouble with datetime dtype in read_csv 
    df.drop(df[df['DEVICE VOLUME >= 20'] == 0].index, inplace=True)   # Remove devices below 20 threshold
    print(df.dtypes)
    print('''There are a total of N={} implants meeting the inclusion criteria.
    The number of distinct models is {}'''.format(len(df),len(df['ICD Implant Device ID'].unique())))

import matplotlib.dates as mdates

fig = plt.figure()
ax = fig.add_subplot(111)    
fig.set_size_inches(6,4) 
ax.hist(df['Date of Implant'].values, bins=10, lw=2, edgecolor=[0.7,0.7,0.7], fc=[0.7,0.7,0.7], cumulative=False, normed=0)
plt.xticks(rotation=-45)
# fig.autofmt_xdate()
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %m %Y'))
plt.ylabel('Number of Implants')    
if True:
        plt.show()
else:
    fname = 'temp.png'
    plt.savefig(fname,format='png',dpi=600,bbox_inches='tight') 
