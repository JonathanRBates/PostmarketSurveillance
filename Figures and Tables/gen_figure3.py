# -*- coding: utf-8 -*-
"""
Plot Figure 3.
"""

##############################################################################
# Import Libraries
##############################################################################

import numpy as np

# Figure formatting
import matplotlib
matplotlib.rc('font', **{'family':'Times New Roman', 'weight':'normal', 'size':20})
import matplotlib.pyplot as plt

# Sample Size Calculators
from poisson_tests import CalculateSampleSizeTwoSamplePoissonTestTwoSided

##############################################################################
# GENERATE FIGURE 1
##############################################################################

alphas = [0.05]
beta = 0.20
d = 1.
t0 = 2.
gamma0a, labela, colora = 0.039, '3.9 events per 100 person-years', 'blue'
gamma0b, labelb, colorb = 0.061, '6.1 events per 100 person-years', 'green'
gamma0c, labelc, colorc = 0.126, '12.6 events per 100 person-years', 'orange'

NO_SAVE = False

rateratio = np.linspace(0.50,2.00,200)    # rate ratio 
# rateratio = np.logspace(-1,1,50,base=2)
for alpha in alphas:
    fig = plt.figure()    
    fig.set_size_inches(6,6)  
    ax = fig.add_subplot(111)  
    gamma0 = gamma0a       
    N = CalculateSampleSizeTwoSamplePoissonTestTwoSided(rateratio,d,alpha,beta,gamma0,t0,method='Huffman')    
    plt.plot(rateratio, N, '-', lw=4, color=colora, label=labela)  
    gamma0 = gamma0b     
    N = CalculateSampleSizeTwoSamplePoissonTestTwoSided(rateratio,d,alpha,beta,gamma0,t0,method='Huffman')
    plt.plot(rateratio, N, '--', lw=4, color=colorb, label=labelb)  
    gamma0 = gamma0c     
    N = CalculateSampleSizeTwoSamplePoissonTestTwoSided(rateratio,d,alpha,beta,gamma0,t0,method='Huffman')
    # plt.plot(rateratio, N, 'o', lw=4, color=colorc, markersize=8, markerfacecolor=colorc, markeredgecolor=colorc, label=labelc)  
    plt.plot(rateratio, N, '-.', lw=4, markersize=8, color=colorc, markerfacecolor=colorc, markeredgecolor=colorc, label=labelc)   
    plt.xlabel('Rate Ratio') 
    plt.ylabel('Sample Size')
    # ax.tick_params(labelsize=12)  
    ax.set_xlim([0.50,2.00])
    ax.set_ylim([0.,5000.])
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0., numpoints=3)    # placement: right of figure
    # ax.legend(bbox_to_anchor=(1., -0.25), loc=1, borderaxespad=0.) 
    if NO_SAVE:
        plt.show()
    else:    
        astring = str(alpha).split('.',1)[1]
        fname = 'figure3_alpha{}.png'.format(astring)    
        plt.savefig(fname,format='png',dpi=600,bbox_inches='tight')     
        # plt.savefig(fname,format='eps',dpi=600, bbox_inches='tight')    
