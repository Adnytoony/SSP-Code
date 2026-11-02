#Name: Ariadna Monzon
#Date: 06/26/26
#Purpose: Calculate orbital elements / works as expected

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

import Monzon_OD2 
reload(Monzon_OD2)


OD1 = np.loadtxt("Monzon_OD1Input.txt")
OD2 = np.loadtxt("Monzon_OD2Input.txt")
OD4 = np.loadtxt("Monzon_OD4Input.txt")

def main():
    
    #get Dec and RA
    ref_time = 2458313.5 #Reference Time: July 14th 2028
    target_time = 2458678.5 #Target Date: July 14th 2019
    earth_sun_vec = OD4
    ref_RA = 228.51902  
    ref_dec = 19.77636

    print("Reference Time (JD):", ref_time)
    print("Target Time (JD):", target_time)
    
    print("Declination:")
    print("Reference Value (JPL): ", ref_dec)
    dec = odlib.get_declination(OD1[0],OD1[1], earth_sun_vec, target_time, ref_time, 0.01)
    dec_deg = odlib.rad_to_deg(dec)
    print("Calculated Value: ", dec_deg)
    print("Percent Difference: ", odlib.get_percent_difference(dec_deg, ref_dec))

    print("Right Ascension:")
    print("Reference Value (JPL): ", ref_RA)
    RA = odlib.get_right_ascension(OD1[0],OD1[1], earth_sun_vec, target_time, ref_time, 0.01)
    RA_deg = odlib.rad_to_deg(RA)
    print("Calculated Value: ", RA_deg)
    print("Percent Difference: ", odlib.get_percent_difference(RA_deg, ref_RA))
