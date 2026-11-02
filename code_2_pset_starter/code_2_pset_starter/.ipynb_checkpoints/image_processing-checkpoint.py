# NAME Ariadna Monzon
# DATE 06/15/26
# PURPOSE OF THIS CODE image_processing used to change individual pixels in any image

import matplotlib.pyplot as plt
import numpy as np

def create_inverted(image_filename):
    # Reads the image ("image_filename") and returns a color-inverted version        

    # Reads the image
    image = plt.imread(image_filename)

    # YOUR CODE HERE
    return 1- image[:] # returns 1 minus every pixel read by the variable
    

def create_grayscale(image_filename):
    # Reads the image ("image_filename") and returns it in grayscale
    
    # Reads the image
    image = plt.imread(image_filename)

    # YOUR CODE HERE
    gray = (image[:,:,0] + image[:,:,1] + image[:,:,2])/3 #gray is equal to the average of all the colors
    image[:,:,0] = gray #turn all reds to gray
    image[:,:,1] = gray #turn all greens to gray
    image[:,:,2] = gray #turn all blue to gray
    
    
    return image


def create_bluescreen(image_filename, background_filename):
    # Reads the main image ("image_filename") and the background image ("background_filename"),
    # and returns the main image with every blue pixel replaced by the background image

    # Reads the two images
    image = plt.imread(image_filename)
    background = plt.imread(background_filename)

   
    # YOUR CODE HERE
    #return the image with the background change
    for row in range(image.shape[0]):     #for every row in the image
       for col in range(image.shape[1]):     #for every column in the image
           if image[row, col, 2] > (image[row, col, 0] + image[row, col, 1]): #if pixel's blue value is bigger than the red and green values combined
               image[row,col, :] = background[row,col, :] #make every pixel of the image to every pizel of the background

    #𝐵 > 𝑅 + 𝐺
    return image # Remove this when you write your own code

