#!/usr/bin/env python3
import sys
import pandas as pd
t = sys.argv[1]

df = pd.read_csv('Spellman-tidy.csv')
gn_df = df[df.gene == t]
print(gn_df[['time', 'expression']].to_string(index=False, header=False))