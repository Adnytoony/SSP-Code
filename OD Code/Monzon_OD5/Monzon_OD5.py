#Name: Ariadna Monzon
#Date: 06/26/26
#Purpose: Full orbit determination code

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

import odlib
reload(odlib)

import Monzon_OD2 
reload(Monzon_OD2)

import pandas as pd

'''
Inputs: For each of 3 observations,
o The observation time (JD)
o The asteroid’s observed celestial coordinates (RA & Dec)
o The Earth-Sun vector
Your input file should also have
o A target time (JD)
o Reference elements (𝑎, 𝑒, 𝑖, Ω, 𝜔, 𝑀) from JPL Horizons at the target time
o A flag specifying whether to use 3rd or 4th order terms in the f and g series
o A “tolerance” value that determines when the method of Gauss has converged
'''

def main():
    test_cases = pd.read_csv('mog_test_cases(in) (1).csv')
    cond_as1 = (test_cases['asteroid_name'] == '2002 QF15')

    earth_sun1 = np.array([test_cases[cond_as1]['sun_x_1'][0], test_cases[cond_as1]['sun_y_1'][0], test_cases[cond_as1]['sun_z_1'][0]])
    earth_sun2 = np.array([test_cases[cond_as1]['sun_x_2'][0], test_cases[cond_as1]['sun_y_2'][0], test_cases[cond_as1]['sun_z_2'][0]])
    earth_sun3 = np.array([test_cases[cond_as1]['sun_x_3'][0], test_cases[cond_as1]['sun_y_3'][0], test_cases[cond_as1]['sun_z_3'][0]])

    RA1 = test_cases[cond_as1]['ra1'][0]
    RA2 = test_cases[cond_as1]['ra2'][0]
    RA3 = test_cases[cond_as1]['ra3'][0]

    #RA is hours minutes seconds
    RAs = []
    for i in (RA1, RA2, RA3):
        RA = i
        RA = RA.split()
        h, m, s = RA
        h = float(h)
        m = float(m)
        s = float(s)
        RA = odlib.hms_to_deg(h, m, s)
        RAs.append(RA)

    RA1, RA2, RA3 = RAs
    '''
    print(RA1)
    print(RA2)
    print(RA3)
    '''
    
    dec1 = test_cases[cond_as1]['1-Dec'][0]
    dec2 = test_cases[cond_as1]['2-Dec'][0]
    dec3 = test_cases[cond_as1]['3-Dec'][0]

    #declination is in degrees arcminutes arcseconds
    decs = []
    for i in (dec1, dec2, dec3):
        dec = i
        dec = dec.split()
        d, arm, ars = dec
        d = float(d)
        arm = float(arm)
        ars = float(ars)
        dec = d + arm/60 + ars/3600
        decs.append(dec)

    dec1, dec2, dec3 = decs
    '''
    print(dec1)
    print(dec2)
    print(dec3)
    '''
    RA1 = np.deg2rad(RA1)
    RA2 = np.deg2rad(RA2)
    RA3 = np.deg2rad(RA3)
    dec1 = np.deg2rad(dec1)
    dec2 = np.deg2rad(dec2)
    dec3 = np.deg2rad(dec3)
    
    t1 = test_cases[cond_as1]['t1_jd'][0]
    t2 = test_cases[cond_as1]['t2_jd'][0]
    t3 = test_cases[cond_as1]['t3_jd'][0]
    
    jpl_r2_ref = np.array([(test_cases[cond_as1]['jpl_r2_x'][0]), (test_cases[cond_as1]['jpl_r2_y'][0]), (test_cases[cond_as1]['jpl_r2_z'][0])])

    jpl_v2_ref = np.array([(test_cases[cond_as1]['jpl_v2_x'][0]), (test_cases[cond_as1]['jpl_v2_y'][0]), (test_cases[cond_as1]['jpl_v2_z'][0])])

    jpl_a = test_cases[cond_as1]['jpl_a'][0]

    jpl_e = test_cases[cond_as1]['jpl_e'][0]

    jpl_i = test_cases[cond_as1]['jpl_i'][0]

    jpl_loan = test_cases[cond_as1]['jpl_loan'][0]

    jpl_aop = test_cases[cond_as1]['jpl_aop'][0]

    jpl_ma = test_cases[cond_as1]['jpl_ma'][0]

    jpl_dist2 = test_cases[cond_as1]['jpl_dist2'][0]

    jpl_Target = test_cases[cond_as1]['t_target_jd'][0]
   
   
    
    r1_vec, r2_vec, r3_vec, p_scalar2, r_u = odlib.get_pos_vec(RA1, dec1, RA2, dec2, RA3, dec3, earth_sun1, earth_sun2, earth_sun3, t1, t2, t3)
    
    vel_vec_2 = odlib.get_vel_vec2(r1_vec, r2_vec, r3_vec, t1, t2, t3, r_u)

    #new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(r2_vec, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)

    #print("Reference Value (JPL): ", jpl_r2_ref)
    print("Calculated Value: ", r2_vec)
    print("Calculated Value: ", vel_vec_2)

    #print("Old p_scalar: ", p_scalar2)
    #print("New p_scalar: ", new_p_scalar2)

    p_hat1 = odlib.range_uvec_4_pos_vec(RA1, dec1)
    p_hat2 = odlib.range_uvec_4_pos_vec(RA2, dec2)
    p_hat3 = odlib.range_uvec_4_pos_vec(RA3, dec3)
    

    earth_tilt_deg = np.deg2rad(23.4374) 
    rotation_earth_tilt2ecliptic = np.array([
    [1, 0, 0],
    [0, np.cos(-earth_tilt_deg), -np.sin(-earth_tilt_deg)],
    [0, np.sin(-earth_tilt_deg), np.cos(-earth_tilt_deg)]
    ])
    
    p_hat1 = rotation_earth_tilt2ecliptic @ p_hat1
    p_hat2 = rotation_earth_tilt2ecliptic @ p_hat2
    p_hat3 = rotation_earth_tilt2ecliptic @ p_hat3

    print('phat1 ', p_hat1)
    print('phat2 ', p_hat2)
    print('phat3 ', p_hat3)



    '''
    new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(r2_vec, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)
    print('new_pos_vec2 ', new_pos_vec2)
    new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(new_pos_vec2, new_vel_vec2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)
    print('new_pos_vec2 ', new_pos_vec2)

    '''
    
    iterations = 0
    while True:
    #for i in range(100):
        new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(r1_vec, r2_vec, r3_vec, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)
        iterations = iterations + 1

        #print(odlib.get_percent_difference(p_scalar2, new_p_scalar2))

        if (odlib.get_percent_difference(p_scalar2, new_p_scalar2)) < 1e-20:
           break
            
        r2_vec = new_pos_vec2
        #print('r2_vec ', r2_vec)
        vel_vec_2 = new_vel_vec2
        p_scalar2 = new_p_scalar2

    print("Iterations: ", iterations)
    
    print("---Testing pos_vec---")
    print("Reference Value (JPL): ", jpl_r2_ref)
    print("Calculated Value: ", new_pos_vec2)
    print("Percent Difference (r_vec): ", odlib.get_percent_difference(new_pos_vec2, jpl_r2_ref))

    print("---Testing vel_vec---")
    print("Reference Value (JPL): ", jpl_v2_ref)
    print("Calculated Value: ", new_vel_vec2)
    print("Percent Difference (r_vec): ", odlib.get_percent_difference(new_vel_vec2, jpl_v2_ref))


    #print("Old p_scalar: ", p_scalar2)
    #print("New p_scalar: ", new_p_scalar2)
    #print("Percent Difference (p): ", odlib.get_percent_difference(p_scalar2, new_p_scalar2))
    
    print("---Testing Semimajor-axis---")
    print("Reference Value (JPL):",  jpl_a)
    a = odlib.get_semimajor_axis(new_pos_vec2,new_vel_vec2)
    print("Calculated Value: ", a)
    print("Percent Difference: ", odlib.get_percent_difference(a,jpl_a))

    print("---Testing Eccentricity---")
    print("Reference Value (JPL): ", jpl_e)
    e = odlib.get_eccentricity(new_pos_vec2,new_vel_vec2)
    print("Calculated Value: ", e)
    print("Percent Difference: ", odlib.get_percent_difference(e, jpl_e))

    print("---Testing Inclination---")
    print("Reference Value (JPL): ", jpl_i)
    i = odlib.rad_to_deg(odlib.get_inclination(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", i)
    print("Percent Difference: ", odlib.get_percent_difference(i,jpl_i))

    print("---Testing Ascending Node---")
    print("Reference Value (JPL): ", jpl_loan)
    omega = odlib.rad_to_deg(odlib.get_len_ascending_node(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", omega)
    print("Percent Difference: ", odlib.get_percent_difference(omega,jpl_loan))

    print("---Testing Perihelion---")
    print("Reference Value (JPL): ", jpl_aop)
    w = odlib.rad_to_deg(odlib.get_arg_perihelion(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", w)
    print("Percent Difference: ", odlib.get_percent_difference(w,jpl_aop))

    print("---Testing Mean Anomaly---")
    print("Reference Value (JPL): ", jpl_ma)

    M_ep_time = odlib.propagate(new_pos_vec2, new_vel_vec2, float(t2), float(jpl_Target))
    M_ep_time = odlib.rad_to_deg(M_ep_time)

    print("Calculated Value: ", M_ep_time)
    print("Percent Difference: ", odlib.get_percent_difference(M_ep_time,jpl_ma))


    print("---Testing Distance---")
    print("Reference Value (JPL): ", jpl_dist2)
    print("Calculated Distance: ", new_p_scalar2)
    print("Percent Difference: ", odlib.get_percent_difference(new_p_scalar2,jpl_dist2))
    
    

'''
Outputs: The required outputs are
o The asteroid’s position & velocity vectors for the central observation. Use ecliptic
rectangular coordinates and units of AU, AU/day.
o The distance between the observer and the asteroid during the central observation
(in AU).
o The orbital elements (𝑎, 𝑒, 𝑖, Ω, 𝜔, 𝑀) for the asteroid at the target time, and a
comparison with JPL’s values (including % difference)
'''

def main2():
    test_cases = pd.read_csv('mog_test_cases(in) (1).csv')
    cond_as2 = (test_cases['asteroid_name'] == '2003 UD8')

    earth_sun1 = np.array([test_cases[cond_as2]['sun_x_1'][1], test_cases[cond_as2]['sun_y_1'][1], test_cases[cond_as2]['sun_z_1'][1]])
    earth_sun2 = np.array([test_cases[cond_as2]['sun_x_2'][1], test_cases[cond_as2]['sun_y_2'][1], test_cases[cond_as2]['sun_z_2'][1]])
    earth_sun3 = np.array([test_cases[cond_as2]['sun_x_3'][1], test_cases[cond_as2]['sun_y_3'][1], test_cases[cond_as2]['sun_z_3'][1]])

    RA1 = test_cases[cond_as2]['ra1'][1]
    RA2 = test_cases[cond_as2]['ra2'][1]
    RA3 = test_cases[cond_as2]['ra3'][1]

    #RA is hours minutes seconds
    RAs = []
    for i in (RA1, RA2, RA3):
        RA = i
        RA = RA.split()
        h, m, s = RA
        h = float(h)
        m = float(m)
        s = float(s)
        RA = odlib.hms_to_deg(h, m, s)
        RAs.append(RA)

    RA1, RA2, RA3 = RAs
    '''
    print(RA1)
    print(RA2)
    print(RA3)
    '''
    
    dec1 = test_cases[cond_as2]['1-Dec'][1]
    dec2 = test_cases[cond_as2]['2-Dec'][1]
    dec3 = test_cases[cond_as2]['3-Dec'][1]

    #declination is in degrees arcminutes arcseconds
    decs = []
    for i in (dec1, dec2, dec3):
        dec = i
        dec = dec.split()
        d, arm, ars = dec
        d = float(d)
        arm = float(arm)
        ars = float(ars)
        dec = d - arm/60 - ars/3600
        decs.append(dec)

    dec1, dec2, dec3 = decs
    '''
    print(dec1)
    print(dec2)
    print(dec3)
    '''
    RA1 = np.deg2rad(RA1)
    RA2 = np.deg2rad(RA2)
    RA3 = np.deg2rad(RA3)
    dec1 = np.deg2rad(dec1)
    dec2 = np.deg2rad(dec2)
    dec3 = np.deg2rad(dec3)
    
    t1 = test_cases[cond_as2]['t1_jd'][1]
    t2 = test_cases[cond_as2]['t2_jd'][1]
    t3 = test_cases[cond_as2]['t3_jd'][1]
    
    jpl_r2_ref = np.array([(test_cases[cond_as2]['jpl_r2_x'][1]), (test_cases[cond_as2]['jpl_r2_y'][1]), (test_cases[cond_as2]['jpl_r2_z'][1])])

    jpl_v2_ref = np.array([(test_cases[cond_as2]['jpl_v2_x'][1]), (test_cases[cond_as2]['jpl_v2_y'][1]), (test_cases[cond_as2]['jpl_v2_z'][1])])

    jpl_a = test_cases[cond_as2]['jpl_a'][1]

    jpl_e = test_cases[cond_as2]['jpl_e'][1]

    jpl_i = test_cases[cond_as2]['jpl_i'][1]

    jpl_loan = test_cases[cond_as2]['jpl_loan'][1]

    jpl_aop = test_cases[cond_as2]['jpl_aop'][1]

    jpl_ma = test_cases[cond_as2]['jpl_ma'][1]

    jpl_dist2 = test_cases[cond_as2]['jpl_dist2'][1]

    jpl_Target = 2459420.5
   
    
    r1_vec, r2_vec, r3_vec, p_scalar2, r_u = odlib.get_pos_vec(RA1, dec1, RA2, dec2, RA3, dec3, earth_sun1, earth_sun2, earth_sun3, t1, t2, t3)
    
    vel_vec_2 = odlib.get_vel_vec2(r1_vec, r2_vec, r3_vec, t1, t2, t3, r_u)

    #new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(r2_vec, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)

    #print("Reference Value (JPL): ", jpl_r2_ref)
    print("Calculated Value: ", r2_vec)
    print("Calculated Value: ", vel_vec_2)

    #print("Old p_scalar: ", p_scalar2)
    #print("New p_scalar: ", new_p_scalar2)

    p_hat1 = odlib.range_uvec_4_pos_vec(RA1, dec1)
    p_hat2 = odlib.range_uvec_4_pos_vec(RA2, dec2)
    p_hat3 = odlib.range_uvec_4_pos_vec(RA3, dec3)
    
    earth_tilt_deg = np.deg2rad(23.4374) 
    rotation_earth_tilt2ecliptic = np.array([
    [1, 0, 0],
    [0, np.cos(-earth_tilt_deg), -np.sin(-earth_tilt_deg)],
    [0, np.sin(-earth_tilt_deg), np.cos(-earth_tilt_deg)]
    ])
    
    p_hat1 = rotation_earth_tilt2ecliptic @ p_hat1
    p_hat2 = rotation_earth_tilt2ecliptic @ p_hat2
    p_hat3 = rotation_earth_tilt2ecliptic @ p_hat3
    
    iterations = 0
    while True:
    #for i in range(100):
        new_pos_vec2, new_vel_vec2, new_p_scalar2 = odlib.get_new_vec(r1_vec, r2_vec, r3_vec, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3)
        iterations = iterations + 1

        #print(odlib.get_percent_difference(p_scalar2, new_p_scalar2))

        if (odlib.get_percent_difference(p_scalar2, new_p_scalar2)) < 1e-20:
           break
            
        r2_vec = new_pos_vec2
        #print('r2_vec ', r2_vec)
        vel_vec_2 = new_vel_vec2
        p_scalar2 = new_p_scalar2

    print("Iterations: ", iterations)
    
    print("---Testing pos_vec---")
    print("Reference Value (JPL): ", jpl_r2_ref)
    print("Calculated Value: ", new_pos_vec2)
    print("Percent Difference (r_vec): ", odlib.get_percent_difference(new_pos_vec2, jpl_r2_ref))

    print("---Testing vel_vec---")
    print("Reference Value (JPL): ", jpl_v2_ref)
    print("Calculated Value: ", new_vel_vec2)
    print("Percent Difference (r_vec): ", odlib.get_percent_difference(new_vel_vec2, jpl_v2_ref))

    #print("Old p_scalar: ", p_scalar2)
    #print("New p_scalar: ", new_p_scalar2)
    #print("Percent Difference (p): ", odlib.get_percent_difference(p_scalar2, new_p_scalar2))
    
    print("---Testing Semimajor-axis---")
    print("Reference Value (JPL):",  jpl_a)
    a = odlib.get_semimajor_axis(new_pos_vec2,new_vel_vec2)
    print("Calculated Value: ", a)
    print("Percent Difference: ", odlib.get_percent_difference(a,jpl_a))

    print("---Testing Eccentricity---")
    print("Reference Value (JPL): ", jpl_e)
    e = odlib.get_eccentricity(new_pos_vec2,new_vel_vec2)
    print("Calculated Value: ", e)
    print("Percent Difference: ", odlib.get_percent_difference(e, jpl_e))

    print("---Testing Inclination---")
    print("Reference Value (JPL): ", jpl_i)
    i = odlib.rad_to_deg(odlib.get_inclination(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", i)
    print("Percent Difference: ", odlib.get_percent_difference(i,jpl_i))

    print("---Testing Ascending Node---")
    print("Reference Value (JPL): ", jpl_loan)
    omega = odlib.rad_to_deg(odlib.get_len_ascending_node(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", omega)
    print("Percent Difference: ", odlib.get_percent_difference(omega,jpl_loan))

    print("---Testing Perihelion---")
    print("Reference Value (JPL): ", jpl_aop)
    w = odlib.rad_to_deg(odlib.get_arg_perihelion(new_pos_vec2,new_vel_vec2))
    print("Calculated Value: ", w)
    print("Percent Difference: ", odlib.get_percent_difference(w,jpl_aop))

    print("---Testing Mean Anomaly---")
    print("Reference Value (JPL): ", jpl_ma)

    M_ep_time = odlib.propagate(new_pos_vec2, new_vel_vec2, float(t2), float(jpl_Target))
    M_ep_time = odlib.rad_to_deg(M_ep_time)

    print("Calculated Value: ", M_ep_time)
    print("Percent Difference: ", odlib.get_percent_difference(M_ep_time,jpl_ma))

    print("---Testing Distance---")
    print("Reference Value (JPL): ", jpl_dist2)
    print("Calculated Distance: ", new_p_scalar2)
    print("Percent Difference: ", odlib.get_percent_difference(new_p_scalar2,jpl_dist2))