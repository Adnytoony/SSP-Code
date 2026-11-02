#NAME
#DATE
#PURPOSE OF THIS CODE
#COLLABORATIONS

import matplotlib.pyplot as plt

def letter_to_bits(letter):
    #this function should take a letter of english alphabet (and " " as well) and convert it to binary number with length of 5
    #YOUR CODE HERE
    
    
    
    #----
    bits = format(n, "05b") # this line converts a number (from 0 to 26) to binary number with length of 5
    # replace n to the variable that stores your number
    return bits

def encode_image(input_image, output_image, message):
    img = plt.imread(input_image)
    img = (img * 255).astype(int)
    pixels = img[:, :, 0].flatten() # this is a list of red values for pixels in 1d array
    #this function inputs 'message', encodes it into 'input_image' and creates a new picture called 'output_image'
    #YOUR CODE HERE
    
    
    
    #---
    img[:, :, 0] = pixels.reshape(img.shape[0], img.shape[1])
    img = img.astype("uint8")
    plt.imsave(output_image, img)
    print("Encoded successfully")


def bits_to_letter(bits):
    #this function converts 5-digit-long binary numbers to letters of english alphabet
    #YOUR CODE HERE
    
    pass


def decode_image(image_path):
    img = plt.imread(image_path)
    img = (img * 255).astype(int)
    pixels = img[:, :, 0].flatten() # this is a list of red values for pixels in 1d array
    #YOUR CODE HERE
    
    pass