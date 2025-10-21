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
x_log_arr = np.log10(x_arr)
m_lin, b_lin = np.polyfit(x_arr, y_arr, 1)
m_log, b_log = np.polyfit(x_log_arr, y_arr, 1)
y_mid = (y_arr.min() + y_arr.max()) /2
x_lin = (y_mid - b_lin) /m_lin
x_log = 10**((y_mid - b_log) /m_log)

print(f'Linear Fit IC50: {x_lin:.2f}\nLogX-Linear Fit IC50: {x_log:.2f}')