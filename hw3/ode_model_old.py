from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class ParamsABC:
    """
    Parameters for the sequential reaction A -> B -> C.

    Attributes
    ----------
    k1_per_s: float
        Rate constant k1 [1/s] for A -> B.
    k2_per_s: float
        Rate constant k2 [1/s] for B -> C.
    tol_mass: float
        Tolerance for mass-conservation checks.
    tol_neg: float
        Tolerance for negativity checks.

    Notes
    -----
    Units: time [s], concentrations [arbitrary or µM], rates [1/s].
    """

    k1_per_s: float = 100.0
    k2_per_s: float = 0.1
    tol_mass: float = 1e-9
    tol_neg: float  = 1e-12


def dxdt(state, params):
    """
    Compute the derivative [dA/dt, dB/dt, dC/dt] for the sequential reaction A -> B -> C.
    Eqautions:
        dA/dt = -k1*A
        dB/dt =  k1*A - k2*B
        dC/dt =  k2*B
    Units: A,B,C [µM]; t,dt [s]; k1,k2 [1/s].

    Args:
    state:    vector (numpy array) that holds the concentration of A, B, and C, respectively.
    params:    special container that holds four variables that can be accessed by name - two reaction rates k1_per_s and k2_per_s, and two parameters tol_mass and tol_neg that we will use later for checking our work. To access one of these variables, you can use the . operator, as in params.k1_per_s.

    Output:
    Returns a vector that contains [dA/dt, dB/dt, dC/dt] based on the current concentrations in state and the reaction rates in params.
    """
    A = state[0]; B = state[1]; C = state[2]
    dAdt = -(params.k1_per_s)*A
    dBdt = ((params.k1_per_s)*A) - ((params.k2_per_s)*B)
    dCdt = (params.k2_per_s)*B
    

    return np.array([dAdt, dBdt, dCdt])


def euler_step(state, params, dt):
    """
    Explicit Euler step for A -> B -> C.
    Computes the concentration at the next timestep based on the current concentration and its differential equation.
    Equations:
        next A = A + dA/dt *dt
        next B = B + dB/dt *dt
        next C = C + dC/dt *dt
    Units: A,B,C [µM]; t,dt [s].
        
    Args:
    state:    vector (numpy array) that holds the concentration of A, B, and C, respectively.
    params:    special container that holds four variables that can be accessed by name - two reaction rates k1_per_s and k2_per_s, and two parameters tol_mass and tol_neg that we will use later for checking our work. To access one of these variables, you can use the . operator, as in params.k1_per_s.
    dt:    time step in units of seconds

    Ouput: 
    Returns a vector that gives the updated concentrations [A, B, C] after one Euler step of dt seconds.
    """
    derivs = dxdt(state, params)
    A = state[0] + (derivs[0]*dt) 
    B = state[1] + (derivs[1]*dt)
    C = state[2] + (derivs[2]*dt)
    return np.array([A, B, C])


def simulate(x0, t_end_s, dt_s, params, checks=True, clip_negative=False):
    """
    Generic simulator with light numerical checks.
    Creates t, a time array from time 0 to t_end_s. Creates X, an array of simulated concentration values, with each row containing concentrations of A, B, and C at corresponding time points. The first row is x0.
    
    Units: x0,X [µM]; t,t_end_s,dt_s [s]; k1,k2 [1/s].
    
    Args: 
    x0:    specifies the initial concentrations [A0, B0, C0].
    t_end_s:    gives the final integration time in units of seconds.
    dt_s:    time step in units of seconds.
    params:    special container that holds four variables that can be accessed by name - two reaction rates k1_per_s and k2_per_s, and two parameters tol_mass and tol_neg that we will use later for checking our work. To access one of these variables, you can use the . operator, as in params.k1_per_s.
    checks:    boolean (input True or False) which will make this function perform a few simple tests 
                If checks=True, then:
                    Raise a ValueError if any concentration becomes smaller than -tol_neg
                    Raise a ValueError if the total mass (A+B+C) deviates from (A0+B0+C0) by more than tol_mass

    Output:
    Returns the time grid (array) and an array with the simulated concentrations over time.
    """
    t = np.arange(0,(t_end_s+dt_s), dt_s)
    X = np.empty((t.shape, len(x0)))
    X[0] = x0
                
    for i in range(1, t.shape[0]):
        X[i] = (euler_step(X[i-1], params, dt_s))
        if checks == True:
            if np.any(X[i] < -params.tol_neg):
                raise ValueError(f'One or more concentrations in x0 are smaller than -tol_neg')
            if np.any(abs(np.sum(X[i]) - np.sum(X[0])) > params.tol_mass):
                raise ValueError(f'Total mass deviates from initial total mass by more than tol_mass')       
    
    return t, X


# ---------- Reference (analytic) solutions ----------

def analytic_A(t, A0, k1):
    """
    Analytical solution for A(t) in A -> B -> C with A0 initial.
    Equation:
    A(t) = A0 * np.exp(-k1*t)
    Units: A0 [µM]; t, [s]; k1,k2 [1/s].
    
    """

    return A0 * np.exp(-k1*t)


def analytic_B(t, A0, k1, k2):
    """
    Analytical solution for B(t) in A -> B -> C with A0, B0=0 initial.
    Equation:
    B(t) = A0*(k1/(k2-k1)*(np.exp(-k1*t)-np.exp(-k2*t))
    Units: A0, B0 [µM]; t, [s]; k1,k2 [1/s].
    """
    
    return A0*(k1/(k2-k1)*(np.exp(-k1*t)-np.exp(-k2*t))


def analytic_C(t, A0, k1, k2):
    """
    Analytical solution for C(t) in A -> B -> C with A0, B0=0, C0=0 initial.
    Equation:
    C(t) = A0*(1-((k2/(k2-1))*np.exp(-k1*t))-((k1/(k1-k2))*np.exp(-k2*t)))
    Units: A0, B0, C0 [µM]; t, [s]; k1,k2 [1/s].
    """

    return A0*(1-((k2/(k2-1))*np.exp(-k1*t))-((k1/(k1-k2))*np.exp(-k2*t)))
