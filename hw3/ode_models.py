from dataclasses import dataclass
def dxdt(state,params):
    
@dataclass
class params:
    k1_per_s: float
    k2_per_s: float
    tol_mass: float
    tol_neg: float