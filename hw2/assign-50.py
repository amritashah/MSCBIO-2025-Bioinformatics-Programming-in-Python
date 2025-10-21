#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
if len(sys.argv)!=3:
    print('error: wrong number of args')
input = sys.argv[1]
output = sys.argv[2]

lines = []
for line in open(input):
    lines.append(line.strip().split(','))
x=[]
y=[]
for l in lines[1:]:
    x.append(int(l[0]))
    y.append(int(l[1]))

plt.plot(x,y)
plt.savefig(output)