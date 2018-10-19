# Adapted from:
# https://www.labri.fr/perso/nrougier/teaching/numpy/numpy.html
# All code and material is licensed 
# under a Creative Commons Attribution-ShareAlike 4.0.

# The game of life model
# Calculates a generation based on the previous one

import numpy


BLINKER = [[50, 49], [50, 50], [50, 51]]

TOAD = [[50, 49], [50, 50], [50, 51],
        [51, 48], [51, 49], [51, 50]]
        
BEACON = [[50, 50], [50, 51],
          [51, 50], [51, 51],
          [52, 52], [52,  53],
          [53, 52], [53, 53]]
          
GLIDER = [[50, 50], [51, 51], 
          [52, 49], [52, 50], [52, 51]]
          
GLIDER_GUN = [[5, 1], [5, 2], [6, 1], 
              [6, 2], [5, 11], [6, 11],
              [7, 11], [4, 12], [3, 13],
              [3, 14], [8, 12], [9, 13],
              [9, 14], [6, 15], [4, 16],
              [5, 17], [6, 17], [7, 17],
              [6, 18], [8, 16], [3, 21],
              [4, 21], [5, 21], [3, 22],
              [4, 22], [5, 22], [2, 23],
              [6, 23], [1, 25], [2, 25],
              [6, 25], [7, 25], [3, 35],
              [4, 35], [3, 36], [4, 36],[40, 50]]
              
LIFE_SPACESHIP = [[52, 50], [54, 50], [51, 51],
                  [51, 52], [51, 53], [54, 53], 
                  [51, 54], [52, 54], [53, 54]]
                  
PENTOMINO = [[50, 50], [50, 51], [49, 51], 
             [50, 52], [51, 52]]



# create a starting point for the game
# cells is a list of the coordinates
# of live cells.
def first_generation(width, height, cells):

    universe = numpy.zeros((width, height), dtype=numpy.int)

    for x, y in cells:
        universe[x, y] = 1

    return universe
        


# universe is a 'numpy.ndarray'
# the function calculates the next cell generation,
# based on the game rules.
def next_generation(universe):

    neighbours = (universe[0:-2,0:-2]
                + universe[0:-2,1:-1]
                + universe[0:-2,2:]
                + universe[1:-1,0:-2]
                + universe[1:-1,2:]
                + universe[2:  ,0:-2]
                + universe[2:  ,1:-1]
                + universe[2:  ,2:])

    # Apply rules
    
    birth = (neighbours == 3) & (universe[1:-1,1:-1] == 0)
    survive = ((neighbours == 2) | (neighbours == 3)) & (universe[1:-1,1:-1] == 1)

    universe[...] = 0
    universe[1:-1,1:-1][birth | survive] = 1
    
    return universe


# Test the functions
def main():

    Z = first_generation(10, 10, [[4, 4], [4, 5], [4, 6]])

    for i in range(4):
        print(next_generation(Z))
        print()


if __name__ == '__main__':
    main()
