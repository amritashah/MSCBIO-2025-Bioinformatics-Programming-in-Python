#!/usr/bin/env python3
import numpy as np
import scipy as sp
import sys
infile = sys.argv[1]

arr = np.loadtxt(infile, dtype=np.float64)
x_arr = np.zeros(len(arr))
y_arr = np.zeros(len(arr))
for i in range(len(arr)):
    x_arr[i] = arr[i][0]
    y_arr[i] = arr[i][1]
y_mid = (y_arr.min() + y_arr.max()) /2
m_lin, b_lin = np.polyfit(x_arr, y_arr, 1)
x_lin = (y_mid - b_lin) /m_lin

x_log_arr = np.log10(x_arr)
m_log, b_log = np.polyfit(x_log_arr, y_arr, 1)
x_log = 10**((y_mid - b_log) /m_log)

def sig(x, Bottom, Top, LogIC50):
    return Bottom + ((Top-Bottom)/(1+ (10**(LogIC50-x))))
popt, pcov = sp.optimize.curve_fit(sig, x_log_arr, y_arr)
Bottom, Top, LogIC50 = popt
IC50 = 10**LogIC50
print(f'Linear Fit IC50: {x_lin:.2f}\nLogX-Linear Fit IC50: {x_log:.2f}\nSigmoid Fit Fixed Slope IC50: {IC50:.2f}')