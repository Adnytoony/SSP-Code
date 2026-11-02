#Name: Ariadna Monzon
#Date: 06/26/26
#Purpose: Calculate Ephemeris Using Newton_Raphson Method

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

def main():
    E, i, tol = odlib.Newton_Raphson(0.8, 0.42, 5, 0.01)
    print ("Testing Newton-Raphson Method")
    print ("E = ", E)
    print ("Convergence Parameter = ", tol)
    print ("Number of iterations = ", i)

    E, i, tol = odlib.Newton_Raphson(2, 4, 40, 0.01)
    print("Test 2")
    print ("E = ", E)
    print ("Convergence Parameter = ", tol)
    print ("Number of iterations = ", i)