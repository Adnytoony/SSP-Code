import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

def main():
#--Test Case 1---
    print("Test case 1:")
    taus = [-0.15481889055, 0.15481889055, 0.3096377811]
    tau1, tau3, tau0 = taus
    Sun2 = [-0.2398478458274071, 0.9065739917845802, 0.3929623749770952]
    rhohat2 = [-0.8518563498182248, -0.2484702599212149, 0.4610892421311239]
    Ds = [-0.0010461861084885213, -0.17297581974209159, -0.17201260125558127, -0.16712421570714076]

    roots_ex = [1.014886625023963, 1.2932503440012362, 1.5851855408957922]
    rhos_ex = [0.012425430826237482, 0.9753289007273918, 1.386900042701193]

    roots, rhos = odlib.SEL(tau1, tau3, tau0, Sun2, rhohat2, Ds)
    print("Expected roots = ", roots_ex)
    print("Actual roots = ", roots)
    print("Expected rhos = ", rhos_ex)
    print("Actual rhos = ", rhos)
   # print("Percent Difference (roots): ", odlib.get_percent_difference(roots, roots_ex))
    #print("Percent Difference (rhos): ", odlib.get_percent_difference(rhos, rhos_ex))


#--Test Case 2---
    print("Test case 2:")
    taus = [-0.1720209895, 0.1720209895, 0.344041979]
    tau1, tau3, tau0 = taus
    Sun2 = [-0.2683394448727136, 0.8997620807182745, 0.3900022331276332]
    rhohat2 = [0.052719013914983195, -0.9121555187306237, 0.40643943610469035]
    Ds = [0.0011797570297704812, 0.052586743761143424, 0.05848153743706686, 0.06274019190783499]

    roots_ex = [0.7775650888697365, 1.0071727095060097, 1.266484861890734]
    rhos_ex = [-0.8448416611523188, -0.01440831314501545, 0.33742943029525474]

    roots, rhos = odlib.SEL(tau1, tau3, tau0, Sun2, rhohat2, Ds)
    print("Expected roots = ", roots_ex)
    print("Actual roots = ", roots)
    print("Expected rhos = ", rhos_ex)
    print("Actual rhos = ", rhos)
   # print("Percent Difference (roots): ", odlib.get_percent_difference(roots, roots_ex))
   # print("Percent Difference (rhos): ", odlib.get_percent_difference(rhos, rhos_ex))