
import numpy
import pygame
from pygame.locals import *

import model


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
              


def set_view(w, h, scale):
    
    width = w * scale
    height = h * scale
    
    display = pygame.display.set_mode((width, height))
    display.fill(WHITE)
    surface = pygame.Surface((width, height))

    return [display, surface]


def tick(matrix, surface, scale):

    for (x, y), value in numpy.ndenumerate(matrix):
        if value == 1:
            pygame.draw.rect(
                    surface, 
                    BLACK, 
                    ((x * scale, y * scale), 
                     (scale, scale)))
    
def loop(width, height, scale, val):
    
    if val == 1:
        seed = BLINKER
    else:
        seed = TOAD
    
    
    clock = pygame.time.Clock()
    display, surface = set_view(width, height, scale)
    
    matrix = model.first_generation(height, width, seed)

    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
                pygame.quit()
        
        tick(matrix, display, scale)
        pygame.display.update()
        clock.tick(20)
        matrix = model.next_generation(matrix)
        display.fill(WHITE)


def main():
    loop(100, 100, 6, 1)


if __name__ == '__main__':
    main()
