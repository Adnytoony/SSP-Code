# NAME Ariadna Monzon
# DATE 06/12
# PURPOSE OF THIS CODE

def vector_magnitude(vec):
    # Returns the length of the vector "vec" (list)
    # YOUR CODE HERE
    sq = 0
    for i in vec:
        sq += i**2
    return sq**(1/2)

def dot_product(vec1, vec2):
    # Returns the dot product of "vec1" (list) and "vec2" (list)
    # These vectors must have the same number of elements

    # Prevents this function from running if vec1 and vec2 have a different number of elements
    assert len(vec1)==len(vec2), 'vec1 and vec2 must have the same length'
    dot_prod = 0
    # YOUR CODE HERE
    for i in range(len(vec1)):
        dot_prod += (vec1[i]*vec2[i])
    return dot_prod
   
def cross_product(vec1, vec2):
    # Returns the cross product of "vec1" (list) and "vec2" (list)
    # Each vector must have exactly 3 elements

    # Prevents this function from running if vec1 or vec2 have the wrong number of elements
    assert len(vec1)==3, 'vec1 must have exactly 3 elements'
    assert len(vec2)==3, 'vec2 must have exactly 3 elements'

    # YOUR CODE HERE
    cross_prod=[]
    for i in range(len(vec1)):
        if i == 0:
            cross_prod.append(vec1[1]*vec2[2] - vec1[2]*vec2[1])
        elif i == 1:
            cross_prod.append(vec1[2]*vec2[0] - vec1[0]*vec2[2])
        else:
            cross_prod.append(vec1[0]*vec2[1] - vec1[1]*vec2[0])
    return cross_prod

def main():

    print('TESTING: vector_magnitude')
    print()
    print('Actual:  ', vector_magnitude([1]))
    print('Expected:', 1)
    print()
    print('Actual:  ', vector_magnitude([1, 1, -1, -1]))
    print('Expected:', 2)
    print()
    print('Actual:  ', vector_magnitude([10, -10]))
    print('Expected:', 14.142136)
    print()

    ####################

    print('TESTING: dot_product')
    print()
    print('Actual:  ', dot_product([], []))
    print('Expected:', 0)
    print()
    print('Actual:  ', dot_product([2,4], [1,1]))
    print('Expected:', 6)
    print()
    print('Actual:  ', dot_product([2,5,6], [3,7,8]))
    print('Expected:', 89)
    print()
    print('Actual:  ', dot_product([1,2,3], [4,5,6]))
    print('Expected:', 32)
    print()
    print('Actual:  ', dot_product([0,0,0], [3,7,8]))
    print('Expected:', 0)
    print()
    
    # Are there any simple cases you can check?

    ####################
    
    print('TESTING: cross_product')
    print()
    print('Actual:  ', cross_product([1,0,0], [0,1,0]))
    print('Expected:', [0,0,1])
    print()
    print('Actual:  ', cross_product([2,5,6], [3,7,8]))
    print('Expected:', [-2,2,-1])
    print()
    print('Actual:  ', cross_product([1,2,3], [4,5,6]))
    print('Expected:', [-3,6,-3])
    print()
    print('Actual:  ', cross_product([0,0,0], [3,7,8]))
    print('Expected:', [0,0,0])
    print()
   
    # Are there any simple cases you can check?