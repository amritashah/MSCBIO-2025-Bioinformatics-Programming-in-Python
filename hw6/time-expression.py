#!/usr/bin/env python3
import sys
import pandas as pd
t = sys.argv[1]
df = pd.read_csv('Spellman-tidy.csv')

t_df = df[df.time == int(t)]
print(t_df['expression'].mean())