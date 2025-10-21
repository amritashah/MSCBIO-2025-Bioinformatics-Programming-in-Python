#!/usr/bin/env python3

import pandas as pd
df = pd.read_csv('Spellman.csv')
df.rename(columns={'time': 'gene'}, inplace=True)
df = pd.melt(df, id_vars=['gene'], var_name = 'time', value_name = 'expression')
df.to_csv('Spellman-tidy.csv', index=False)
