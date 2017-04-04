# -*- coding: utf-8 -*-
"""

"""

##############################################################################
# Import Libraries
##############################################################################
import pandas as pd
import datetime
import numpy as np
import matplotlib
matplotlib.rc('font', **{'family':'Times New Roman', 'weight':'normal', 'size':20})
import matplotlib.pyplot as plt

##############################################################################
# 
##############################################################################

def get_time_to_sample_size_accumulation_dataframe(df, alpha=0.05,gamma0=0.061, beta=0.20, d=1., t0=2., rateratio=1.25):
    """
    
    """
    from poisson_tests import CalculateSampleSizeTwoSamplePoissonTestTwoSided
    
    # 1. sort implant dates per device
    df.sort_values('Date of Implant', inplace=True) 
    # 2. For sample size N, get date of Nth implant; store as Nan if never reaches
    N = CalculateSampleSizeTwoSamplePoissonTestTwoSided([rateratio],d,alpha,beta,gamma0,t0,method='Huffman')
    N = int(N[0])
    print('N = {}'.format(N))
    # Note: 
    # "Note that groupby will preserve the order in which observations are sorted within each group"
    # source: http://pandas.pydata.org/pandas-docs/stable/groupby.html
    df_t1 = df.groupby('ICD Implant Device ID', as_index=False).nth(0)
    df_tN = df[['ICD Implant Device ID', 'Date of Implant']].groupby('ICD Implant Device ID', as_index=False).nth(N-1)
    dfx = pd.merge(df_t1, df_tN, on='ICD Implant Device ID', how='left')
    dfx=dfx.rename(columns={'Date of Implant_x':'Date of 1st Implant', 'Date of Implant_y':'Date of Nth Implant'})    
    #
    dfx['Analysis Date'] = dfx['Date of Nth Implant'] + datetime.timedelta(days=365.25*t0)
    dfx['Analysis Date Differential'] = (dfx['Analysis Date'] - dfx['Date of 1st Implant']).dt.days/365.25   # in years
    dfx['Analysis Date Differential'] = dfx['Analysis Date Differential'].fillna(100.)   # what to do when not enough sample size? 100 years= infinity
    #
    dfx['Sample Size Accumulation Differential'] = (dfx['Date of Nth Implant'] - dfx['Date of 1st Implant']).dt.days/365.25   # in years
    dfx['Sample Size Accumulation Differential'] = dfx['Sample Size Accumulation Differential'].fillna(100.)   # what to do when not enough sample size? 100 years= infinity
    #
    return dfx, N
    
##############################################################################
# 
##############################################################################
  
def get_advise_date_dataframe(df, alpha=0.05,gamma0=0.061, beta=0.20, d=1., t0=2., rateratio=1.25):
    """
    The 'Can Advise Date'
    is the date at which the individual can be advised regarding the device.
    It is t0 = 2 years after the sample size accumulation date for the device
    and after he receives the implant.
    """
    from poisson_tests import CalculateSampleSizeTwoSamplePoissonTestTwoSided
    
    # 1. sort implant dates per device
    df.sort_values('Date of Implant', inplace=True) 
    # 2. For sample size N, get date of Nth implant; store as Nan if never reaches
    N = CalculateSampleSizeTwoSamplePoissonTestTwoSided([rateratio],d,alpha,beta,gamma0,t0,method='Huffman')
    N = int(N[0])
    print('N = {}'.format(N))  
    df_tN = df[['ICD Implant Device ID', 'Date of Implant']].groupby('ICD Implant Device ID', as_index=False).nth(N-1)
    dfz = pd.merge(df, df_tN, on='ICD Implant Device ID', how='left')
    dfz=dfz.rename(columns={'Date of Implant_x':'Date of Implant', 'Date of Implant_y':'Date of Sample Size Accumulation'})    
    dfz['Analysis Date'] = dfz['Date of Sample Size Accumulation'] + datetime.timedelta(days=365.25*t0)
    dfz['Can Advise Date'] =  dfz[['Analysis Date','Date of Implant']].dropna().max(axis=1)
    # print(dfz[['Analysis Date','Date of Implant','Can Advise Date']].head(n=40))
    return dfz, N
    
    
##############################################################################
# 
##############################################################################

def plot_full_time_to_sample_size_accumulation(dfx):
    """
    dfx : dataframe returned by get_time_to_sample_size_accumulation_dataframe()
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    fig.set_size_inches(6,12) 
    for i in range(dfx.shape[0]):      
        t1 = dfx.loc[i,'Date of 1st Implant'].date()
        tN = dfx.loc[i,'Date of Nth Implant'].date()
        tA = dfx.loc[i,'Analysis Date'].date()
        y = i
        if i==0:
            label_1 = 'First Implant'
            label_N = 'Sample Size Accumulation' # 'Nth Implant'
            label_A = 'Analysis Time'
        else:
            label_1, label_N, label_A = '', '', ''       
        if pd.isnull(tN): 
            plt.plot(t1, y, '|', lw=1, markersize=8, markerfacecolor='red', markeredgecolor='red', label=label_1)
            plt.plot(tN, y, 's', lw=1, markersize=8, markerfacecolor='red', markeredgecolor='red', label='')  # this doesn't plot anything ;)
        else:
            plt.plot(t1, y, '|', lw=1, markersize=8, markerfacecolor='blue', markeredgecolor='blue', label=label_1)
            plt.plot(tN, y, 's', lw=1, markersize=8, markerfacecolor='blue', markeredgecolor='blue', label=label_N)
            plt.plot([t1, tN], [y, y], '-', lw=4, color='blue', label='')
            # plt.plot(tN, y, 's', lw=2, markersize=8, markerfacecolor='blue', markeredgecolor='blue', label=label_N)                
    ax.set_xlim([datetime.date(2005,1,1),datetime.date(2011,1,1)])
    plt.xticks([datetime.date(a,1,1) for a in range(2006,2011)])
    # ax.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0., numpoints=1)    # placement: right of figure
    ax.legend(bbox_to_anchor=(1., -0.1), loc=1, borderaxespad=0., numpoints=1) # placement: under of figure
    plt.ylim([0,142])
    plt.ylabel('Model')
    
##############################################################################
# 
##############################################################################
    
def plot_hist_time_to_sample_size_accumulation(dfx, cumulative=False):
    """
    dfx : dataframe returned by get_time_to_sample_size_accumulation_dataframe()
    """ 
    fig = plt.figure()    
    fig.set_size_inches(6,6)  
    fig.add_subplot(111)     
    if cumulative:
        plt.hist(np.clip(dfx['Analysis Date Differential'],a_min=0.,a_max=10.), 20, lw=2, edgecolor='blue', fc=(0, 0, 1, 0.3), range=(0,10), cumulative=True, normed=1, histtype='stepfilled')
    else:
        plt.hist(np.clip(dfx['Analysis Date Differential'],a_min=0.,a_max=10.), 20, lw=2, edgecolor='blue', fc=(0, 0, 1, 0.3), range=(0,10))
    plt.xlabel('time to sample size accumulation (in years)') 
    plt.xticks([a for a in range(0,9)])
    plt.ylabel('')
    # return plt
    