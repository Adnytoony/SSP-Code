# NAME Ariadna Monzon
# DATE 06/20/26
# PURPOSE OF THIS CODE localize the pixel with the highest value in an image and find its coordinates

import numpy as np
import matplotlib.pyplot as plt


def get_centroid(grid):
    # Computes the centroid of "grid", an N-by-N array of pixels
    
    # YOUR CODE HERE
    centroid_x = 0
    centroid_y = 0
    all_lums = np.sum(grid[:])
    #print("w_i is", all_lums)

    for r in range(len(grid[:])): #for every row in the grid
        #add up all the luminosities and multiply them by its row number
        centroid_x += np.sum(grid[r,:])*(r)
        #divide that result by all the luminosities
    centroid_x = centroid_x / all_lums

    for c in range(grid.shape[1]): #for every colums in the grid
        #print(c)
        #add up all the luminosities and multiply them by its column number
        centroid_y += np.sum(grid[:,c])*(c)
        #divide that result by all the luminosities
        #print(centroid_y)
    centroid_y = centroid_y / all_lums

    plt.imshow(grid)
    plt.scatter(centroid_y,centroid_x)
    return (float(centroid_x), float(centroid_y)) #coordinates of centroid
    

def get_subgrid(image_grid, row_center, col_center, grid_size):
    # Returns a subgrid of "image_grid". Its center should be "row_center", "col_center", and its side length should be "grid_size"
    # "grid_size" must be positive & odd
    assert grid_size > 0 and grid_size % 2 == 1
    
    index = grid_size//2
    #column starts half of the grid_size before and ends half of the grid_size after
    #row starts half of the grid_size before and ends half of the grid_size after + 1 for the center
    sub_grid = image_grid[(row_center - index):(row_center + index+1),(col_center - index):(col_center + index+1)]
    #make a new grid that is half of grid_size from the before and after the row-center and column_center
    return sub_grid


def get_centroid_from_image(image_grid, row_center, col_center, grid_size):
    # Given "image_grid", an array of pixels representing an image, computes the centroid at ("row_center", "col_center") using a subgrid of size "grid_size"
    # "grid_size" must be positive & odd
    assert grid_size > 0 and grid_size % 2 == 1
   
    # find the subgrid of those coordinates
    sub_grid = get_subgrid(image_grid, row_center, col_center, grid_size)
    
    #find the centroid of that subgrid and assign its column and row within that index
    c_cent, r_cent = get_centroid(sub_grid) 
    
    #the center of the subgrid will always have a column and row that is half the grid size
    index_center = grid_size//2 
    
    #the x of the centroid is the the center of the subgrid + the difference between the row of the center and the row of the centroid
    centroid_x = row_center + (index_center - r_cent)
    
    #the y of the centroid is the the center of the subgrid + the difference between the column of the center and the column of the centroid
    centroid_y = col_center + (index_center - c_cent)

    
    return (centroid_x, centroid_y)
    

def main():

    # Small grid for testing get_centroid
    # The centroid is approximately: row = 2.191 and column = 1.182 
    test_grid_small = np.array([
        [0, 33, 21, 33, 8],
        [0, 56, 51, 53, 26],
        [23, 120, 149, 73, 18],
        [55, 101, 116, 50, 16],
        [11, 78, 26, 2, 10],
    ])

    print('--- Testing: get_centroid ---')

    # YOUR TESTS HERE
    print(get_centroid(test_grid_small))
    
    
    ########################################

    # Larger grid for testing get_subgrid and get_centroid_from_image
    # All values are 0 except for the one at row=30, col=70
    test_image = np.zeros([100, 100])
    test_image[30, 70] = 1
    
    print('--- Testing: get_subgrid ---')
    print(get_subgrid(test_image, 30,70,5))

    # YOUR TESTS HERE

    ########################################

    print('--- Testing: get_centroid_from_image ---')

    # YOUR TESTS HERE
    print('Expected: 30, 70')
    print('Actual: ', get_centroid_from_image(test_image, 29, 71, 5))
    
