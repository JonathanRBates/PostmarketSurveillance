# -*- coding: utf-8 -*-
"""
Generate Figure 4
"""

fname = 'Z:\\NCDR\\ICD\\cp\\For Jon\\V1DATA_SAMPLE_SIZE_PROJECT.xlsx'    

##############################################################################
# Import Libraries
##############################################################################

# Figure formatting
import matplotlib
matplotlib.rc('font', **{'family':'Times New Roman', 'weight':'normal', 'size':20})
import matplotlib.pyplot as plt

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
alphas = [0.05]
beta, d, t0 = 0.20, 1., 2.
gamma0a, labela, colora = 0.039, '3.9 events per 100 person-years', 'blue'         # (0.0, 0.0, 1.0)
gamma0b, labelb, colorb = 0.061, '6.1 events per 100 person-years', 'green'        # (0.0, 0.5, 0.0)
gamma0c, labelc, colorc = 0.126, '12.6 events per 100 person-years', 'orange'      # (1.0, 0.65, 0.0)

gamma0_ = [gamma0a, gamma0b, gamma0c]
gamma0_label = ['03pt9','06pt1','12pt6']
# rateratio_ = [1.05,1.15,1.25,1.5,2.]
# rateratio_label = ['1pt05','1pt15','1pt25','1pt50','2pt00']
# alpha_ = [0.05]
colorM1_ = [[0.3,0.3,1], [0.5, 0.0, 0.0]]
colorMF_ = [[0.0, 0.0, 1.0], [0.5, 0.0, 0.0]]
colorML_ = [[0.7,0.7,1], [0.5, 0.0, 0.0]]


color_scheme = 'grey'

for j, gamma0 in enumerate(gamma0_):         
    dfx, N = ssutils.get_time_to_sample_size_accumulation_dataframe(df,alpha=0.05,gamma0=gamma0,beta=beta,d=d,t0=t0,rateratio=1.25)
    #
    # ssutils.plot_full_time_to_sample_size_accumulation(dfx)
    #    
    import datetime
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
        
        if color_scheme == 'redblue':
        
            # Accumulated sample size marker
            if pd.isnull(tN):  
                plt.plot([t1, datetime.datetime.today()], [y, y], '-', lw=3, color=colorML_[1], label='', alpha=0.5)    
                plt.plot(t1, y, 'x', lw=1, mew=2, markersize=8, markerfacecolor=colorM1_[1], markeredgecolor=colorM1_[1], label=label_1)
                # plt.plot(tN, y, 's', lw=1, markersize=8, markerfacecolor='red', markeredgecolor='red', label='')  # this doesn't plot anything ;)
            else:
                # Line joining markers
                plt.plot([t1, tN], [y, y], '-', lw=3, color=colorML_[0], label='', alpha=0.5)
                plt.plot(t1, y, 'x', lw=1, mew=2, markersize=8, markerfacecolor=colorM1_[0], markeredgecolor=colorM1_[0], label=label_1)
                plt.plot(tN, y, 's', lw=1, markersize=8, markerfacecolor=colorMF_[0], markeredgecolor=colorMF_[0], label=label_N)        
                # plt.plot(tN, y, 's', lw=2, markersize=8, markerfacecolor='blue', markeredgecolor='blue', label=label_N)  
                
        elif color_scheme == 'grey':       
            
            # Accumulated sample size marker
            if pd.isnull(tN):  
                plt.plot([t1, datetime.datetime.today()], [y, y], '-', lw=3, color=[0.7,0.7,0.7], label='', alpha=0.5)    
                plt.plot(t1, y, 'x', lw=1, mew=2, markersize=8, markerfacecolor=[0.7,0.7,0.7], markeredgecolor=[0.7,0.7,0.7], label=label_1)                
            else:
                # Line joining markers
                plt.plot([t1, tN], [y, y], '-', lw=3, color=[0.7,0.7,0.7], label='', alpha=0.5)
                plt.plot(t1, y, 'x', lw=1, mew=2, markersize=8, markerfacecolor=[0.7,0.7,0.7], markeredgecolor=[0.7,0.7,0.7], label=label_1)
                plt.plot(tN, y, 's', lw=1, markersize=8, markerfacecolor=[0.1,0.1,0.1], markeredgecolor=[0.1,0.1,0.1], label=label_N)        
                # plt.plot(tN, y, 's', lw=2, markersize=8, markerfacecolor='blue', markeredgecolor='blue', label=label_N)  
                
    ax.set_xlim([datetime.date(2005,1,1),datetime.date(2011,1,1)])
    plt.xticks([datetime.date(a,1,1) for a in range(2006,2011)])
    # ax.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0., numpoints=1)    # placement: right of figure
    ax.legend(bbox_to_anchor=(1., -0.1), loc=1, borderaxespad=0., numpoints=1) # placement: under of figure
    plt.ylim([0,142])
    plt.ylabel('Model')                
    plt.grid()          
    if True:
        plt.show()
    else:
        fname = 'figure4_timeline_gamma0_{}.png'.format(gamma0_label[j])
        plt.savefig(fname,format='png',dpi=600,bbox_inches='tight') 
    

