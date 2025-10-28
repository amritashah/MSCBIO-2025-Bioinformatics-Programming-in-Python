#!/usr/bin/env python3
import sys
import prody as prd # have to call fxn w pd.
prd.LOGGER._setverbosity('none')

pdb_name = sys.argv[1]
pdb = prd.parsePDB(pdb_name) # downloads pdb & passes all its info into object 'pdb'
calphas = pdb.select('protein and name CA')

ca_anm = prd.calcANM(calphas)
sq_flucts = prd.calcSqFlucts(ca_anm[0])

print(f'Max ANM SqFluct: {max(sq_flucts):.3f}')