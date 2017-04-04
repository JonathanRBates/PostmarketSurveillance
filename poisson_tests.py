# -*- coding: utf-8 -*-
"""

This script is for sample size calculations, originally intended to test the 
feasibility of postmarket surveillance studies.
The sample size calculations are based on Poisson tests, mostly two-sample, 
but a few where the number of controls is fixed before running the tests.
In particular, two Poisson processes with failure rates gamma0, gamma1
are observed for fixed times s0, s1.  The number of outcomes observed X0, X1
are assumed to be Poisson random variables with means gamma0*s0 and gamma1*s1.
(If you don't like this assumption, consider negative binomial tests, etc.)
In the following, we test H0: gamma0=gamma1 against H1: gamma1 > gamma0.

Notation:
r = gamma1/gamma0         the "rate ratio"
d = s1/s0
alpha = significance level
beta = 1 - Power

    alpha = type I error
    beta = type II error

"""

##############################################################################
# Sample Size Estimates Based on Poisson Rate Ratios
##############################################################################


def TwoSamplePoissonTestA(r,d,alpha,beta):
    """
    Shiue and Bain's test    
    
    Return:
        S1, the observation time need to treat
    """
    from scipy import stats
    from numpy import sqrt
    C = (r/d+1.)/(r-1.)**2
    D = sqrt((1.+d*r)/(d+r))
    ka = stats.norm.ppf(1.-alpha)
    kb = stats.norm.ppf(1.-beta)
    lambda0 = C*(D*ka+kb)**2
    return lambda0
        
        
def TwoSamplePoissonTestB(r,d,alpha,beta):
    """
    Huffman's test    
    
    Return:
        S1, the observation time need to treat
    """
    from scipy import stats
    from numpy import sqrt
    C = (d+1.)/(4*d*(sqrt(r)-1.)**2)    
    ka = stats.norm.ppf(1.-alpha)
    kb = stats.norm.ppf(1.-beta)
    lambda0 = C*(ka+kb)**2    
    return lambda0
        
        
def TwoSamplePoissonTestC(r,d,alpha,beta):
    """
    Wu & Makuch's Approximate Test    
    
    Return:
        S1, the observation time need to treat
    """
    from scipy import stats
    from numpy import sqrt
    C = 1./(d*(r-1.)**2)    
    ka = stats.norm.ppf(1.-alpha)
    kb = stats.norm.ppf(1.-beta)
    lambda0 = C*(ka*sqrt(r+d)+kb*sqrt(r))**2    
    return lambda0
    
 
def TwoSamplePoissonTest(r,d,alpha,beta,method='Huffman'):
    """    
    TODO: rewrite to use map on iterable r 
    """
    if method=='Huffman':
        lambda0 = TwoSamplePoissonTestB(r,d,alpha,beta)
    elif method=='WuMakuch':
        lambda0 = TwoSamplePoissonTestC(r,d,alpha,beta)
    elif method=='ShiueBain':
        lambda0 = TwoSamplePoissonTestA(r,d,alpha,beta)
    else:
        raise NameError('That test is not implemented.')
    return lambda0
    
def CalculateSampleSizeTwoSamplePoissonTestTwoSided(r,d,alpha,beta,gamma0,t0,method='Huffman'):
    """
    Estimate sample size necessary to achieve power 1-beta
    when observing t0 years per unit, with baseline Poisson rate of gamma0 events/year
    """
    from numpy import ceil
    lambda0 = [TwoSamplePoissonTest(rr,d,alpha/2.,beta,method=method) for rr in r]   # divide by 2 for two-sided test
    samplesize = [ceil(s/(t0*gamma0)) for s in lambda0]
    return samplesize
    