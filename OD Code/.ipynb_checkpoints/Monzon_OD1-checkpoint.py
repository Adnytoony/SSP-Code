#Name: Ariadna Monzon
#Date: 06/26/26
#Purpose: Calculate the Angula Momentum 

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

OD1 = np.loadtxt("Monzon_OD1Input.txt")

def main():
    print ("Testing Angular Momentum")
    print ("Expected: -0.341081, 0.228006, 0.873642")
    print ("Result: ", odlib.get_angular_momentum(OD1[0],OD1[1]))