# -*- coding: utf-8 -*-
"""
Figure 5
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
rateratio_ = [1.05,1.15,1.25,1.5,2.]
rateratio_label = ['1pt05','1pt15','1pt25','1pt50','2pt00']
alpha_ = [0.05]
colorM1_ = [[0.3,0.3,1], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
colorMF_ = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
colorML_ = [[0.7,0.7,1], [0.0, 0.5, 0.0], [1.0, 0.65, 0.0]]
color_ = [colora, colorb, colorc]

##############################################################################
# Individual Everything (FIGURE3)
##############################################################################

import matplotlib.gridspec as gridspec
import numpy as np

for i, rateratio in enumerate(rateratio_):
    for j, gamma0 in enumerate(gamma0_):
        for alpha in alpha_:     
            
            dfx, N = ssutils.get_time_to_sample_size_accumulation_dataframe(df,alpha,gamma0,beta=0.20,d=1.,t0=2.,rateratio=rateratio)
            
            just_get_percentages = False
            if just_get_percentages:
                print('rr={}, baseline={}, frac={}'.format(rateratio,
                                                           gamma0,
                                                           np.sum(dfx['Sample Size Accumulation Differential'] >= 6.5)/
                                                           dfx['Sample Size Accumulation Differential'].shape[0]))
                continue        
            
            n = 12; m = 1;
            gs = gridspec.GridSpec(1,2, width_ratios = [n,m])
            
            plt.figure(figsize=(6,4))
            
            ax = plt.subplot(gs[0,0])
            ax2 = plt.subplot(gs[0,1], sharey = ax)
            plt.setp(ax2.get_yticklabels(), visible=False)
            plt.subplots_adjust(wspace = 0.25)
            normed = 0                        
            ax.hist(np.clip(dfx['Sample Size Accumulation Differential'],a_min=0.,a_max=6.5), np.linspace(0,7.5,16), lw=2, edgecolor=colorMF_[0], fc=colorMF_[0], range=(0,10), cumulative=False, normed=normed)
            ax2.hist(np.clip(dfx['Sample Size Accumulation Differential'],a_min=0.,a_max=6.5), np.linspace(0,7.5,16), lw=2, edgecolor=colorMF_[0], fc=colorMF_[0], range=(0,10), cumulative=False, normed=normed)
            ax.set_xlim([0,6.])
            ax.set_ylim([0,141.])
            ax2.set_xlim([6.5,7.])
            
            # hide the spines between ax and ax2
            ax.spines['right'].set_visible(False)
            ax2.spines['left'].set_visible(False)
            ax.yaxis.tick_left()
            ax.tick_params(labeltop='off') # don't put tick labels at the top
            ax2.yaxis.tick_right()
            ax2.tick_params(labelright='off') # don't put tick labels at the top
            
            ax.set_xticks([0,1,2,3,4,5,6])
            ax2.set_xticks([6.5,7])
            ax2.set_xticklabels(['$+\infty$'])
            ax.set_xlabel('Time to Sample Size Accumulation (Years)',x=.6)
            # fig.text(0.075, 0.5, "this", rotation="horizontal", va="center")
            ds = .015 # how big to make the diagonal lines in axes coordinates
            # arguments to pass plot, just so we don't keep repeating them
            kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
            
            on = (n+m)/n; om = (n+m)/m;
            ax.plot((1-ds*on,1+ds*on),(-ds,ds), **kwargs) # bottom-left diagonal
            ax.plot((1-ds*on,1+ds*on),(1-ds,1+ds), **kwargs) # top-left diagonal
            kwargs.update(transform=ax2.transAxes) # switch to the bottom axes
            ax2.plot((-ds*om,ds*om),(-ds,ds), **kwargs) # bottom-right diagonal
            ax2.plot((-ds*om,ds*om),(1-ds,1+ds), **kwargs) # top-right diagonal  
            if True:
                plt.show()
            else:
                fname = 'figure5_rateratio_{}_gamma0_{}.png'.format(rateratio_label[i],gamma0_label[j])
                plt.savefig(fname,format='png',dpi=600,bbox_inches='tight') 
           
            