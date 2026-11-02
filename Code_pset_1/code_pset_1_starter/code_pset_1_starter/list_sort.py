
def get_minimum(list_min):
    assert len(list_min) > 0, 'list_min must not be empty'
    list_min_1 = list_min[0]
    for a in range(len(list_min)):
        for i in list_min:
            if i > list_min_1:
                continue
            else:
                list_min_1 = i
    return list_min_1

def remove_minimum(list_min):
    assert len(list_min) > 0, 'list_min must not be empty'
    list_min.remove(get_minimum(list_min))
    return list_min

def sort_list(list_min):
    sorted_list = []
    assert len(list_min) > 0, 'list_min must not be empty'
    for a in range(len(list_min)):
        sorted_list.append(get_minimum(list_min))
        remove_minimum(list_min)
    return sorted_list
            

def main():
    print('TESTING: get_minimum')
    print()
    print('Actual:  ', get_minimum([0,1,2]))
    print('Expected:', 0)
    print()
    print('Actual:  ', get_minimum([8,7,6,5,4,3]))
    print('Expected:', 3)
    print()
    print('Actual:  ', get_minimum([1,2,0,5,6]))
    print('Expected:', 0)
    print()
    print('Actual:  ', get_minimum([0,0,0]))
    print('Expected:', 0)
    print()
    print('Actual:  ', get_minimum([0.3,0.5,0.1]))
    print('Expected:', 0.1)
    print()
    print('Actual:  ', get_minimum([-1,-5,-3]))
    print('Expected:', -5)
    print()

    print('TESTING: remove_minimum')
    print()
    print('Actual:  ', remove_minimum([0,1,2]))
    print('Expected:', [1,2])
    print()
    print('Actual:  ', remove_minimum([8,7,6,5,4,3]))
    print('Expected:', [8,7,6,5,4])
    print()
    print('Actual:  ', remove_minimum([1,2,0,5,6]))
    print('Expected:', [1,2,5,6])
    print()
    print('Actual:  ', remove_minimum([0,0,0]))
    print('Expected:', [0,0])
    print()
    print('Actual:  ', remove_minimum([0.3,0.5,0.1]))
    print('Expected:', [0.3,0.5])
    print()
    print('Actual:  ', remove_minimum([-1,-5,-3]))
    print('Expected:', [-1,-3])
    print()

    print('TESTING: list_sort')
    print()
    print('Actual:  ', sort_list([0,1,2]))
    print('Expected:', [0,1,2])
    print()
    print('Actual:  ', sort_list([8,7,6,5,4,3]))
    print('Expected:', [3,4,5,6,7,8])
    print()
    print('Actual:  ', sort_list([1,2,0,5,6]))
    print('Expected:', [0,1,2,5,6])
    print()
    print('Actual:  ', sort_list([0,0,0]))
    print('Expected:', [0,0,0])
    print()
    print('Actual:  ', sort_list([0.3,0.5,0.1]))
    print('Expected:', [0.1,0.3,0.5])
    print()
    print('Actual:  ', sort_list([-1,-5,-3]))
    print('Expected:', [-5,-3,-1])
    print()
    