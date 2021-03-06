"""
    noise_dist.py Author T. Shokair 9/11/15
    function takes in a series of power spectra, calculates the mean, and the deviations from the mean. returns single bin deviations as a histogram.
    
"""

import numpy as np
import random
from scipy import signal
import pylab as pl
import matplotlib.pyplot as plt
import pylab as P
import time
import math


def single_bin_dev(p):
    n_ss=len(p)
    p_av=[]
    hist_pts=[]
    sig=[]
    for i in range (0,n_ss):
        pts=len(p[i])
        p_av.append(np.average(p[i]))
        sig.append(np.std(p[i]))
        #print(p_av[i],sig[i])
        for j in range(0,pts):
            hist_pts.append((p[i][j]-p_av[i])/sig[i])
    return hist_pts

def summed_bin_dev(p_tot):
    n_ss=len(p_tot)
    p_av=np.average(p_tot)
    sigma=np.std(p_tot)
    print(p_av,sigma)
    hist_pts=[]
    for i in range (0,n_ss):
        hist_pts.append((p_tot[i]-p_av)/sigma)
    return hist_pts
