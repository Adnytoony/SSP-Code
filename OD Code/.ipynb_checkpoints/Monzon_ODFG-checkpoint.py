import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

import pandas as pd
test_cases = pd.read_csv('f_and_g_test_cases(in).csv')

def main():
    for i in range(len(test_cases)):
        pos_vec = np.array([test_cases['r2_x'][i], test_cases['r2_y'][i], test_cases['r2_z'][i]])
        vel_vec = np.array([test_cases['v2_x'][i], test_cases['v2_y'][i], test_cases['v2_z'][i]])
        tau = test_cases['tau'][i]
        order_4 = test_cases['order4'][i]
        f_output = test_cases['f_output'][i]
        g_output = test_cases['g_output'][i]

        print("Testing calculate_fg on ", i + 1)
        calc_f, calc_g = odlib.calculate_fg(pos_vec, vel_vec, tau, order_4)
        print("Calculated Value F: ", calc_f)
        print("Actual Value F: ", f_output)
        print("Percent Difference (F): ", odlib.get_percent_difference(calc_f, f_output))
        
        print("Calculated Value G: ", calc_g)
        print("Actual Value G: ", g_output)
        print("Percent Difference (G): ", odlib.get_percent_difference(calc_g, g_output))