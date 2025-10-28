#!/usr/bin/env python3
import sys
import numpy as np
import prody as prd # have to call fxn w pd.
prd.LOGGER._setverbosity('none')

pdb_name = sys.argv[1]
pdb = prd.parsePDB(pdb_name) # downloads pdb & passes all its info into object 'pdb'
calphas = pdb.select('protein and name CA')

ca_gnm = prd.calcGNM(calphas)
sq_gnm = prd.calcSqFlucts(ca_gnm[0])
ca_anm = prd.calcANM(calphas)
sq_anm = prd.calcSqFlucts(ca_anm[0])

abs_norm_diff = abs((sq_gnm / max(sq_gnm)) - (sq_anm / max(sq_anm)))

top10_i = np.argsort(abs_norm_diff)[-10:][::-1] # slice last 10 elems of ascending order, reverse order of the slice

for i in top10_i:
    print(f'{abs_norm_diff[i]:.3f} {i} {calphas[i].getResname()}{calphas[i].getResnum()}')

