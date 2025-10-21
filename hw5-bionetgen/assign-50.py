#!/usr/bin/env python3

import subprocess
import pandas as pd
import os

# BNGL model text
bngl_model = """begin model

begin parameters
    # Initial concentrations
    INH_0   5000
    PG3_0   20000
    ADP_0   10000
    NADH_0  2000
    PGM_0   5000
    ENO_0   5000
    PKM_0   5000
    LDH_0   1000
    # Rate constants
    kf      1e-5
    kr      1e-1
    kcat    1e-1
    kf_inh    1e-3
end parameters

begin molecule types
    INH(i)
    PGM(s,i)
    PG3()
    PG2()
    PEP()
    PYR()
    LAC()
    NAD()
    NADH()
    ADP()
    ENO()
    PKM()
    LDH()
end molecule types

begin species
    INH(i)   INH_0
    PG3()   PG3_0
    ADP()   ADP_0
    NADH()  NADH_0
    PGM(s,i)   PGM_0
    ENO()   ENO_0
    PKM()   PKM_0
    LDH()   LDH_0
end species

begin observables
    Molecules   NAD   NAD()
    Molecules   LAC   LAC()
    Molecules   PYR   PYR()
    Molecules   PEP   PEP()
    Molecules   PG2   PG2()
    Molecules   PG3   PG3()

end observables
    
begin reaction rules
    INH(i) + PGM(i) -> INH(i!1).PGM(i!1) kf_inh
end reaction rules


end model

# Actions
generate_network({overwrite=>1})
simulate_ode({t_end=>100, n_steps=>49})
"""

# Write BNGL file
with open("assign-50.bngl", "w") as f:
    f.write(bngl_model)

# Run BNGL with BioNetGen
subprocess.run(["bionetgen", "run", "-i", "assign-50.bngl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Load simulation results
res = pd.read_csv("assign-50.gdat", sep=r'\s+', comment="#", header=None)

# Assign correct column names
res.columns = ['time', 'NAD', 'LAC', 'PYR', 'PEP', 'PG2', 'PG3']

# Observables of interest
onames= ['NAD','LAC','PYR', 'PEP', 'PG2', 'PG3']
for i in range(0,len(res),7):
    print(' '.join([ f'{o}: {res[o][i]:.0f}' for o in onames]))