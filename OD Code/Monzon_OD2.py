#Name: Ariadna Monzon
#Date: 06/26/26
#Purpose: Calculate orbital elements / works as expected

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)


OD1 = np.loadtxt("Monzon_OD1Input.txt")
OD2 = np.loadtxt("Monzon_OD2Input.txt")

def main():
    print("Date: 2018-07-14 0:00 UTC")
    print("Julian Date:  2458158.72")
    
    print("Testing Semimajor-axis")
    print("Reference Value (JPL): 1.056723680924958")
    a = odlib.get_semimajor_axis(OD1[0],OD1[1])
    print("Calculated Value: ", a)
    print("Percent Difference: ", odlib.get_percent_difference(a,OD2[0]))

    print("Testing Eccentricity")
    print("Reference Value (JPL): 0.3442825499921447")
    e = odlib.get_eccentricity(OD1[0],OD1[1])
    print("Calculated Value: ", e)
    print("Percent Difference: ", odlib.get_percent_difference(e,OD2[1]))

    print("Testing Inclination")
    print("Reference Value (JPL): 25.15378611481617")
    i = odlib.rad_to_deg(odlib.get_inclination(OD1[0],OD1[1]))
    print("Calculated Value: ", i)
    print("Percent Difference: ", odlib.get_percent_difference(i,OD2[2]))
    

    print("Testing Ascending Node")
    print("Reference Value (JPL): 236.2498688799159")
    omega = odlib.rad_to_deg(odlib.get_len_ascending_node(OD1[0],OD1[1]))
    print("Calculated Value: ", omega)
    print("Percent Difference: ", odlib.get_percent_difference(omega,OD2[3]))
    
    '''
    print("Testing True Anomaly")
    print("Expected:158.9559247584013")
    nu = odlib.rad_to_deg(odlib.get_true_anomaly(OD1[0],OD1[1]))
    print("Actual: ", nu)
    print("Percent Difference: ", odlib.get_percent_difference(nu,158.9559247584013))
    
    
    print("Testing U")
    u = odlib.get_U(OD1[0],OD1[1])
    print("Actual: ", u)
    '''
    
    print("Testing Perihelion")
    print("Reference Value (JPL): 255.5322271736599")
    w = odlib.rad_to_deg(odlib.get_arg_perihelion(OD1[0],OD1[1]))
    print("Calculated Value: ", w)
    print("Percent Difference: ", odlib.get_percent_difference(w,OD2[4]))
    

    #NTS: apparently it is not supposed to match JLP Horizon
    print("Testing Mean Anomaly")
    print("Reference Value (JPL): 15.74699967867798")
    m = odlib.rad_to_deg(odlib.get_mean_anomaly(OD1[0],OD1[1]))
    print("Calculated Value: ", m)
    print("Percent Difference: ", odlib.get_percent_difference(m,OD2[5]))
    
