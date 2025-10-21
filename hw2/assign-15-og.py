#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
if len(sys.argv)!=4:
    print('error: wrong number of args')
input1 = sys.argv[1]
input2 = sys.argv[2]
output = sys.argv[-1]

lines1 = []; lines2 = []
for line in open(input1): 
    lines1.append(line.strip().split(',')) 
for line in open(input2): 
    lines2.append(line.strip().split(',')) 
x1=[]; y1=[]; x2=[]; y2=[] 
for l in lines1[1:]: 
    x1.append(int(l[0])) 
    y1.append(int(l[1])) 
for l in lines2[1:]: 
    x2.append(int(l[0])) 
    y2.append(int(l[1]))
plt.plot(x1,y1, label=(lines1[0][0]))
plt.plot(x2,y2, label=(lines2[0][0]))
plt.xlabel('Time (min)')
plt.ylabel('Cell count')
plt.legend(loc='best')
plt.savefig(output)