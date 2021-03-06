"""
    main.py Author T. Shokair 9/11/15
    This main function reads in a list of power spectra, calls a function to process them, coadds each processed spectra, and finally plots a grand spectrum.
    updated 10/8/15 to fix some bugs with coadding and incorporate histogram plotting
    updated 2/10/16 to add snr spectra as well as to take some of the logic out of main and move it to separte programs.
    
"""
import numpy as np
import random
import math
from scipy import signal
from scipy import optimize
from scipy.stats import norm
import pylab as pl
import matplotlib.pyplot as plt
import time

from pad_list import find_pad_param
from pad_list import pad_l
from six_bin_average import six_bin_av
import pickle
from fit_gauss import fit
from count_contributing_bins import count_f_per_bin

from calc_weights import calc_weight_ijk
from pad_list import find_pad_param
from pad_list import pad_l
from make_plots import plot_everything

from call_process_fn import call_process
class ReturnProcessedSorted(object):
    def __init__(self, f,p,f0,fs,delta_ij,sig_sq_ij):
        self.f = f
        self.f0 = f0
        self.fs = fs
        self.delta_ij =delta_ij
        self.sig_sq_ij = sig_sq_ij
        self.p = p
def processed_streams(l):
    return ReturnProcessedSorted(l[0],l[1],l[2],l[3],l[4],l[5])



#get the processed streams
p_array=call_process("p_spectra.txt")
f=processed_streams(p_array).f
f0=processed_streams(p_array).f0
fs=processed_streams(p_array).fs
p=processed_streams(p_array).p
sig_sq_ij=processed_streams(p_array).sig_sq_ij
delta_ij=processed_streams(p_array).delta_ij
n_ss=len(f)

#pad the streams with zeros for co-adding
pad_param=find_pad_param(f,fs[0])
p_pad=[]
delta_ij_pad=[]
sig_sq_ij_pad=[]
for i in range(0,n_ss):
    p_pad.append(pad_l(f[i],pad_param,p[i]))
    delta_ij_pad.append(pad_l(f[i],pad_param,delta_ij[i]))
    sig_sq_ij_pad.append(pad_l(f[i],pad_param,sig_sq_ij[i]))
#find the weighting factors
w_ijk=calc_weight_ijk(sig_sq_ij_pad)
w_ij=np.transpose(w_ijk)
#weight the delta_ij and sigma_sq_ij padded streams
delta_ij_pad_w=[]
sig_sq_ij_pad_w=[]
for k in range(0,n_ss):
    delta_ij_pad_w.append([a*b for a,b in zip(delta_ij_pad[k],w_ij[k])])
    sig_sq_ij_pad_w.append([a*b**2 for a,b in zip(sig_sq_ij_pad[k],w_ij[k])])
#sum the powers and offset the subspectra for plotting
#offset_snr are offset spectra, offset simply for plotting purposes.
snr_c=[a/math.sqrt(b) if b!=0 else b for a,b in zip(delta_ij_pad_w[0],sig_sq_ij_pad_w[0])]
offset_snr=[]
offset_dij=[]
offset_sij=[]
offset=10
offset_snr.append([a+offset for a in snr_c])
offset_dij.append([a+offset/100 for a in delta_ij_pad_w[0]])
offset_sij.append([a+offset/100 for a in sig_sq_ij_pad_w[0]])
for i in range (1,n_ss):
    snr=[a/math.sqrt(b) if b!=0 else b for a,b in zip(delta_ij_pad_w[i],sig_sq_ij_pad_w[i])]
    offset_snr.append([a+offset*(i%19+1) for a in snr])
    offset_dij.append([a+offset/100*(i%19+1) for a in delta_ij_pad_w[i]])
    offset_sij.append([a+offset/100*(i%19+1) for a in sig_sq_ij_pad_w[i]])
    snr_c=[a+b for a,b in zip(snr_c,snr)]
    del snr


#make the plots
plot_everything(n_ss,f,f0,snr_c,offset_snr,p,w_ij,offset_dij)




