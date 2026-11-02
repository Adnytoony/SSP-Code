# NAME Ariadna Monzon
# DATE 06/15/26
# PURPOSE OF THIS CODE rotate vectors around origin for angle theta

import numpy as np



def rotate_2d(vec2d, theta_rad):
    # Returns the vector "vec2d" rotated by "theta_rad" radians
   
    # YOUR CODE HERE
    vec2d_new = np.array(vec2d) #assigns the variable vec2d to a new variable to avoid editing original variable
    rotation_matrix = np.array([
    [np.cos(theta_rad),-1*np.sin(theta_rad)],
    [np.sin(theta_rad),np.cos(theta_rad)]
    ]) #matrix of rotation for variable theta
    vec2d_new = rotation_matrix @ vec2d_new # matrix multiplication operator to rotate x and y of given vector by angle theta
    return vec2d_new #returns the new vector after rotation


def print_test_result(actual, expected):
    # A helper function for printing out tests. Prints "actual", "expected", and "actual-expected"
    print('Actual:  ', actual)
    print('Expected:', expected)
    print('Difference:', actual-expected)
    if np.any(np.abs(actual-expected) > 1e-4):
        print('ERROR: Difference is too large!')
    print()

def main():
    
    print('TESTING: rotate_2d')
    print()

    # Rotates the x-unit vector [1, 0]
    print_test_result(rotate_2d(np.array([1,0]), 0), np.array([1,0]))
    print_test_result(rotate_2d(np.array([1,0]), np.pi/2), np.array([0,1]))
    print_test_result(rotate_2d(np.array([1,0]), np.pi), np.array([-1,0]))
    
    # Rotates the y-unit vector [0, 1]
    print_test_result(rotate_2d(np.array([0,1]), 0), np.array([0,1]))
    print_test_result(rotate_2d(np.array([0,1]), np.pi/2), np.array([-1,0]))

    # Rotates more complicated vectors
    print_test_result(
        rotate_2d(np.array([3,7]), 1.7*np.pi),
        np.array([7.42647472, 1.68744578])
    )
    print_test_result(
        rotate_2d(np.array([-100, 300]), -0.1*np.pi),
        np.array([-2.40055332, 316.21865433])
    )

