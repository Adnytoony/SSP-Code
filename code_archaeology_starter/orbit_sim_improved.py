# Dr. Sum R. Science
# Mar 14, 20XX
# Orbital simulation code

import numpy as np
import matplotlib.pyplot as plt


#compute acceleration
#compute velocity
#compute position

# constants
NEWTONS_AU = 1.4882e-34 #in AU^3/kg*day
NEWTONS_SI = 6.6743e-11 #in m^3/kg*s^2
SUN_MASS_kg = 1.98841e30
fg_const = 1.4882e-34 * 1.98841e30


vec_mag = 0
#func compute magnitude
def magnitude(pos_vec):
    vec_mag = np.sqrt(np.sum(pos_vec**2))
    return vec_mag

#func compute acceleration
def acceleration(pos_vec,vel_vec):
    gravity = -NEWTONS_AU*SUN_MASS_kg
    vec_mag = magnitude(pos_vec)
    return vel_vec + (gravity/vec_mag)*(pos_vec)

def main():

    plt.figure(figsize=(6,6))
    
    r_val = np.array([-1.0, 0]) #position vector
    v_val = np.array([0, -0.0172]) #velocity vector
    
    obj1_plot = [r_val.copy()]
    t_step = 1
    n = int(200 / t_step)
    
    r2x = -1.1315
    r2y = -0.2949
    v2x = 0.0043
    v2y = -0.0129
    
    H2_list = [[r2x, r2y]]

    #r1_mag = np.sqrt(np.sum(r_val**2))
    
    for i in range(n):
        # object 1
        v_val += acceleration(r_val, v_val) #computing velocity w/ acceleration ob1
        r_val += v_val * t_step
        obj1_plot.append(r_val.copy())
        
        # adding the second object
        r2_mag = np.sqrt(r2x**2 + r2y**2)
        v2x, v2y = np.array([v2x, v2y]) + (-fg_const / r2_mag**3 * r_val) #computing velocity w/ acceleration ob2
        r2x += v2x * t_step
        r2y += v2y * t_step

        H2_list.append([r2x, r2y])

    # object 1
    plt.scatter(r_val[0], r_val[1], s=50, c='b', label='Object 1')
    r1_history_array = np.array(obj1_plot)
    plt.plot(r1_history_array[:, 0], r1_history_array[:, 1], color='b', linestyle='--')

    #star
    plt.scatter(0, 0, marker='*', color='gold', s=150)
    
    # object 2
    plt.scatter(r2x, r2y, s=50, c='r', label='Object 2') 
    plt.plot(np.array(H2_list)[:, 0], np.array(H2_list)[:, 1], color='r', linestyle='--')
    plt.grid(linestyle=':')

    
    
    #plotting graph
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.title('Orbital simulation result')
    plt.xlabel('x (AU)')
    plt.ylabel('y (AU)')
    plt.legend()
    plt.show()