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
    INH()
    PGM()
    PG3()
    PG2()
    PEP()
    PYR()
    LAC()
    NAD()
    NADH()
    ADP()
    ATP()
    ENO()
    PKM()
    LDH()
    PGM_PG3()
    INH_PGM()
    ENO_PG2() 
    PKM_PEP()
    PKM_ADP()
    PKM_PEP_ADP()
    LDH_PYR()
    LDH_NADH()
    LDH_PYR_NADH()
    LDH_LAC()
    LDH_NAD()
    LDH_LAC_NAD()


end molecule types

begin species
    INH()   INH_0
    PG3()   PG3_0
    ADP()   ADP_0
    NADH()  NADH_0
    PGM()   PGM_0
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
    INH() + PGM() <-> INH_PGM() kf_inh, kr

    PGM() + PG3() <-> PGM_PG3() kf, kr
    PGM_PG3() -> PGM() + PG2() kcat

    PG2() + ENO() <-> ENO_PG2() kf, kr
    ENO_PG2() -> ENO() + PEP() kcat

    
    PEP() + PKM() <-> PKM_PEP() kf, kr
    ADP() + PKM() <-> PKM_ADP() kf, kr

    PEP() + PKM_ADP() <-> PKM_PEP_ADP() kf, kr
    ADP() + PKM_PEP() <-> PKM_PEP_ADP() kf, kr

    PKM_PEP_ADP() -> PYR() + ATP() + PKM() kcat

    
    PYR() + LDH() <-> LDH_PYR() kf, kr
    NADH() + LDH() <-> LDH_NADH() kf, kr

    PYR() + LDH_NADH() <-> LDH_PYR_NADH() kf, kr
    NADH() + LDH_PYR() <-> LDH_PYR_NADH() kf, kr

    LDH_PYR_NADH() -> LAC() + NAD() + LDH() kcat

    
    PYR() + LDH() <-> LDH_PYR() kf, kr
    NADH() + LDH() <-> LDH_NADH() kf, kr
    LAC() + LDH() <-> LDH_LAC() kf, kr
    NAD() + LDH() <-> LDH_NAD() kf, kr

    PYR() + LDH_NADH() <-> LDH_PYR_NADH() kf, kr
    NADH() + LDH_PYR() <-> LDH_PYR_NADH() kf, kr
    LAC() + LDH_NAD() <-> LDH_LAC_NAD() kf, kr
    NAD() + LDH_LAC() <-> LDH_LAC_NAD() kf, kr


    LDH_LAC_NAD() -> PYR() + NADH() + LDH() kcat

    LDH_PYR_NADH() -> LDH_LAC_NAD() kcat
    LDH_LAC_NAD() -> LDH_LAC() + NAD() kf
    LDH_LAC() -> LDH() + LAC() kf


end reaction rules


end model

# Actions
generate_network({overwrite=>1})
simulate_ode({t_end=>600, n_steps=>49})
"""

# Write BNGL file
with open("assign-90.bngl", "w") as f:
    f.write(bngl_model)

# Run BNGL with BioNetGen
subprocess.run(["bionetgen", "run", "-i", "assign-90.bngl"], 
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
               check=True)

# Load simulation results
res = pd.read_csv("assign-90.gdat", sep=r'\s+', comment="#", header=None)

# Assign correct column names
res.columns = ['time', 'NAD', 'LAC', 'PYR', 'PEP', 'PG2', 'PG3']

# Observables of interest
onames= ['NAD','LAC','PYR', 'PEP', 'PG2', 'PG3']
for i in range(0,len(res),7):
    print(' '.join([ f'{o}: {res[o][i]:.0f}' for o in onames]))