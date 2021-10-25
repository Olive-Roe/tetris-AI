import pygame, sys
import random
import kicktables

cell_size = 18
cols = 10
rows = 20
maxfps = 30

Z = [['.....',
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
      ['.....',
      '..00..',
      '.00...',
      '......',
      '.....'],
     ]

S = [['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
      ['.....',
      '...0.',
      '..00.',
      '..0..',
      '.....'],
      ['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],]

I = [
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
     ['.0...',
      '.0...',
      '.0...',
      '.0...',
      '.....'],
      ['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

L = [
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
      '.....'],
      ['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],]

J = [[
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
      '.....'],
      '.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],]

T = [['.....',
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
      '.....'],
      ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],]

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

'LIOZ4IL/JS5TSZ/SZSZ6/O9/J9' #board notation number 2

def board_notation_to_dict(notation): #this should work, might need more testing
      global colours_dict
      output_list = []
      rows = len(notation.split("/"))
      for row in notation.split("/"):
            for index in range(len(row)):
                  item = row[index]
                  if item.isnumeric() == False:
                        output_list.append(colours_dict[item])
                  else:
                        num_of_empty_cells = int(row[index])
                        for i in range(num_of_empty_cells):
                                    output_list.append((0, 0, 0))
      indices = [(x, y) for x in range(rows) for y in range(10)]
      try:
            items_list = [(indices[i], output_list[i]) for i in range(rows * 10)]
      except:
            print(output_list)
            raise ValueError(f"Invalid board notation. Length of output_list: {len(output_list)}")
      return {k:v for (k, v) in items_list}

def boardstate_to_extended_boardstate(boardstate:str):
      if boardstate == "":
            return "/.........."*20
      output_list = []
      for row in boardstate.split("/"):
            output_list2 = []
            for index in range(len(row)):
                  item = row[index]
                  if item.isnumeric() == True:
                        num_of_empty_cells = int(row[index])
                        for i in range(num_of_empty_cells):
                              output_list2.append(".")
                  else:
                        output_list2.append(item)
            if len(output_list2) != 10:
                  raise ValueError(output_list2)
            output_list.append("".join(output_list2))
      notation = "/".join(output_list)
      rows = len(notation.split("/"))
      for i in range(20-rows):
            notation = notation + "/.........."
      return notation

def extended_boardstate_to_boardstate(extended_boardstate:str):
      output_list = []
      for row in extended_boardstate.split("/"):
            if row == "..........": continue
            output_list2 = []
            counter = 0
            for item in row:
                  if item == ".": counter += 1
                  else:
                        if counter != 0:
                              output_list2.append(str(counter))
                              counter = 0
                        output_list2.append(item)
            if counter != 0:
                  output_list2.append(str(counter))
            output_list.append("".join(output_list2))
      return "/".join(output_list)

def boardstate_to_list_form(boardstate:str):
      return [[i for i in item] for item in boardstate_to_extended_boardstate(str(boardstate)).split("/")]

def list_form_to_boardstate(list_form:list):
      return "/".join(["".join(item) for item in (list_form)])

def access_cell(boardstate:str, row:int, column:int):
      'Given a boardstate, row, and column of a cell (starting from index 0), return the value of the cell in the boardstate.'
      b = boardstate_to_extended_boardstate(boardstate)
      return b.split("/")[row][column]

def change_cell(boardstate:str, row:int, column:int, val:str):
      'Given a boardstate, row, column of a cell (starting from index 0), and a value, update the boardstate and return it.'
      row = int(row)
      column = int(column)
      new_boardstate = boardstate_to_list_form(boardstate)
      new_boardstate[row][column] = val
      return list_form_to_boardstate(new_boardstate)

#Example piece notation
'S038' #S piece in spawn orientation (0) in column 3, row 8

def findBLC(shape): #finding bottom left corner of a shape
      'Given a shape, finds its bottom left corner (helper function to update_boardstate)'
      for r in range(5):
            for c in range(5):
                  if shape[4-r][c] == "0":
                        return (c, r)
      return (None, None)


def update_boardstate(current_boardstate:str, piece_notation:str): #works 3/4 of the way, still buggy
      'Given a boardstate and a piece notation, return the updated boardstate.'
      global pieces
      #initalize local variables
      piece = piece_notation[0]
      orientation = int(piece_notation[1])
      #column, row refer to leftmost, bottommost cell of piece
      column = int(piece_notation[2])
      if len(piece_notation) == 4:
            row = int(piece_notation[3])
      else:
            print(piece_notation)
      #Finding the center of the 'bounding box'
      shape = pieces[piece][orientation]
      bl_row, bl_col = findBLC(shape) #bottom left row and column
      assert bl_row != None and bl_col != None
      rdif = 2-bl_row
      cdif = 2-bl_col
      center = (row+rdif, column+cdif)
      #Checking whether the piece will fit in the given boardstate
      nbs = boardstate_to_extended_boardstate(current_boardstate) #new board state
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
                  nbs = change_cell(nbs, x, y, piece)
            else:
                  raise ValueError("This piece cannot be placed in this location")
      return (extended_boardstate_to_boardstate(nbs))

def update_boardstate_from_piece_board_notation(piece_board_notation):
      piece = piece_board_notation.split(":")[0]
      board = piece_board_notation.split(":")[1]
      return update_boardstate(board, piece)

def generate_bag(current_bag):
      'Takes a 13-long bag and adds a new piece to the end of it'
      if len(current_bag) == 14:
            return current_bag
      pieces = [p for p in "IJLOSZT"]
      output_list = []
      if current_bag == "":
            for x in range(2):
                  pieces = [p for p in "IJLOSZT"]
                  for x in range(7):
                        a = random.randint(0, len(pieces) - 1)
                        output_list.append(pieces[a])
                        pieces.pop(a)
                        #output_list.append(pieces.pop(random.randint(0, len(pieces) - 1)))
            return "".join(output_list)
      #Current bag is not empty
      assert len(current_bag) == 13
      latest_bag = []
      for piece in current_bag:
            if piece in latest_bag:
                  latest_bag = [piece]
            else:
                  latest_bag.append(piece)
      for item in latest_bag:
            if item in pieces:
                  pieces.remove(item)
      return current_bag + random.choice(pieces)

def check_kick_tables(piece, direction, test_number):
      'Takes a piece and the test number, returns the respective offset, or False if there are no more tests'
      #print(piece, direction, test_number)
      if direction == "CW": direction = 0
      elif direction == "CCW": direction = 1
      if piece == "O": return False
      elif piece == "I": table = kicktables.i_table
      elif piece in [p for p in "JLSZT"]: table = kicktables.jlszt_table
      kicktable = table[[k for k in table.keys()][direction]] #accessing kick table
      if test_number >= len(kicktable): #no more kicks
            return False
      a = kicktable[test_number][1:-1].split(", ") #converting from 
      x_offset = int(a[0])
      y_offset = int(a[1])
      return x_offset, y_offset
      

def rotate_piece(piece_board_notation, direction):
      'Takes a piece-board notation and direction'
      global pieces
      piece_notation = piece_board_notation.split(":")[0]
      piece = piece_notation[0]
      orientation = int(piece_notation[1])
      row = int(piece_notation[3])
      column = int(piece_notation[2])
      boardstate = piece_board_notation.split(":")[1]
      shape = pieces[piece][orientation]

      if direction == "CW": new_orientation = (orientation+1)%4
      if direction == "CCW": new_orientation = (orientation+3)%4 #+3 = -1
      if direction == "180": new_orientation = (orientation+2)%4
      bl_row, bl_col = findBLC(shape)
      assert bl_row != None and bl_col != None
      rdif = 2-bl_row
      cdif = 2-bl_col
      center = (row+rdif, column+cdif)
      new_shape = pieces[piece][new_orientation]
      bl_row, bl_col = findBLC(new_shape)
      assert bl_row != None and bl_col != None
      rdif = 2-bl_row
      cdif = 2-bl_col
      counter = 0
      location = [center[0]-rdif, center[1]-cdif]
      new_x_loc, new_y_loc = location[0], location[1]
      while True:
            #print(location)
            output = piece + str(new_orientation) + str(new_x_loc) + str(new_y_loc) + ":" + boardstate
            try:
                  update_boardstate_from_piece_board_notation(output)
                  break
            except:
                  var = check_kick_tables(piece, direction, counter)
                  if var == False:
                        break
                  x_off, y_off = var
                  new_x_loc = location[0] + x_off
                  new_y_loc = location[1] + y_off
                  #print(x_off, y_off, location)
                  counter += 1
      return output


def move_piece_down(piece_board_notation):
      #TODO
      pass

def display_as_text(notation):
      notation = boardstate_to_extended_boardstate(notation)
      for row in (notation.split("/"))[::-1]: #reverse list
            print(row)

class Board():
      def __init__(self, boardstate="", bag=""):
            self.boardstate = boardstate
            self.extended_boardstate = boardstate_to_extended_boardstate(self.boardstate)
            self.bag = Bag(bag)

class Bag():
      def __init__(self, bag=""):
            self.value = generate_bag(bag)
      def update():
            piece = Bag.value.pop(0)
            Bag.value = generate_bag(Bag.value)
            return piece

#testing commands, these work
#dict1 = board_notation_to_dict('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9')
#print(create_grid(locked_positions=dict1))

#working test function
# a = boardstate_to_extended_boardstate('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9')
#a = boardstate_to_extended_boardstate('')
# print(a)
# print(extended_boardstate_to_boardstate(a))

#working test function
#print(access_cell('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 2, 1))
#print(change_cell('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 1, 5, "S"))

#working test functionsz
#a = update_boardstate_from_piece_board_notation("S054:JJI4ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS")
# a = update_boardstate('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9', 'I253')
# display_as_text('LIOZ4IL/JS5TSZ/SZSZ6/O9/J9')
#display_as_text('JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS')
# display_as_text(a)

#test function
#print(generate_bag("JIZISLZJOTOJZ"))
# a = "I140:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
# display_as_text(update_boardstate_from_piece_board_notation(a))
# for x in range(4):
#       a = rotate_piece(a, "CW")
#       b = update_boardstate_from_piece_board_notation(a)
#       display_as_text(b)

#test function
#print(generate_bag("JIZISLZJOTOJZ"))

#not working test functions
# a = "T140:JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
# display_as_text(update_boardstate_from_piece_board_notation(a))
# a = rotate_piece(a, "CW")
# b = update_boardstate_from_piece_board_notation(a)
# display_as_text(b)