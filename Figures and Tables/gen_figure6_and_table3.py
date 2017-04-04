# -*- coding: utf-8 -*-
"""
Generate Figure 6 and Table 3.
"""

fname = 'V1DATA_SAMPLE_SIZE_PROJECT.xlsx'

##############################################################################
# Import Libraries
##############################################################################

# Figure formatting
import matplotlib
matplotlib.rc('font', **{'family':'Times New Roman', 'weight':'normal', 'size':20})
import matplotlib.pyplot as plt

import plot_sample_size_utils as ssutils
 
##############################################################################
# GENERATE FIGURE 4 
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


# PARAMETERS
alphas = [0.05]
beta, d, t0 = 0.20, 1., 2.
gamma0a, labela, colora = 0.039, '3.9 events per 100 person-years', [0.7, 0.7, 0.7]         # (0.0, 0.0, 1.0)
gamma0b, labelb, colorb = 0.061, '6.1 events per 100 person-years', [0.3, 0.3, 0.3]        # (0.0, 0.5, 0.0)
gamma0c, labelc, colorc = 0.126, '12.6 events per 100 person-years', [0.0, 0.0, 0.0]     # (1.0, 0.65, 0.0)

gamma0_ = [gamma0a, gamma0b, gamma0c]
gamma0_label = ['03pt9','06pt1','12pt6']
rateratio_ = [1.05,1.15,1.25,1.5,2.]
rateratio_label = ['1pt05','1pt15','1pt25','1pt50','2pt00']
alpha_ = [0.05]
colorM1_ = [[0.3,0.3,1], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
colorMF_ = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
colorML_ = [[0.7,0.7,1], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
color_ = [colora, colorb, colorc]

##############################################################################
# Individual Everything (FIGURE4)
##############################################################################

import datetime, numpy as np
# import numpy as np

theTable = pd.DataFrame(columns=['baseline event rate', 'rate ratio', 'fraction'])
k=0

for i, rateratio in enumerate(rateratio_):
    
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    fig.set_size_inches(6,12) 
    plt.plot([datetime.date(2005,1,1),datetime.date(2011,1,1)],[len(df),len(df)], ':', lw=6, color='black', label='Total Count')

    dfz, N = ssutils.get_advise_date_dataframe(df,alpha=0.05,gamma0=gamma0a,beta=beta,d=d,t0=t0,rateratio=rateratio)
    t = dfz['Can Advise Date'].values
    t = np.sort(t[~pd.isnull(t)])
    counter = np.linspace(1,len(t),len(t))    
    plt.plot(t, counter, '-', lw=6, color=colora, label=labela)  # was lw=4
    theTable.loc[k,'rate ratio'] = rateratio
    theTable.loc[k,'baseline event rate'] = gamma0a
    try:
        theTable.loc[k,'fraction'] = (dfz['Can Advise Date'] < datetime.date(2011,1,1)).sum()/len(df)
    except:
        theTable.loc[k,'fraction'] = 'nan'
    k=k+1
    
    dfz, N = ssutils.get_advise_date_dataframe(df,alpha=0.05,gamma0=gamma0b,beta=beta,d=d,t0=t0,rateratio=rateratio)
    t = dfz['Can Advise Date'].values
    t = np.sort(t[~pd.isnull(t)])
    counter = np.linspace(1,len(t),len(t))    
    plt.plot(t, counter, '--', lw=6, color=colorb, label=labelb)
    theTable.loc[k,'rate ratio'] = rateratio
    theTable.loc[k,'baseline event rate'] = gamma0b
    try:
        theTable.loc[k,'fraction'] = (dfz['Can Advise Date'] < datetime.date(2011,1,1)).sum()/len(df)
    except:
        theTable.loc[k,'fraction'] = 'nan'
    k=k+1
    
    dfz, N = ssutils.get_advise_date_dataframe(df,alpha=0.05,gamma0=gamma0c,beta=beta,d=d,t0=t0,rateratio=rateratio)
    t = dfz['Can Advise Date'].values
    t = np.sort(t[~pd.isnull(t)])
    counter = np.linspace(1,len(t),len(t))    
    plt.plot(t, counter, '-.', lw=6, color=colorc, label=labelc)
    theTable.loc[k,'rate ratio'] = rateratio
    theTable.loc[k,'baseline event rate'] = gamma0c
    try:
        theTable.loc[k,'fraction'] = (dfz['Can Advise Date'] < datetime.date(2011,1,1)).sum()/len(df)
    except:
        theTable.loc[k,'fraction'] = 'nan'
    k=k+1
    
    ax.set_xlim([datetime.date(2007,1,1),datetime.date(2011,1,1)])
    plt.xticks([datetime.date(a,1,1) for a in range(2008,2011)])
    ax.legend(bbox_to_anchor=(1., -0.1), loc=1, borderaxespad=0., numpoints=1) # placement: under of figure
    plt.ylabel('Individual Count')                
    plt.grid()
   
    if True:
        plt.show()
    else:
        fname = '\\figs\\figure6_rateratio_{}.png'.format(rateratio_label[i])
        plt.savefig(fname,format='png',dpi=600,bbox_inches='tight') 
    

theTable.to_csv('Table3.csv')
