import pygame
import sys
import random
import kicktables
from turtle import Screen, Turtle
import display
from time import sleep

cell_size = 18
cols = 10
rows = 20
maxfps = 30

S = [['.....',
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

Z = [['.....',
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
      '.....'], ]

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
     '.....'], ]

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
     '.....'], ]

T = [
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
     '.....'],
    ['.....',
     '..0..',
     '.000.',
     '.....',
     '.....'], ]

pieces = {"I": I, "J": J, "L": L, "O": O, "S": S, "Z": Z, "T": T}
# for key in [k for k in pieces.keys()]:
#      pieces[key] = pieces[key][::-1]

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
colours_dict2 = {  # turtle-compatible colors
    "I": "cyan",
    "J": "blue",
    "L": "orange",
    "O": "yellow",
    "S": "lime",
    "Z": "red",
    "T": "magenta"
}

shapes = ["I", "J", "L", "O", "S", "Z", "T"]


def create_grid(locked_positions={}):
    # FIXME: Changed height to 40, hopefully doesn't break things
    grid = [["black" for x in range(10)] for x in range(40)]
    for row in range(len(grid)):
        for col in range(len(grid[1])):
            if (row, col) in locked_positions:
                c = locked_positions[(row, col)]
                grid[row][col] = c
    return grid


'LIOZ4IL/JS5TSZ/SZSZ6/O9/J9'  # board notation number 2


def boardstate_to_extended_boardstate(boardstate: str):
    if boardstate == "":
        # FIXME: Changed rows to 40, might cause breaking change
        return "/.........."*40
    output_list = []
    for i in range(len(boardstate.split("/"))):
        row = boardstate.split("/")[i]
        if row == "":
            if i == 0:
                continue
            else:
                output_list2 = [".........."]
                output_list.append("".join(output_list2))
                continue
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
            print(boardstate, output_list2)
            raise ValueError(output_list2)
        output_list.append("".join(output_list2))
    notation = "/".join(output_list)
    rows = len(notation.split("/"))
    # FIXME: Changed to 40 max rows
    for i in range(40-rows):
        notation = notation + "/.........."
    return notation


def extended_boardstate_to_boardstate(extended_boardstate: str):
    output_list = []
    for row in extended_boardstate.split("/"):
        if row == "..........":
            output_list.append("")
            continue
        output_list2 = []
        counter = 0
        for item in row:
            if item == ".":
                counter += 1
            else:
                if counter != 0:
                    output_list2.append(str(counter))
                    counter = 0
                output_list2.append(item)
        if counter != 0:
            output_list2.append(str(counter))
        output_list.append("".join(output_list2))
    return "/".join(output_list)

# this should work, might need more testing


def board_notation_to_dict(notation):
    global colours_dict2
    #notation = boardstate_to_extended_boardstate(notation)
    output_list = []
    rows = len(notation.split("/"))
    for row in notation.split("/"):
        if row == "":
            for x in range(10):
                output_list.append("black")
        for index in range(len(row)):
            item = row[index]
            if item.isnumeric() == False:
                output_list.append(colours_dict2[item])
            else:
                num_of_empty_cells = int(row[index])
                for i in range(num_of_empty_cells):
                    output_list.append("black")
    indices = [(x, y) for x in range(rows) for y in range(10)]
    try:
        items_list = [(indices[i], output_list[i]) for i in range(rows * 10)]
    except:
        print(output_list)
        raise ValueError(
            f"Invalid board notation. Length of output_list: {len(output_list)}")
    return {k: v for (k, v) in items_list}


def boardstate_to_list_form(boardstate: str):
    return [[i for i in item] for item in boardstate_to_extended_boardstate(str(boardstate)).split("/")]


def list_form_to_boardstate(list_form: list):
    return "/".join(["".join(item) for item in (list_form)])


def access_cell(boardstate: str, row: int, column: int):
    'Given a boardstate, row, and column of a cell (starting from index 0), return the value of the cell in the boardstate.'
    b = boardstate_to_extended_boardstate(boardstate)
    return b.split("/")[row][column]


def change_cell(boardstate: str, row: int, column: int, val: str):
    'Given a boardstate, row, column of a cell (starting from index 0), and a value, update the boardstate and return it.'
    row = int(row)
    column = int(column)
    new_boardstate = boardstate_to_list_form(boardstate)
    new_boardstate[row][column] = val
    return list_form_to_boardstate(new_boardstate)


# Example piece notation
'S038'  # S piece in spawn orientation (0) in column 3, row 8


def return_x_y(piece_notation):
    if piece_notation[2] == "-":  # handling negative x/y values and 2 digit x values
        x_loc = int(str(piece_notation[2]) + str(piece_notation[3]))
        y_loc = int(piece_notation[4:])
    else:
        x_loc = piece_notation[2]
        y_loc = int(piece_notation[3:])
    return str(x_loc), str(y_loc)


def generate_bag(current_bag):
    'Takes a 13-long bag and adds a new piece to the end of it'
    if len(current_bag) == 14:
        return current_bag
    # Make list of all the types of pieces
    pieces = [p for p in "IJLOSZT"]
    output_list = []
    if current_bag == "":
        for x in range(2):
            pieces = [p for p in "IJLOSZT"]
            for x in range(7):
                # FIXME: Hacky solution, check for bugs later
                if len(pieces) == 1:
                    output_list.append(pieces[0])
                    continue
                a = random.randint(0, len(pieces) - 1)
                output_list.append(pieces[a])
                pieces.pop(a)
                #output_list.append(pieces.pop(random.randint(0, len(pieces) - 1)))
        return "".join(output_list)
    # Current bag is not empty
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
    # FIXME: Hacky solution, check for bugs
    if pieces == []:
        return random.choice([p for p in "IJLOSZT"])
    else:
        return current_bag + random.choice(pieces)


def check_kick_tables(piece, initial_direction, final_direction, test_number):
    'Takes a piece and the test number, returns the respective offset, or False if there are no more tests'
    direction = str(initial_direction) + str(final_direction)
    if piece == "O":
        return False
    elif piece == "I":
        table = kicktables.i_table
    elif piece in [p for p in "JLSZT"]:
        table = kicktables.jlszt_table
    if abs(final_direction - initial_direction) == 2:
        table = kicktables.flip_table  # if 180 rotation
    kicktable = table[direction]  # accessing kick table
    if test_number >= len(kicktable):  # no more kicks
        return False
    a = kicktable[test_number][1:-1].split(", ")  # converting from
    x_offset = int(a[0])
    y_offset = int(a[1])
    # if x_offset < 0 or x_offset > 9 or y_offset < 0:
    #       return False
    return y_offset, x_offset


def check_kick_tables_repeatedly(final_piece_board_notation, initial_direction, final_direction, debug=True):
    'Takes a piece and the rotation, checks all tests and returns the final offset, or False if there are no more tests'
    full_piece = final_piece_board_notation.split(":")[0]
    # if "-" in full_piece: #i don't see why this is here
    #      return False
    piece = full_piece[0]  # type of piece
    final_direction = int(full_piece[1])  # final orientation
    direction = str(initial_direction) + \
        str(final_direction)  # key in kicktable
    board = final_piece_board_notation.split(":")[1]
    if piece == "O":
        return final_piece_board_notation
    elif piece == "I":
        table = kicktables.i_table
    elif piece in [p for p in "JLSZT"]:
        table = kicktables.jlszt_table
    if abs(final_direction - initial_direction) == 2:
        table = kicktables.flip_table  # if 180 rotation
        if debug == True:
            print("180 tables accessed.")
    kicktable = table[direction]  # accessing kick table
    if debug == True:
        print(f"Testing piece '{full_piece}', in direction {direction}.")
    for test_number in range(5):
        if test_number >= len(kicktable):  # no more kicks
            return final_piece_board_notation  # return original
        a = kicktable[test_number][1:-1].split(", ")  # converting from
        x_offset = int(a[0])
        y_offset = int(a[1])
        x_loc, y_loc = return_x_y(full_piece)
        if debug == True:
            print(f"x-offset: {x_offset}, y-offset: {y_offset}")
        if debug == True:
            print(
                f"Test {test_number}: ({int(x_loc) + x_offset}, {int(y_loc) + y_offset})")
        if (int(x_loc) + x_offset) < 0 or (int(x_loc) + x_offset) > 9 or (int(y_loc) + y_offset < 0):
            if debug == True:
                print(
                    f"Coords failed initial check: {int(x_loc) + x_offset,int(y_loc) + y_offset}")
            continue
        try:
            y_loc = str(int(y_loc) + int(y_offset))
            x_loc = str(int(x_loc) + int(x_offset))
            piece_message = piece + str(final_direction) + x_loc + y_loc
            if debug == True:
                print(f"Testing {piece_message}, {board}.")
            update_boardstate2(board, piece_message)
            return piece_message + ":" + board
        except:  # if an error is thrown (piece doesn't fit)
            if debug == True:
                print(f"Piece does not fit.")
            continue  # keep trying
    if debug == True:
        print("All checks have been tried. Returning original boardstate.")
    return final_piece_board_notation  # if no breaks have occured


def rotate_piece(piece_board_notation, direction, debug=False, without_kick_testing=False):
    'Takes a piece-board notation and direction (CW, CCW, or 180), returns updated piece-board notation'
    global pieces
    piece_notation = piece_board_notation.split(":")[0]
    piece = piece_notation[0]
    orientation = int(piece_notation[1])
    column = int(piece_notation[2])
    row = int(piece_notation[3])
    boardstate = piece_board_notation.split(":")[1]
    boardstate = extended_boardstate_to_boardstate(
        boardstate_to_extended_boardstate(boardstate))
    shape = pieces[piece][orientation]
    if direction == "CW":
        new_orientation = (orientation+1) % 4
    elif direction == "CCW":
        new_orientation = (orientation+3) % 4  # +3 = -1
    elif direction == "180":
        new_orientation = (orientation+2) % 4
    else:
        raise ValueError(f"Incorrect direction of rotation: '{direction}'")
    new_shape = pieces[piece][new_orientation]
    y_diff, x_diff = find_difference(shape, new_shape)
    location = [column+x_diff, row+y_diff]
    new_x_loc, new_y_loc = location[0], location[1]
    if debug == True:
        print(
            f"Original loc: ({column}, {row}). New loc: ({new_x_loc}, {new_y_loc}). Diff: ({x_diff}, {y_diff})")
    if without_kick_testing == True:
        return piece + str(new_orientation) + str(new_x_loc) + str(new_y_loc) + ":" + boardstate
    output = piece + str(new_orientation) + str(new_x_loc) + \
        str(new_y_loc) + ":" + boardstate
    final_output = check_kick_tables_repeatedly(
        output, orientation, new_orientation, debug)
    print(f"Output from check_kick_tables_repeatedly: {final_output}")
    if final_output == False:
        return output
    else:
        return final_output


def move_piece_down(piece_board_notation):
    piece = piece_board_notation.split(":")[0]
    x, y = return_x_y(piece)
    y = str(int(y)-1)
    return piece[0] + piece[1] + x + y + ":" + piece_board_notation.split(":")[0]


def display_as_text(notation):
    notation = boardstate_to_extended_boardstate(notation)
    for row in (notation.split("/"))[::-1]:  # reverse list
        print(row)


def check_type_notation(notation):
    'Takes a (valid) notation and returns its type, or False if it\'s unrecognizable.'
    n_list = [i for i in notation]
    if len(n_list) == 4:
        return "piece notation"
    elif ":" in n_list:
        return "piece-board notation"
    elif "/" in n_list:
        if "." in n_list:
            return "extended board notation"
        else:
            for item in n_list:
                if item.isnumeric() == True:
                    return "board notation"
            return False
    else:
        if len(n_list) == 14 or len(n_list) == 13:
            return "bag notation"
        else:
            return False


class Piece():
    def __init__(self, piece_notation: str = ""):
        self.value = piece_notation
        self.x, self.y = return_x_y(piece_notation)
        self.x, self.y = int(self.x), int(self.y)
        self.type = piece_notation[0]
        self.orientation = int(piece_notation[1])

    def update(self, new_piece: str):
        self.value = new_piece
        self.x, self.y = return_x_y(new_piece)
        self.x, self.y = int(self.x), int(self.y)
        self.type = new_piece[0]
        self.orientation = int(new_piece[1])


class Bag():
    def __init__(self, bag=""):
        self.value = generate_bag(bag)

    def update(self):
        piece = self.value[0]
        self.value = generate_bag(self.value[1:])
        return piece


class Board():
    def __init__(self, piece_notation="", boardstate="", bag="", hold=""):
        self.boardstate = boardstate
        self.extended_boardstate = boardstate_to_extended_boardstate(
            self.boardstate)
        self.bag = Bag(bag)
        self.hold = hold
        # Weird how you can call functions written after __init__
        if piece_notation == "":
            self.piece = Piece(self.spawn_next_piece(init=True))
        else:
            self.piece = Piece(piece_notation)
        # Non-dynamic init piece board notation
        self.piece_board_notation = self.piece.value + ":/" + self.boardstate

    def display_board(self, t, screen):
        # Creates a temporary variable to display the current piece/boardstate
        boardstate = update_boardstate2(self.boardstate, self.piece)
        if boardstate == "out of bounds" or boardstate == "occupied cell":
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        else:
            self.boardstate = boardstate
            draw_grid(boardstate, t, screen)

    def spawn_next_piece(self, init=""):
        new_piece_type = self.bag.update()
        orientation = "0"  # spawn orientation
        # Adjusting spawn coordinates based on piece
        if new_piece_type == "L":
            x, y = 3, 22
        if new_piece_type == "J":
            x, y = 3, 22
        if new_piece_type == "S":
            x, y = 3, 22
        if new_piece_type == "Z":
            x, y = 4, 22
        if new_piece_type == "O":
            x, y = 4, 22
        if new_piece_type == "T":
            x, y = 3, 22
        if new_piece_type == "I":
            x, y = 3, 22
        if init != "":
            return new_piece_type + orientation + str(x) + str(y)
        else:
            self.piece.update(new_piece_type + orientation + str(x) + str(y))

    def move_piece_down(self):
        y_value = self.piece.y
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation) + str(self.piece.x)
        self.piece.update(rest_of_piece_value + str(y_value-1))

    def move_piece_left(self):
        x_value = self.piece.x
        b = update_boardstate2(self.boardstate, self.piece)
        # Checking if piece is all the way to the left or will hit something
        if b == "out of bounds" or b == "occupied cell":
            # Exit function
            return None
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation)
        self.piece.update(rest_of_piece_value +
                          str(x_value-1) + str(self.piece.y))

    def move_piece_right(self):
        x_value = self.piece.x
        b = update_boardstate2(self.boardstate, self.piece)
        # Checking if piece is all the way to the left or will hit something
        if b == "out of bounds" or b == "occupied cell":
            # Exit function
            return None
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation)
        self.piece.update(rest_of_piece_value +
                          str(x_value+1) + str(self.piece.y))

    def rotate_piece(self, direction):
        #FIXME: Piece-board notation shenanigans
        #self.piece_board_notation = self.piece.value + ":/" + self.boardstate
        p, b = rotate_and_update2(
            self.piece_board_notation, direction)
        self.piece.update(p)
        self.boardstate = b

    def lock_piece(self):
        b = update_boardstate2(self.boardstate, self.piece)
        if b == "out of bounds" or b == "occupied cell":
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        else:
            self.boardstate = b
            self.spawn_next_piece()


class Game():
    def __init__(self):
        # TODO: Write some stuff
        pass


def update_boardstate2(boardstate, piecestate: Piece):
    'Takes a boardstate and a Piece, and returns the boardstate with the piece in it, or False if it is impossible'
    global pieces
    x, y = piecestate.x, piecestate.y
    # Reversed because list is reversed for some reason
    shape = pieces[piecestate.type][::-1][piecestate.orientation]
    blx, bly = findBLC(shape)
    assert blx != None and bly != None
    xdif = 2-blx
    ydif = 2-bly
    center = (x+xdif, y+ydif)
    oList = []
    for r in range(5):
        for cell in range(5):
            if shape[r][cell] == "0":
                oList.append((cell-2, 2-r))
    nbs = boardstate_to_extended_boardstate(boardstate)
    for change_in_x, change_in_y in oList:
        cx, cy = center
        x_loc = cx+change_in_x
        y_loc = cy+change_in_y
        # FIXME: Changed y_loc upper bound to 39, might cause breaking change
        if x_loc < 0 or x_loc > 9 or y_loc < 0 or y_loc > 39:
            return "out of bounds"
        if access_cell(boardstate, y_loc, x_loc) == ".":
            nbs = change_cell(nbs, y_loc, x_loc, piecestate.type)
        else:
            return "occupied cell"
    return extended_boardstate_to_boardstate(nbs)


def findBLC(shape):  # finding bottom left corner of a shape
    'Given a shape, finds its bottom left corner (helper function to update_boardstate)'
    for r in range(5):
        for c in range(5):
            if shape[4-r][c] == "0":
                return (c, r)
    return (None, None)


def find_difference(shape, new_shape):
    'Helper function for rotate_piece'
    bl_row, bl_col = findBLC(shape)
    assert bl_row != None and bl_col != None
    bl_row2, bl_col2 = findBLC(new_shape)
    assert bl_row2 != None and bl_col2 != None
    y_diff, x_diff = bl_row2 - bl_row, bl_col2 - bl_col
    return y_diff, x_diff


def find_difference2(piece, new_piece):
    'Takes the type of piece and orientation (T0) of two pieces and returns their difference'
    global pieces
    shape = pieces[piece[0]][::-1][int(piece[1])]
    new_shape = pieces[new_piece[0]][::-1][int(new_piece[1])]
    x, y = findBLC(shape)
    x2, y2 = findBLC(new_shape)
    x_diff, y_diff = x2 - x, y2 - y
    return x_diff, y_diff


def check_kick_tables2(old_piece_notation, new_piece_notation, board_notation):
    '''Takes a piece notation, board notation, direction and returns the piece notation 
    after checking kicktables, or False if rotation is impossible'''
    direction = old_piece_notation[1] + new_piece_notation[1]
    t = new_piece_notation[0]
    x, y = return_x_y(new_piece_notation)
    r_diff = int(old_piece_notation[1]) - int(new_piece_notation[1])
    if t == "O":
        return False
    if r_diff == 2 or r_diff == -2:
        table = kicktables.fliptable
    elif t == "I":
        table = kicktables.i_table
    else:
        assert t in "JLSZT"
        table = kicktables.jlszt_table
    for i in range(5):
        # getting offsets from table (formatting)
        tup = table[direction][i][1:-1].split(", ")
        x_offset = int(tup[0])
        y_offset = int(tup[1])
        new_piece_message = t + \
            new_piece_notation[1] + str(int(x)+x_offset) + str(int(y)+y_offset)
        b = update_boardstate2(board_notation, Piece(new_piece_message))
        if b == "out of bounds" or b == "occupied cell":
            # Doesn't work, try next kick
            continue
        else:
            return new_piece_message
    # Checked all kicks, none work
    return False


def rotate_and_update2(pb_notation, direction):
    # TODO: Write stuff
    piece_n = pb_notation.split(":")[0]
    b = pb_notation.split(":")[1]
    d = piece_n[1]
    x, y = return_x_y(piece_n)
    if direction == "CW":
        rotation_factor = 1
    elif direction == "CCW":
        rotation_factor = 3
    elif direction == "180":
        rotation_factor = 2
    else:
        raise ValueError(f"Bad direction: '{direction}")
    new_direction = str((int(d) + rotation_factor) % 4)
    po1 = piece_n[:2]
    po2 = piece_n[0] + new_direction
    x_diff, y_diff = find_difference2(po1, po2)
    nx, ny = str(int(x)+x_diff), str(int(y)+y_diff)
    piece_message = piece_n[0]+new_direction+nx+ny
    final_piece_notation = check_kick_tables2(piece_n, piece_message, b)
    if final_piece_notation == False:
        final_piece_notation = piece_n
    return final_piece_notation, b


def init_screen():
    screen = Screen()
    screen.bgcolor("black")
    screen.setup(width=300, height=600)
    screen.title("Tetris")
    t = Turtle()
    screen.tracer(0)
    return t, screen


def draw_grid(board_notation, t, screen):
    display.draw_grid(create_grid(
        board_notation_to_dict(board_notation)), t, screen)


def smart_display(notation, t, screen):
    type_of_notation = check_type_notation(notation)
    if type_of_notation == "board notation":
        notation = notation
    elif type_of_notation == "piece-board notation":
        notation = update_boardstate2(
            notation.split(":")[0], notation.split(":")[1])
    elif type_of_notation == "extended board notation":
        notation = extended_boardstate_to_boardstate(notation)
    else:
        raise ValueError(
            f"Incorrect notation: '{notation}''. This was interpreted as a '{type_of_notation}'")
    draw_grid(notation, t, screen)


def slideshow(slides, t, screen: Screen):
    current_slide = 0
    smart_display(slides[0], t, screen)

    def go_back():
        nonlocal current_slide, t, screen
        if current_slide - 1 >= 0:
            smart_display(slides[current_slide - 1], t, screen)
            current_slide += -1
        else:
            smart_display(slides[current_slide], t, screen)

    def go_forward():
        nonlocal current_slide, t, screen
        if current_slide + 1 < len(slides):
            smart_display(slides[current_slide + 1], t, screen)
            current_slide += 1
        else:
            smart_display(slides[current_slide], t, screen)
    screen.onkey(go_forward, "Right")
    screen.onkey(go_back, "Left")
    screen.listen()


t, screen = init_screen()
s = "JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS"
b = Board("S1410", s)
for x in range(20):
    b.display_board(t, screen)
    sleep(1)
    b.rotate_piece("CCW")
    b.display_board(t, screen)
    sleep(1)
    b.rotate_piece("CW")
