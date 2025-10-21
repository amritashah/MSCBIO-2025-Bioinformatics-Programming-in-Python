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
slope, intercept = np.polyfit(x_arr, y_arr, 1)
y_mid = (y_arr.min() + y_arr.max()) /2
x = (y_mid - intercept) /slope

print(f'Linear Fit IC50: {x:.2f}')

    