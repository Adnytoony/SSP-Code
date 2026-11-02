import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    
    circle = plt.Circle((0,0),1)
    square = plt.patches.Rectangle(0, 2, 2, angle=0.0, rotation_point='xy')

    plt.title('Monte Carlo Challenge')
    plt.plot(circle, color='blue', label='Circle')
    plt.plot(square, y, color='red', label='Square')
    plt.scatter(np.random.random(), np.random.random, color='orange')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    
    #N = iterations
    
    x_sum = old_x + new_x
    mean = (x_sum)/N
    st_dev = np.sqrt((np.sum(x_sum - mean)**2/(N - 1))
    SDOM = st_dev/np.sqrt(N)
    percentage error = np.abs(actual-expected)/np.abs(expected)
