# -*- coding: utf-8 -*-
"""

"""


fname = 'Z:\\NCDR\\ICD\\cp\\For Jon\\V1DATA_SAMPLE_SIZE_PROJECT.xlsx'



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
import pandas as pd, numpy as np

try:
    print(df.dtypes)
except NameError:    
    df = pd.read_excel(fname)        # see loadsasdata.py for other possible data reading methods; had trouble with datetime dtype in read_csv 
    df.drop(df[df['DEVICE VOLUME >= 20'] == 0].index, inplace=True)   # Remove devices below 20 threshold
    print(df.dtypes)
    print('''There are a total of N={} implants meeting the inclusion criteria.
    The number of distinct models is {}'''.format(len(df),len(df['ICD Implant Device ID'].unique())))

x = df.groupby('ICD Implant Device ID').size().values
x = np.sort(x)[::-1]

fig = plt.figure()
ax = fig.add_subplot(111)    
fig.set_size_inches(6,4) 
ax.bar(np.linspace(1,141,141), x, lw=2, edgecolor=[0.7,0.7,0.7], fc=[0.7,0.7,0.7])
plt.ylim([0,65000])
plt.xlim([0,141])
plt.ylabel('Number of Implants') 
plt.xlabel('Model') 
if True:
    plt.show()
else:
    fname = 'figure2_utilization_distribution.png'
    plt.savefig(fname,format='png',dpi=600,bbox_inches='tight') 

print(np.subtract(*np.percentile(x, [75, 25])))
print(np.median(x))
print(np.percentile(x,50))
