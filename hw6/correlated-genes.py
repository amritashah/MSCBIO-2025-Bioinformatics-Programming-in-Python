#!/usr/bin/env python3
import sys
import pandas as pd
gn = sys.argv[1]
df = pd.read_csv('Spellman-tidy.csv')

piv = df.pivot(index='time', columns='gene', values='expression')
corr = piv.corr()
gc = list(corr[gn].drop(gn).sort_values(ascending=False).head(5).index)
for g in gc:
    print(g)
