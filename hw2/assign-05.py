#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

inputs = sys.argv[1:-1]
output = sys.argv[-1]

for input in inputs:
    lines=[]
    for line in open(input):
        lines.append(line.strip().split(','))
    x=[]; y=[]; y_std=[]
    for l in lines[1:]:
        x.append(int(l[0]))
        y.append(np.mean([int(s) for s in l[1:]]))
        y_std.append(np.std([int(s) for s in l[1:]]))
    plt.errorbar(x,y, yerr=y_std, label=(lines[0][0]))
plt.xlabel('Time (min)')
plt.ylabel('Cell count')
plt.legend(loc='best')
plt.savefig(output)