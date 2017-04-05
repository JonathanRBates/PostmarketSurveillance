# -*- coding: utf-8 -*-
"""
Generate Table 2.
"""

fname = 'V1DATA_SAMPLE_SIZE_PROJECT.xlsx'

##############################################################################
# Import Libraries
##############################################################################

import plot_sample_size_utils as ssutils
 
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


# PARAMETERS
beta, d, t0 = 0.20, 1., 2.
gamma0a, labela, colora = 0.039, '3.9 events per 100 person-years', 'blue'         # (0.0, 0.0, 1.0)
gamma0b, labelb, colorb = 0.061, '6.1 events per 100 person-years', 'green'        # (0.0, 0.5, 0.0)
gamma0c, labelc, colorc = 0.126, '12.6 events per 100 person-years', 'orange'      # (1.0, 0.65, 0.0)

gamma0_ = [gamma0a, gamma0b, gamma0c]
gamma0_label = ['03pt9','06pt1','12pt6']
rateratio_ = [1.05,1.15,1.25,1.5,2.]
alpha_ = [0.05]

##############################################################################
# Table 2
##############################################################################

import numpy as np

theTable = pd.DataFrame(columns=['baseline event rate', 'model event rate', 'rate ratio', 'sample size estimate', 'fraction reaching sample size'])

k = 0
for i, rateratio in enumerate(rateratio_):
    for j, gamma0 in enumerate(gamma0_):
        for alpha in alpha_:           
            dfx, N = ssutils.get_time_to_sample_size_accumulation_dataframe(df,alpha,gamma0,beta=0.20,d=1.,t0=2.,rateratio=rateratio)
            theTable.loc[k,'baseline event rate'] = 100*gamma0
            theTable.loc[k,'model event rate'] = 100*gamma0*rateratio
            theTable.loc[k,'rate ratio'] = rateratio
            theTable.loc[k,'sample size estimate'] = int(N)
            theTable.loc[k,'fraction reaching sample size'] = np.sum(dfx['Sample Size Accumulation Differential'] < 6.5) \
                                                               / dfx['Sample Size Accumulation Differential'].shape[0]
            x = dfx[dfx['Sample Size Accumulation Differential'] < 6.5]['Sample Size Accumulation Differential'].values
            print(np.median(x))
            print(np.percentile(x,25))
            print(np.percentile(x,50))
            print(np.percentile(x,75))                                                   
            k=k+1
    
theTable.to_csv('table.csv')         
            
            