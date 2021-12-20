import random
import kicktables
from turtle import Screen, Turtle
import display
from time import sleep

# switched 2nd and 4th orientation of L, T, J recently
I = [['.....', '0000.', '.....', '.....', '.....'], ['.0...', '.0...', '.0...', '.0...', '.....'], [
    '.....', '.....', '0000.', '.....', '.....'], ['..0..', '..0..', '..0..', '..0..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], [
    '.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], [
    '.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
S = [['.....', '..00..', '.00...', '......', '.....'], ['.....', '.0...', '.00..', '..0..', '.....'], [
    '.....', '......', '..00..', '.00...', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.00..', '..00.', '.....', '.....'], ['.....', '...0.', '..00.', '..0..', '.....'], [
    '.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0...', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], [
    '.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

pieces = {"I": I, "J": J, "L": L, "O": O, "S": S, "Z": Z, "T": T}

colours_dict2 = {  # turtle-compatible colors
    "I": "cyan",
    "J": "blue",
    "L": "orange",
    "O": "yellow",
    "S": "lime",
    "Z": "red",
    "T": "magenta"
}


def create_grid(locked_positions={}):
    grid = [["black" for x in range(10)] for x in range(40)]
    for row in range(len(grid)):
        for col in range(len(grid[1])):
            if (row, col) in locked_positions:
                c = locked_positions[(row, col)]
                grid[row][col] = c
    return grid

# TODO: Refactor into smaller methods


def boardstate_to_extended_boardstate(boardstate: str):
    if boardstate == "":
        return "/.........."*40
    output_list = []
    for i in range(len(boardstate.split("/"))):
        row = boardstate.split("/")[i]
        if row == "":
            if i != 0:
                output_list2 = [".........."]
                output_list.append("".join(output_list2))
            # Skips to next row as row is empty
            continue
        output_list2 = []
        for index in range(len(row)):
            item = row[index]
            if item.isnumeric() == True:
                num_of_empty_cells = int(row[index])
                # Unused variable
                for _ in range(num_of_empty_cells):
                    output_list2.append(".")
            else:
                output_list2.append(item)
        if len(output_list2) != 10:
            print(boardstate, output_list2)
            raise ValueError(output_list2)
        output_list.append("".join(output_list2))
    notation = "/".join(output_list)
    rows = len(notation.split("/"))
    for _ in range(40-rows):
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
    # Strict format: there is an extra / at the beginning
    return "/" + "/".join(output_list)

# TODO: Refactor into smaller functions, make more readable


def board_notation_to_dict(notation):
    global colours_dict2
    #notation = boardstate_to_extended_boardstate(notation)
    output_list = []
    rows = len(notation.split("/"))
    for row in notation.split("/"):
        if row == "":
            for _ in range(10):
                output_list.append("black")
        for index in range(len(row)):
            item = row[index]
            if item.isnumeric() == False:
                output_list.append(colours_dict2[item])
            else:
                num_of_empty_cells = int(row[index])
                for _ in range(num_of_empty_cells):
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


def construct_piece_board_notation(piece_notation, board_notation):
    'Returns str of piece board notation'
    return f"{piece_notation}:{board_notation}"


def separate_piece_board_notation(pb_notation):
    'Returns a tuple (piece_notation, board_notation)'
    return (pb_notation.split(":")[0], pb_notation.split(":")[1])


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


def return_x_y(piece_notation):
    if piece_notation[2] == "-":  # handling negative x/y values and 2 digit x values
        x_loc = int(str(piece_notation[2]) + str(piece_notation[3]))
        y_loc = int(piece_notation[4:])
    else:
        x_loc = piece_notation[2]
        y_loc = int(piece_notation[3:])
    return str(x_loc), str(y_loc)

# TODO: Refactor this


def generate_bag(current_bag):
    'Takes a 13-long bag and adds a new piece to the end of it'
    if len(current_bag) == 14:
        return current_bag
    # Make list of all the types of pieces
    pieces = [p for p in "IJLOSZT"]
    if current_bag == "":
        output_list = []
        for _ in range(2):
            pieces = [p for p in "IJLOSZT"]
            for _ in range(7):
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


def display_as_text(notation):
    notation = boardstate_to_extended_boardstate(notation)
    for row in (notation.split("/")):  # reverse list
        print(row)

# TODO: Refactor


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
        for item in n_list:
            if item.isnumeric() == True:
                return "board notation"
        return False
    else:
        if len(n_list) in [14, 13]:
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
    'A Tetris board, with a turtle, screen, and data'

    def __init__(self, t, screen, piece_notation="", boardstate="", bag="", hold=""):
        self.t = t
        self.screen = screen
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

    def update_pb_notation(self):
        self.piece_board_notation = construct_piece_board_notation(
            self.piece.value, self.boardstate)

    def display_board(self):
        'Displays the current board through Turtle'
        # Creates a temporary variable to display the current piece/boardstate
        boardstate = update_boardstate2(self.boardstate, self.piece)
        if boardstate in ["out of bounds", "occupied cell"]:
            # TODO: Do validation if the piece locks at the 21st row or up
            # Meaning the game is over
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        draw_grid(boardstate, self.t, self.screen)

    def spawn_next_piece(self, init=""):
        new_piece_type = self.bag.update()
        orientation = "0"  # spawn orientation
        # Adjusting spawn coordinates based on piece
        if new_piece_type in ["L", "J", "S", "T", "I"]:
            x, y = 3, 22
        elif new_piece_type in ["Z", "O"]:
            x, y = 4, 22
        if init != "":
            return new_piece_type + orientation + str(x) + str(y)
        else:
            self.piece.update(new_piece_type + orientation + str(x) + str(y))
        self.update_pb_notation()

    def move_piece_down(self):
        y_value = self.piece.y
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation) + str(self.piece.x)
        piece_message = rest_of_piece_value + str(y_value-1)
        b = update_boardstate2(self.boardstate, Piece(
            piece_message))
        if b in ["out of bounds", "occupied cell"]:
            # Exit function
            return None
        self.piece.update(piece_message)
        self.update_pb_notation()
        # returns True if the function is successful
        return True

    def change_x(self, value: int):
        '''Moves the piece left or right by a certain amount of cells
        Will stop if the piece cannot move
        Does not validate the input of cells needed to move'''
        if value > 0:
            func = self.move_piece_right
        elif value < 0:
            func = self.move_piece_left
        else:
            # Value is 0 or not an integer, exit the function
            return None
        # Loop absolute value of the number of cell times
        for _ in range(abs(value)):
            # Call the move_piece_left/right func
            # Piece, board, and piece-board notation are updated in here
            flag = func()
            self.display_board()
            # Flag is True if it is successful, None if unsuccessful
            if flag is None:
                # Piece cannot be moved left/right anymore, stop the function
                break
        return True

    def move_piece_left(self):
        x_value = self.piece.x
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation)
        b = update_boardstate2(self.boardstate, Piece(rest_of_piece_value +
                                                      str(x_value-1) + str(self.piece.y)))
        # Checking if piece is all the way to the left or will hit something
        if b in ["out of bounds", "occupied cell"]:
            # Exit function
            return None
        # If it works, update piece
        self.piece.update(rest_of_piece_value +
                          str(x_value-1) + str(self.piece.y))
        self.update_pb_notation()
        # Return True if successful
        return True

    def move_piece_right(self):
        x_value = self.piece.x
        b = update_boardstate2(self.boardstate, self.piece)
        # Checking if piece is all the way to the left or will hit something
        if b in ["out of bounds", "occupied cell"]:
            # Exit function
            return None
        rest_of_piece_value = self.piece.type + \
            str(self.piece.orientation)
        self.piece.update(rest_of_piece_value +
                          str(x_value+1) + str(self.piece.y))
        self.update_pb_notation()
        # Return True if successful
        return True

    def rotate_piece(self, direction):
        #self.piece_board_notation = self.piece.value + ":/" + self.boardstate
        p, b = rotate_and_update2(
            self.piece_board_notation, direction)
        self.piece.update(p)
        self.boardstate = b
        self.update_pb_notation()

    def lock_piece(self):
        b = update_boardstate2(self.boardstate, self.piece)
        if b in ["out of bounds", "occupied cell"]:
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        self.boardstate = b
        self.spawn_next_piece()
        self.update_pb_notation()


class Game():
    def __init__(self):
        # TODO: Write some stuff
        pass


# TODO: Refactor into smaller functions
def update_boardstate2(boardstate, piecestate: Piece):
    'Takes a boardstate and a Piece, and returns the boardstate with the piece in it, or False if it is impossible'
    global pieces
    x, y = piecestate.x, piecestate.y
    shape = pieces[piecestate.type][piecestate.orientation]
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
        if x_loc < 0 or x_loc > 9 or y_loc < 0 or y_loc > 39:
            return "out of bounds"
        if access_cell(boardstate, y_loc, x_loc) == ".":
            nbs = change_cell(nbs, y_loc, x_loc, piecestate.type)
        else:
            return "occupied cell"
    return extended_boardstate_to_boardstate(nbs)


def update_boardstate_from_pb_notation(pb_notation):
    'Takes a piece-board notation and returns the updated board notation'
    p1, b1 = separate_piece_board_notation(pb_notation)
    return update_boardstate2(b1, Piece(p1))


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
    'Takes the type of piece and orientation (e.g. T0) of two pieces and returns their difference'
    global pieces
    # FIXME: Hacky fix, might not work
    if piece[0] == "O":
        # If piece is an O-piece, make the orientation 0 because all orientations are the same
        # (for the purpose of this function)
        piece = piece[0] + "0" + piece[2:]
    # same goes for new_piece (optimize this later)
    if new_piece[0] == "O":
        new_piece = new_piece[0] + "0" + new_piece[2:]
    shape = pieces[piece[0]][int(piece[1])]
    new_shape = pieces[new_piece[0]][int(new_piece[1])]
    x, y = findBLC(shape)
    x2, y2 = findBLC(new_shape)
    return x2 - x, y2 - y

# TODO: Refactor into smaller chunks


def check_kick_tables2(old_piece_notation, new_piece_notation, board_notation):
    '''Takes a piece notation, board notation, direction and returns the piece notation 
    after checking kicktables, or False if rotation is impossible'''
    direction = old_piece_notation[1] + new_piece_notation[1]
    t = new_piece_notation[0]
    x, y = return_x_y(new_piece_notation)
    r_diff = int(old_piece_notation[1]) - int(new_piece_notation[1])
    if t == "O":
        return False
    if r_diff in [2, -2]:
        # this said fliptable for some time
        table = kicktables.flip_table
    elif t == "I":
        table = kicktables.i_table
    else:
        assert t in "JLSZT"
        table = kicktables.jlszt_table
    # TODO: Make the first repetition check the original new_piece_notation
    # as there is unnecessary assignment here
    for i in range(5):
        # getting offsets from table (formatting)
        tup = table[direction][i][1:-1].split(", ")
        x_offset = int(tup[0])
        y_offset = int(tup[1])
        new_piece_message = t + \
            new_piece_notation[1] + str(int(x)+x_offset) + str(int(y)+y_offset)
        b = update_boardstate2(board_notation, Piece(new_piece_message))
        if b not in ["out of bounds", "occupied cell"]:
            return new_piece_message
    # Checked all kicks, none work
    return False

# TODO: Refactor, make more readable


def rotate_and_update2(pb_notation, direction):
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

# TODO: Deprecated, update to match with Board class structure


def smart_display(notation, t, screen):
    'Displays a board, piece-board, or extended board notation in the form of a Board'
    piece_notation = ""
    boardstate = ""
    type_of_notation = check_type_notation(notation)
    if type_of_notation == "board notation":
        boardstate = notation
    elif type_of_notation == "piece-board notation":
        p, b = separate_piece_board_notation(notation)
        piece_notation = p
        boardstate = b
    elif type_of_notation == "extended board notation":
        boardstate = extended_boardstate_to_boardstate(notation)
    else:
        raise ValueError(
            f"Incorrect notation: '{notation}''. This was interpreted as a '{type_of_notation}'")
    b = Board(t, screen, piece_notation, boardstate)
    b.display_board()


def slideshow(slides, t, screen: Screen):
    current_slide = 0
    smart_display(slides[0], t, screen)

    def go_back():
        nonlocal current_slide, t, screen
        if current_slide >= 1:
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
    screen.mainloop()


t, screen = init_screen()

# Slideshow is working (although it spawns a random piece)
# slides = ["JJJI3ZZT/OOJI2ZZTT/OOLI3SST/LLLI4SS",
#           "///TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/TZLOSJI3/"]
# slideshow(slides, t, screen)

# FIXME: move_piece_down pushes piece below it
try:
    for _ in range(20):
        b = Board(t, screen)
        b.display_board()
        sleep(0.5)
        for _ in range(20):
            for _ in range(15):
                b.move_piece_down()
                b.display_board()
                sleep(0.05)
            b.lock_piece()
            b.display_board()
except KeyboardInterrupt:
    print(construct_piece_board_notation(b.piece.value, b.boardstate))

# silly test function for random gameplay (game might be ok)
# directions = ["CW", "CCW", "180"]
# for _ in range(20):
#     b = Board(t, screen)
#     b.display_board()
#     sleep(0.5)
#     for _ in range(20):
#         b.rotate_piece(random.choice(directions))
#         b.display_board()
#         b.change_x(random.randint(-5, 5))
#         b.display_board()
#         for _ in range(21):
#             if b.move_piece_down() is None:
#                 continue
#             b.display_board()
#             sleep(0.05)
#         b.lock_piece()
#         b.display_board()

# FIXME: pieces moved to the right cause impossible piece locks error
# not caught by the move_piece_left/right function
# e.g. "ValueError: Impossible piece lock, piece: 'J1921', board: 'IIII3T2/1Z1J2TTT1/ZZZJ3J2/ZZZJJ2J2/JZT1T2JJ1/J1TTTT1ZZ1/JJT1T1ZZ2/LIIII5/LLL1T5/4TT4/4T5/4IIII2/5LL3/5L4/5L4/5S4/4SS4/4S5//////////////////////'"
