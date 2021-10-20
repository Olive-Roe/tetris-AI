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

pieces = {"I":I, "J": J, "L": L, "O": O, "S": S, "Z": Z, "T": T}
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
'09O05I04/16I03/17I02/18I01/19I/19I/18I01/17I02/16I03/09O05I04' #smileyface test
#remember to use 03 format for single-digit numbers

def board_notation_to_dict(notation): #this should work, might need more testing
      global colours_dict
      output_list = []
      for row in notation.split("/"):
            for index in range(len(row)):
                  item = row[index]
                  if item.isnumeric() == False:
                        output_list.append(colours_dict[item])
                  elif index < len(row) - 1:
                        if row[index+1].isnumeric() == True:
                              num_of_empty_cells = int(row[index] + row[index+1])                                    
                              for i in range(num_of_empty_cells):
                                    output_list.append((0, 0, 0))
      indices = [(x, y) for x in range(20) for y in range(10)]
      try:
            items_list = [(indices[i], output_list[i]) for i in range(200)]
      except:
            print(output_list)
            raise ValueError(f"Invalid board notation. Length of output_list: {len(output_list)}")
      return {k:v for (k, v) in items_list}

def boardstate_to_extended_boardstate(boardstate:str):
      output_list = []
      for row in boardstate.split("/"):
            for index in range(len(row)):
                  item = row[index]
                  if index < len(row) - 1:
                        if row[index].isnumeric() == True:
                              if row[index+1].isnumeric() == True:
                                    num_of_empty_cells = int(row[index] + row[index+1])                                    
                                    for i in range(num_of_empty_cells):
                                          output_list.append(".")
                        else:
                              output_list.append(item)
            output_list.append("/")
      return "".join(output_list)[:-1] #to get rid of final slash

def extended_boardstate_to_boardstate(extended_boardstate:str):
      output_list = []
      for row in extended_boardstate.split("/"):
            counter = 0
            for item in row:
                  if item == ".":
                        counter += 1
                  else:
                        if counter != 0:
                              if counter < 10: output_list.append("0" + str(counter))
                              else: output_list.append(str(counter))
                              counter = 0
                        output_list.append(item)
            if counter != 0:
                  if counter < 10: output_list.append("0" + str(counter))
                  else: output_list.append(str(counter))
            output_list.append('/')
      return "".join(output_list)[:-1] #to get rid of final slash
      

def access_cell(boardstate:str, row:int, column:int):
      'Given a boardstate, row, and column of a cell (starting from index 0), return the value of the cell in the boardstate.'
      b = boardstate_to_extended_boardstate(boardstate)
      return boardstate.split("/")[row][column]

def change_cell(boardstate:str, row:int, column:int, val:str): #needs work, does not work
      'Given a boardstate, row, column of a cell (starting from index 0), and a value, update the boardstate and return it.'
      row = int(row)
      column = int(column)
      new_boardstate = str(boardstate)
      print(new_boardstate.split("/"))
      [i for i in new_boardstate.split("/")[row]][column] = val
      return "/".join(new_boardstate)

#Example piece notation
'S038' #S piece in spawn orientation (0) in column 3, row 8 

def update_boardstate(current_boardstate:str, piece_notation:str):
      'Given a boardstate and a piece notation, return the updated boardstate.'
      def findBLC(shape): #finding bottom left corner of a shape
            for r in range(5):
                  for c in range(5):
                        if shape[4-r][c] == "0":
                              return (c, r)
            return (None, None)
      global pieces
      #initalize local variables
      piece = piece_notation[0]
      orientation = int(piece_notation[1])
      #column, row refer to leftmost, bottommost cell of piece
      column = int(piece_notation[2])
      if len(piece_notation) == 4:
            row = int(piece_notation[3])
      #Finding the center of the 'bounding box'
      shape = pieces[piece][orientation]
      bl_row, bl_col = findBLC(shape) #bottom left row and column
      assert bl_row != None and bl_col != None
      rdif = 2-bl_row
      cdif = 2-bl_col
      center = (row+rdif, column+rdif)
      #Checking whether the piece will fit in the given boardstate
      board = [i for i in current_boardstate.split("/")]
      nbs = boardstate_to_extended_boardstate(current_boardstate) #new board state
      print(nbs)
      oList = []
      for r in range(5):
            for cell in range(5):
                  if shape[r][cell] == "0":
                        oList.append((cell-2, 2-r))
      for change_in_x, change_in_y in oList:
            cx, cy = center
            x = cx+change_in_x
            y = cy+change_in_y
            if access_cell(nbs, x, y) == ".": 
                  change_cell(nbs, x, y, piece)
            else:
                  raise ValueError("This piece cannot be placed in this location")
      return (extended_boardstate_to_boardstate(nbs))

#testing commands, these work
#dict1 = board_notation_to_dict('09O05I04/16I03/17I02/18I01/19I/19I/18I01/17I02/16I03/09O05I04')
#print(create_grid(locked_positions=dict1))
            
#working test function
#a = boardstate_to_extended_boardstate('09O05I04/16I03/17I02/18I01/19I/19I/18I01/17I02/16I03/09O05I04')
#print(a)
#print(extended_boardstate_to_boardstate(a))

#not working test functions
print(update_boardstate('16TJOL/20/20/20/20/20/20/20/20/20', 'S361'))

