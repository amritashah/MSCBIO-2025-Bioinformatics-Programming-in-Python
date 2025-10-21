#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
inputs = sys.argv[1:-1]
output = sys.argv[-1]

for input in inputs:
    lines=[]
    for line in open(input):
        lines.append(line.strip().split(','))
    x=[]; y=[]
    for l in lines[1:]:
        x.append(int(l[0]))
        y.append(int(l[1]))
    plt.plot(x,y, label=(lines[0][0]))
plt.xlabel('Time (min)')
plt.ylabel('Cell count')
plt.legend(loc='best')
plt.savefig(output)