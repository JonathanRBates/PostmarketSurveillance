# -*- coding: utf-8 -*-
"""
Generate Appendix Table.
Sample size for other significance levels.
"""

import psutil
print(psutil.virtual_memory())

##############################################################################
# Import Libraries
##############################################################################

import pandas as pd

# Sample Size Calculators
from poisson_tests import CalculateSampleSizeTwoSamplePoissonTestTwoSided

##############################################################################
# GENERATE TABLE X
##############################################################################

beta = 0.20
d = 1.
t0 = 2.
gamma0a, labela, colora = 0.039, '3.9 events per 100 person-years', 'blue'
gamma0b, labelb, colorb = 0.061, '6.1 events per 100 person-years', 'green'
gamma0c, labelc, colorc = 0.126, '12.6 events per 100 person-years', 'orange'

gamma0_ = [gamma0a, gamma0b, gamma0c]
rateratio_ = [1.05,1.15,1.25,1.5,2.]

theTable = pd.DataFrame(columns=['baseline event rate', 'rate ratio', 'sample size estimate, 0.1', 'sample size estimate, 0.2'])

k = 0
for i, rateratio in enumerate(rateratio_):
    for j, gamma0 in enumerate(gamma0_):        
        theTable.loc[k,'baseline event rate'] = 100*gamma0
        theTable.loc[k,'rate ratio'] = rateratio
        alpha = 0.1
        N = CalculateSampleSizeTwoSamplePoissonTestTwoSided([rateratio],d,alpha,beta,gamma0,t0,method='Huffman')[0]    
        theTable.loc[k,'sample size estimate, 0.1'] = int(N)
        alpha = 0.2
        N = CalculateSampleSizeTwoSamplePoissonTestTwoSided([rateratio],d,alpha,beta,gamma0,t0,method='Huffman')[0]    
        theTable.loc[k,'sample size estimate, 0.2'] = int(N)
        k=k+1
    
theTable.to_csv('sample_size_paper_TableAppendix_multisig.csv')
