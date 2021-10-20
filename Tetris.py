import pygame, sys
import random

cell_size = 18
cols = 10
rows = 20
maxfps = 30

S = [['.....',
      '..00..',
      '.00...',
      '......',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....'],
     ['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '..0..',
      '.....'],
     ]

Z = [
     ['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],
      '.0...',
     ['.0...',
      '.0...',
      '.0...',
      '.....'],

     ]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

colours = [
  (0, 255, 255),
  (0, 0, 255),
  (255, 165, 0),
  (255, 255, 0),
  (0, 255, 0),
  (255, 0, 0),
  (255, 0, 255)
]
colours_dict = {
  "I": (0, 255, 255),
  "J": (0, 0, 255),
  "L": (255, 165, 0),
  "O": (255, 255, 0),
  "S": (0, 255, 0),
  "Z": (255, 0, 0),
  "T": (255, 0, 255)
}

shapes = ["I", "J", "L", "O", "S", "Z", "T"]
class piece(object):
  rows = 20
  colms = 10
  
  def __init__(self, colms, rows, shape):
    self.x = colms
    self.y = rows
    self.shape = shape
    self.color = colours[shapes.index(shape)]
    self.rotation = 0

def create_grid(locked_positions={}):
      grid = [[(0,0,0) for x in range(10)] for x in range(20)]
      for row in range(len(grid)):
          for col in range(len(grid[1])):
              if (row,col) in locked_positions:
                  c = locked_positions[(row,col)]
                  grid[row][col] = c
      return grid

'20/20/20/20/20/20/20/20/20/20/20' #example board notation
'16TJOL/20/20/20/20/20/20/20/20/20' #another example
def board_notation_to_dict(notation): #this should work, might need more testing
      global colours_dict
      output_list = []
      for row in notation.split("/"):
            for index in range(len(row)):
                  item = row[index]
                  if item.isnumeric() == False:
                        output_list.append(colours_dict[item])
                  else:
                        if index < len(row) - 1:
                              if row[index+1].isnumeric() == True:
                                    num_of_empty_cells = int(row[index] + row[index+1])
                                    for i in range(num_of_empty_cells):
                                          output_list.append((0, 0, 0))
      indices = [(x, y) for x in range(20) for y in range(10)]
      items_list = [(indices[i], output_list[i]) for i in range(200)]
      return {k:v for (k, v) in items_list}

#testing commands, these work
#dict1 = board_notation_to_dict('16TJOL/20/20/20/20/20/20/20/20/19Z')
#print(create_grid(locked_positions=dict1))
            

