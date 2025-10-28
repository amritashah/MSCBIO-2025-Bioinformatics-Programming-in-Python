#!/usr/bin/env python3
import sys
import prody as prd # have to call fxn w pd.
prd.LOGGER._setverbosity('none')

pdb_name = sys.argv[1]
pdb = prd.parsePDB(pdb_name) # downloads pdb & passes all its info into object 'pdb'
calphas = pdb.select('protein and name CA')

ca_gnm = prd.calcGNM(calphas)
sq_gnm = prd.calcSqFlucts(ca_gnm[0])

ca_anm = prd.calcANM(calphas)
sq_anm = prd.calcSqFlucts(ca_anm[0])

abs_diff = abs(sq_gnm-sq_anm)

abs_norm_diff = abs((sq_gnm / max(sq_gnm)) - (sq_anm / max(sq_anm)))

print(f'Max Abs Difference: {max(abs_diff):.3f}')
print(f'Max Abs Norm Difference: {max(abs_norm_diff):.3f}')