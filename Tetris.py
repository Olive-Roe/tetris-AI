import pygame, sys
import random

cell_size = 18
cols = 10
rows = 20
maxfps = 30

colours = [
  (0, 255, 255),
  (0, 0, 255),
  (255, 165, 0),
  (255, 255, 0),
  (0, 255, 0),
  (255, 0, 0),
  (255, 0, 255)
]

shapes = [
  
     [['I', 'I', 'I', 'I']],

    [['J', 0, 0],
     ['J', 'J', 'J'],

    [[0, 0, 'L'],
     ['L', 'L', 'L']],

    [['O', 'O'],
     ['O', 'O']],

    [[0, 'S', 'S'],
     ['S', 'S', 0]],

    [['Z', 'Z', 0],
     [0, 'Z', 'Z']],

     [['T', 'T', 'T'],
     [0, 'T', 0]],
]]

class Tetris(object):
      def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        self.width = cell_size * (cols + 6)
        self.height = cell_size * rows
        self.rlim = cell_size * cols
        self.bground_grid = [[ 0 for x in range(cols)] for y in range(rows)]

        self.default_font = pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)  # We do not need
        # mouse movement
        # events, so we
        # block them.
        self.next_stone = shapes[rand(len(shapes))]
        self.init_game()
        
def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]
