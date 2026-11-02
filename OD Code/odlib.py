import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from importlib import reload

def hms_to_deg(hours, minutes, seconds):
    hms = (hours + (minutes/60) + (seconds/3600))*(360/24)
    return hms

def convert_2_gaussian(vector):
    return vector * 58.1324408629
    
def get_angular_momentum(pos_vec, vel_vec):
    vel_gauss = convert_2_gaussian(vel_vec) #convert (each) to Gaussian date
    ang_momentum = np.cross(pos_vec, vel_gauss) #cross product of position vector and velocity vector
    return ang_momentum

#Helper Func x Newton_Raphson Method - calculates the funcion of E and derivative
def get_FE(e, M, E):
    FE = E - e*np.sin(E) - M
    fE = 1 - e*np.cos(E)
    return (FE/fE)

def Newton_Raphson(e, M, x0, tol): #implements Newton_raphson method
    i = 0 #iterations
    while True:
        x_n = x0 - get_FE(e, M, x0) #Newton Raphson Eq.
        i+= 1 #adds 1 for every time it runs through the loop (Iteration)
        
        #difference between given value(x0) and new value (x_n) must be less than the tolerance
        if np.abs(x_n - x0) < tol:
            break
            
        #reassigns the new value to the given value, it is supposed to be closer to the right answer
        x0 = x_n 
        
    #actual difference achieved (Convergence Parameter) 
    tol = np.abs(x_n - x0)
       
    return x_n, i, tol
    
#---Calculating Orbital Elements---
a = 0 #Semimajor Axis (a)
e = 0 #Eccentricity (e)
i = 0 #Inclination (i)
omega = 0 #Longitude of the Ascending Node (Ω)
w = 0 #Argument of Perihelion (ω)
nu = 0 # true anomaly (v = nu)
u = 0 #???
m = 0 # Mean anomaly (M)
E_anom = 0 #ecc
    
def get_vector_magnitude(vector):
    x_vec, y_vec, z_vec = vector
    vec_mag = np.sqrt(x_vec**2 + y_vec**2 + z_vec**2)
    return vec_mag
    
def get_semimajor_axis(pos_vec, vel_vec):
    vel_gauss = convert_2_gaussian(vel_vec)
    r_mag = get_vector_magnitude(pos_vec)
    v_mag = get_vector_magnitude(vel_gauss)
    
   # print(r_mag)
   # print(v_mag)
    a = 1/((2/r_mag) - v_mag**2)
    return a
    
def get_eccentricity(pos_vec, vel_vec):
    h_mag = get_vector_magnitude(get_angular_momentum(pos_vec, vel_vec))
    a = get_semimajor_axis(pos_vec, vel_vec)
    #print(h_mag)
    e = np.sqrt(1 - (h_mag**2/a))
    return e

def rad_to_deg(val_rad):
    val_rad = val_rad * (180/np.pi)
    return val_rad
    
#NTS: JPL Horizon has inclination(IN) AND Longitude of Ascending Node (OM) in Degrees, the equations are in Radians
def get_inclination(pos_vec, vel_vec):
    hx, hy, hz = get_angular_momentum(pos_vec, vel_vec)
    #print(hx,hy,hz)
    i = np.arctan(np.sqrt(hx**2 + hy**2)/hz)
    return i

#different quadrant checks for cos and sin 
def quadrant_check_sin(cos_val_rad, val_rad):
    if cos_val_rad < 0:
        return (2*np.pi - val_rad)
    else:
        return val_rad

#NTS: inclination should NOT be in degrees for Ascending Node formula
def get_len_ascending_node(pos_vec, vel_vec):
    hx, hy, hz = get_angular_momentum(pos_vec, vel_vec)
    h_mag = get_vector_magnitude(get_angular_momentum(pos_vec, vel_vec))
    i = get_inclination(pos_vec, vel_vec)
    
    sin_omega = hx / (h_mag * (np.sin(i)))
    cos_omega = -hy / (h_mag * (np.sin(i)))

    #Quadrant Check
    omega = np.arccos(cos_omega)
    omega = quadrant_check_sin(sin_omega, omega)
    return omega

def get_true_anomaly(pos_vec, vel_vec): #nu
    e = get_eccentricity(pos_vec, vel_vec)
    a = get_semimajor_axis(pos_vec, vel_vec)
    r_mag = get_vector_magnitude(pos_vec)
    h_mag = get_vector_magnitude(get_angular_momentum(pos_vec, vel_vec))
    
    cos_nu = ((a*(1 - e**2)/r_mag) - 1)/e
    sin_nu = (a*(1 - e**2)/(h_mag*e))*(np.dot(pos_vec, vel_vec)/r_mag)

    #quadrant check
    nu = np.arccos(cos_nu)
    nu = quadrant_check_sin(sin_nu, nu)
    return nu
    
def get_U(pos_vec, vel_vec):
    rx, ry, rz = pos_vec
    r_mag = get_vector_magnitude(pos_vec)
    omega = get_len_ascending_node(pos_vec, vel_vec)
    i = get_inclination(pos_vec, vel_vec)
    
    cos_u = (rx*np.cos(omega) + ry*np.sin(omega))/r_mag
    sin_u = rz/(r_mag*np.sin(i))
    
    #quadrant check
    u = np.arccos(cos_u)
    u = quadrant_check_sin(sin_u, u)
 
    return u

#argument of perihelion
def get_arg_perihelion(pos_vec, vel_vec):
    u = get_U(pos_vec, vel_vec)
    nu = get_true_anomaly(pos_vec, vel_vec)
    w = u - nu

    #correct if it is bigger than 2pi or lower than 0
    if w > 2*np.pi:
        w = w - 2*np.pi
    elif w < 0:
        w = w + 2*np.pi
        
    return w

def get_ecc_anomaly(pos_vec, vel_vec):
    e = get_eccentricity(pos_vec, vel_vec)
    a = get_semimajor_axis(pos_vec, vel_vec)
    r_mag = get_vector_magnitude(pos_vec)

    cos_E_anom = (1 - (r_mag/a))/e
    E_anom = np.arccos(cos_E_anom)

    return E_anom
    
def get_mean_anomaly(pos_vec, vel_vec):
    e = get_eccentricity(pos_vec, vel_vec)
    E_anom = get_ecc_anomaly(pos_vec, vel_vec)
    m = E_anom - e*np.sin(E_anom)

    if m > 2*np.pi:
        m = m - 2*np.pi
    elif m < 0:
        m = m + 2*np.pi
        
    return m

def get_percent_difference(actual, expected):
    diff = abs(actual - expected)/abs(expected)
    per_diff = diff*100
    return per_diff


#---Method of Gauss---
#---Generating Ephemeris---
k = 0.01720209894
mu = 1
t = 0
T = 0
#t = ref time
#T = time of perihelion passage (JPL Horizons: time of periapapsis[in Julian date])
#Step 1

def propagate(pos_vec, vel_vec, t, T):
    a = get_semimajor_axis(pos_vec, vel_vec)
    n = k * np.sqrt(mu/a**3)
    m = get_mean_anomaly(pos_vec, vel_vec)
    M_ep_time = n * (t - T) + m

    #quadrant check
    M_ep_time = M_ep_time % (2*np.pi)
    while M_ep_time < 0:
        M_ep_time +=2*np.pi
        
    return M_ep_time
    
def generate_ephemeris(pos_vec, vel_vec, t, T, tol):
    M_ep_time = propagate(pos_vec, vel_vec, t, T)
    e = get_eccentricity(pos_vec, vel_vec)
    
    #Step 2
    E, i, tol = Newton_Raphson(e, M_ep_time, M_ep_time, tol)
    #print("M_ep_time ", M_ep_time)
    return E

#Step 3
#NTS*: make get_cartesian_coordinates its own function for universal application to any vector
def get_cartesian_coordinates(pos_vec, vel_vec, t, T, tol):
    a = get_semimajor_axis(pos_vec, vel_vec)
    e = get_eccentricity(pos_vec, vel_vec)
    E = generate_ephemeris(pos_vec, vel_vec, t, T, tol)
    
    rx_cc = a*np.cos(E) - a*e
    ry_cc = a*np.sqrt(1 - e**2)*np.sin(E)
    rz_cc = 0

    pos_vec_cartesian = np.array([rx_cc, ry_cc, rz_cc])
    #print(pos_vec_cartesian)
    return pos_vec_cartesian

#Step 4
# *same for get_ecliptic_coordinates
#pos_vec_ec = 0
def get_ecliptic_coordinates(pos_vec, vel_vec, t, T, tol):
    omega = get_len_ascending_node(pos_vec, vel_vec)
    i = get_inclination(pos_vec, vel_vec)
    w = get_arg_perihelion(pos_vec, vel_vec)
    
    pos_vec_cartesian = get_cartesian_coordinates(pos_vec, vel_vec, t, T, tol)

    rotation_omega = np.array([
    [np.cos(omega), -np.sin(omega), 0],
    [np.sin(omega), np.cos(omega), 0],
    [0, 0, 1]
    ])

    rotation_i = np.array([
    [1, 0, 0],
    [0, np.cos(i), -np.sin(i)],
    [0, np.sin(i), np.cos(i)]
    ])

    rotation_w = np.array([
    [np.cos(w), -np.sin(w), 0],
    [np.sin(w), np.cos(w), 0],
    [0, 0, 1]
    ])
    
    pos_vec_ec = rotation_omega @ rotation_i @ rotation_w @ pos_vec_cartesian
    #print(pos_vec_ec)
    return pos_vec_ec

#Step 5
# *same for get_equatorial_coordinates
#pos_vec_ec = 0
earth_tilt_deg = np.deg2rad(23.4374) 
def get_equatorial_coordinates(vector):
    #this should be in main
    #pos_vec_ec = get_ecliptic_coordinates(pos_vec, vel_vec, t, T, tol)
    
    rotation_earth_tilt = np.array([
    [1, 0, 0],
    [0, np.cos(earth_tilt_deg), -np.sin(earth_tilt_deg)],
    [0, np.sin(earth_tilt_deg), np.cos(earth_tilt_deg)]
    ])
    
    pos_vec_eq = rotation_earth_tilt @ vector
    return pos_vec_eq

#Step 6: Determine the earth-sun vector from the JPL site
#R_vec =  Earth sun vector

#Step 7
#rename to range_uvec_4_ra
def get_range_unit_vector(pos_vec, vel_vec, R_vec, t, T, tol):
    pos_vec_eq = get_equatorial_coordinates(pos_vec, vel_vec, t, T, tol)
    range_vec = pos_vec_eq + R_vec
    
    range_vec_eq_mag = get_vector_magnitude(range_vec)
    range_unit_vec = range_vec/range_vec_eq_mag
    
    return range_unit_vec

    #these are correct

#Step 8
dec = 0 #declination
RA = 0 #right ascension

def get_declination(pos_vec, vel_vec, R_vec, t, T, tol):
    p_hat_x, p_hat_y, p_hat_z = get_range_unit_vector(pos_vec, vel_vec, R_vec, t, T, tol)
    dec = np.arcsin(p_hat_z)
    return dec

def get_right_ascension(pos_vec, vel_vec, R_vec, t, T, tol):
    p_hat_x, p_hat_y, p_hat_z = get_range_unit_vector(pos_vec, vel_vec, R_vec, t, T, tol)
    dec = get_declination(pos_vec, vel_vec, R_vec, t, T, tol)
    
    cos_RA = p_hat_x/np.cos(dec)
    sin_RA = p_hat_y/np.cos(dec)

    #quadrant check
    RA = np.arccos(cos_RA)
    RA = quadrant_check_sin(sin_RA, RA)

    return RA

#---Code SEL---
import numpy.polynomial.polynomial as poly


#in your actual MoG code, these would have already been calculated (or
#read from the input file in the case of the Sun vector)

def SEL(tau1, tau3, tau,Sun2,rhohat2,Ds):
    D0, D21, D22, D23 = Ds

   # roots = [0.,0.,0.] #for up to three real, positive roots
   # rhos = [0.,0.,0.] #range values for each real, positive root
    
    #OD Packet App. B
    #remember mu = 1 when working in gaussian units
    
    A1 = tau3 / tau
    B1 = (A1/6) * (tau**2 - tau3**2)
    A3 = -tau1/tau
    B3 = (A3/6) * (tau**2 - tau1**2)
    
    A = (A1*D21 - D22 + A3*D23)/(-D0)
    B = (B1*D21 + B3*D23)/(-D0)
    E = -2*np.dot(rhohat2, Sun2)
    Sun2_mag = get_vector_magnitude(Sun2)
    F = Sun2_mag**2
    
    
    a = -(A**2 + A*E + F)
    b = -(2*A*B + B*E)
    c = -B**2

    #r2**8 + a*r2**6 + b*r2**3 + c = 0
    coeff = [c, 0, 0, b, 0, 0, a, 0, 1]
    roots_tot = np.polynomial.polynomial.polyroots(coeff)
    #NTS: gives 9 possibel answers, only need positive ones

    #print('roots_tot ', roots_tot)
    roots = []
    rhos = []
    for i in range(len(roots_tot)):
        if roots_tot[i] >= 0:
            roots.append(float(roots_tot[i]))

    for i in range(len(roots)):
        rho2 = A + B / (roots[i]**3)
        rhos.append(float(rho2))
        
    return roots, rhos, A1, B1, A3, B3


#---Getting pos/vel vectors---
#NTS: the range unit vector lets you go from ra and dec to pos_vec, or pos_vec to RA and dec, figure out a way to make it into a function that can perform both in either way (f and g 2)
k = 0.0172020989484
cAU = 173.144643267 # speed of light in AU/(mean solar)day
eps_deg = 23.4374 # Earth's obliquity in degrees

range_vec = 0 #range vector
def range_uvec_4_pos_vec(RA, dec):
    range_unit_vec = np.array([ (np.cos(RA)*np.cos(dec)) , (np.sin(RA)*np.cos(dec)) , (np.sin(dec)) ])
    return range_unit_vec

def get_tau(t1, t2, t3):
    tau1 = k*(t1 - t2) #always negative
    tau3 = k*(t3 - t2)
    tau0 = k*(t3 - t1)
    return tau1, tau3, tau0

def get_Ds(p_hat1,p_hat2,p_hat3,earth_sun1,earth_sun2,earth_sun3):
    D0 = np.dot(p_hat1, np.cross(p_hat2, p_hat3))
    D11 = np.dot(np.cross(earth_sun1, p_hat2), p_hat3)
    D21 = np.dot(np.cross(p_hat1, earth_sun1), p_hat3)
    D31 = np.dot(p_hat1, np.cross(p_hat2, earth_sun1))

    D12 = np.dot(np.cross(earth_sun2, p_hat2), p_hat3)
    D22 = np.dot(np.cross(p_hat1, earth_sun2), p_hat3)
    D32 = np.dot(p_hat1, np.cross(p_hat2, earth_sun2))

    D13 = np.dot(np.cross(earth_sun3, p_hat2), p_hat3)
    D23 = np.dot(np.cross(p_hat1, earth_sun3), p_hat3)
    D33 = np.dot(p_hat1, np.cross(p_hat2, earth_sun3))
    return D0, D11, D21, D31, D12, D22, D32, D13, D23, D33
    
def get_p_scalar(p_hat1, p_hat2, p_hat3, earth_sun1, earth_sun2, earth_sun3, c1, c2, c3):

    D0, D11, D21, D31, D12, D22, D32, D13, D23, D33 = get_Ds(p_hat1,p_hat2,p_hat3,earth_sun1,earth_sun2,earth_sun3)

    #calculate pscalarj and add it to the list
    p_scalar1 = (c1*D11 + c2*D12 + c3*D13)/(c1*D0)
    p_scalar2 = (c1*D21 + c2*D22 + c3*D23)/(c2*D0)
    p_scalar3 = (c1*D31 + c2*D32 + c3*D33)/(c3*D0)
    return p_scalar1, p_scalar2, p_scalar3


#for 1st guess
def get_pos_vec(RA1, dec1, RA2, dec2, RA3, dec3, earth_sun1, earth_sun2, earth_sun3, t1, t2, t3):
    tau1, tau3, tau0 = get_tau(t1, t2, t3)

    #range unit vectors
    p_hat1 = range_uvec_4_pos_vec(RA1, dec1)
    p_hat2 = range_uvec_4_pos_vec(RA2, dec2)
    p_hat3 = range_uvec_4_pos_vec(RA3, dec3)

    #change unit vectors from equatorial to ecliptic
    #NTS earth tilt needs to be negative for some f reason
    rotation_earth_tilt2ecliptic = np.array([
    [1, 0, 0],
    [0, np.cos(-earth_tilt_deg), -np.sin(-earth_tilt_deg)],
    [0, np.sin(-earth_tilt_deg), np.cos(-earth_tilt_deg)]
    ])
    
    p_hat1 = rotation_earth_tilt2ecliptic @ p_hat1
    p_hat2 = rotation_earth_tilt2ecliptic @ p_hat2
    p_hat3 = rotation_earth_tilt2ecliptic @ p_hat3

    D0, D11, D21, D31, D12, D22, D32, D13, D23, D33 = get_Ds(p_hat1,p_hat2,p_hat3,earth_sun1,earth_sun2,earth_sun3)
    Ds = [D0, D21, D22, D23]

    roots, rhos, A1, B1, A3, B3 = SEL(tau1, tau3, tau0 ,earth_sun2,p_hat2,Ds)
    #print('roots: ', roots)
    #print('rhos: ', rhos)

    #check if rhos are positive
    pos_rho_roots = []
    for i in range(len(rhos)):
        if rhos[i] > 0:
            pos_rho_roots.append(roots[i])
   
    print(pos_rho_roots)
    r_u = np.real(pos_rho_roots)#???

    c1 = tau3/tau0
    c2 = -1
    c3 = -tau1/tau0
    '''
    #print('r_u ', r_u)
    #get scalar c
    u2 = 1/r_u**3
    c1 = A1 + u2 * B1
    c2 = -1
    c3 = A3 + u2 * B3
    '''
    #print('c1, c2, c3', c1, c2, c3)

    p_scalar1, p_scalar2, p_scalar3 = get_p_scalar(p_hat1, p_hat2, p_hat3, earth_sun1, earth_sun2, earth_sun3, c1, c2, c3)
    #print('rho scalar:', p_scalar1, p_scalar2, p_scalar3)
       
    #fundamental triangle
    pos_vec_1 = p_scalar1*p_hat1 - earth_sun1
    pos_vec_2 = p_scalar2*p_hat2 - earth_sun2
    pos_vec_3 = p_scalar3*p_hat3 - earth_sun3

    #print('pos_vec_1 ', pos_vec_1)
    #print('pos_vec_2 ', pos_vec_2)
    #print('pos_vec_3 ', pos_vec_3)


    return pos_vec_1, pos_vec_2, pos_vec_3, p_scalar2, r_u

#NTS: try to get less input variable, change stuff in OD5
def get_vel_vec2(pos_vec_1, pos_vec_2, pos_vec_3, t1, t2, t3, r_u):
    #Should do this in the main function
    tau1, tau3, tau0 = get_tau(t1, t2, t3)

    u = 1/(r_u**3)

    f1 = 1 - (0.5 * (u * tau1**2))
    g1 = tau1 - (1/6 * (u * (tau1**3)))
    f3 = 1 - (0.5 * (u * tau3**2))
    g3 = tau3 - (1/6 * (u * (tau3**3)))

    d1 = -f3/(f1*g3 - f3*g1)
    d3 = f1/(f1*g3 - f3*g1)

    #print('d1, d3 ', d1, d3)

    v21 = (pos_vec_2 - pos_vec_1)/tau1
    v23 = (pos_vec_3 - pos_vec_2)/tau3

    vel_vec_2 = (-tau3 * v21 + tau1 * v23)/tau0

    #vel_vec_2 = d1*pos_vec_1 + d3*pos_vec_3
    #print(pos_vec_1, pos_vec_2, pos_vec_3)
    print(vel_vec_2)
    
    return vel_vec_2
    
    #ultimate goal: figure out each position/velocity vector
    #r_vec_i = p_scalar_i*range_unit vec - earth_sun_i

#---F & G Function---
def calculate_fg(pos_vec, vel_vec, tau, order_4):

    pos_vec_mag = get_vector_magnitude(pos_vec)

    u = 1/(pos_vec_mag**3)
    z = np.dot(pos_vec, vel_vec)/pos_vec_mag**2
    q = np.dot(vel_vec, vel_vec)/pos_vec_mag**2
    
    f = 1 - (u*tau**2)/2 + (u*z*tau**3)/2
    g = tau - (u*tau**3)/6

    if order_4 == True:
        f = f + (3*u*q - 15*u*z**2 + u**2)*(tau**4)/24
        g = g + (u*z*tau**4)/4
    
    return f, g


def get_new_vec(pos_vec_1, pos_vec_2, pos_vec_3, vel_vec_2, earth_sun1, earth_sun2, earth_sun3, p_hat1, p_hat2, p_hat3, t1, t2, t3):
    #print('pos_vec_2 ', pos_vec_2)

    tau1, tau3, tau0 = get_tau(t1, t2, t3)

    f1, g1 = calculate_fg(pos_vec_2, vel_vec_2, tau1, True)
    f3, g3 = calculate_fg(pos_vec_2, vel_vec_2, tau3, True)

    c1 = g3/(f1*g3 - f3*g1)
    c2 = -1
    c3 = -g1/(f1*g3 - f3*g1)

    #print('c1 ',c1)
    #print('c3 ',c3)

    p_scalar1, p_scalar2, p_scalar3 = get_p_scalar(p_hat1, p_hat2, p_hat3, earth_sun1, earth_sun2, earth_sun3, c1, c2, c3)

    #print(p_scalar1, p_scalar2, p_scalar3)
    
    d1 = -f3/(f1*g3 - f3*g1)
    d3 = f1/(f1*g3 - f3*g1)

    #new_pos_vec2 = c1*(f1*pos_vec_2 + g1*vel_vec_2) + c3*(f3*pos_vec_2 + g3*vel_vec_2)
    
    new_pos_vec1 = p_scalar1*p_hat1 - earth_sun1
    new_pos_vec2 = p_scalar2*p_hat2 - earth_sun2
    new_pos_vec3 = p_scalar3*p_hat3 - earth_sun3

    new_vel_vec2 = d1*new_pos_vec1 + d3*new_pos_vec3
    new_vel_vec2 = k * new_vel_vec2

    return new_pos_vec2, new_vel_vec2, p_scalar2
