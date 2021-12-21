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

# recently changed, added . and black
colours_dict2 = {  # turtle-compatible colors
    "I": "cyan",
    "J": "blue",
    "L": "orange",
    "O": "yellow",
    "S": "lime",
    "Z": "red",
    "T": "magenta",
    ".": "black",
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
    # Strict input: must have a starting *
    # Empty boardstate
    if boardstate == "*":
        # Asterisk + 40 rows with slashes in between
        # but without the last slash
        return "*" + ("........../"*40)[:-1]
    # Removes starting asterisk
    if boardstate[0] == "*":
        boardstate = boardstate[1:]
    else:
        raise ValueError(
            f"Bad boardstate (no starting asterisk): '{boardstate}'")
    output_list = []
    for i in range(len(boardstate.split("/"))):
        row = boardstate.split("/")[i]
        if row == "":
            output_list2 = [".........."]
            output_list.append("".join(output_list2))
            # Skips to next row as row is empty
            continue
        output_list2 = []
        for index in range(len(row)):
            item = row[index]
            if item.isnumeric() == True:
                num_of_empty_cells = int(row[index])
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
    # Adds empty rows at the end of a board notation
    for _ in range(40-rows):
        notation = notation + "/.........."
    return "*" + notation


def extended_boardstate_to_boardstate(extended_boardstate: str):
    output_list = []
    # Check if board is empty and return empty board
    if extended_boardstate == ("*" + ("........../"*40)[:-1]):
        return "*"
    # Remove starting asterisk
    if extended_boardstate[0] == "*":
        extended_boardstate = extended_boardstate[1:]
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
    # Removes extra lines at the end of a boardstate
    # reverses output list
    for row in output_list[::-1]:
        # As long as the rows (from the end) are empty, remove them
        if row == "":
            output_list.pop(-1)
        else:
            break
    # Strict format: there is an extra * at the beginning
    return "*" + "/".join(output_list)

# TODO: Refactor into smaller functions, make more readable


def board_notation_to_dict(notation):
    global colours_dict2
    notation = boardstate_to_extended_boardstate(notation)
    # Remove starting asterisk
    notation = notation[1:]
    output_list = []
    rows = len(notation.split("/"))
    for row in notation.split("/"):
        if row == "":
            for _ in range(10):
                output_list.append("black")
        for index in range(len(row)):
            item = row[index]
            # Whether it's S or . check color dict and append the respective colour
            output_list.append(colours_dict2[item])
    indices = [(x, y) for x in range(rows) for y in range(10)]
    try:
        items_list = [(indices[i], output_list[i]) for i in range(rows * 10)]
    except:
        print(output_list)
        raise ValueError(
            f"Invalid board notation. Length of output_list: {len(output_list)}")
    return {k: v for (k, v) in items_list}


def type_of_boardstate(boardstate):
    if type(boardstate) == list:
        return "list form"
    if "." in boardstate:
        return "extended boardstate"
    else:
        return "boardstate"


def boardstate_to_list_form(boardstate: str):
    # sourcery skip: inline-immediately-returned-variable
    'Returns a 2D array of cells inside rows from a boardstate'
    type_b = type_of_boardstate(boardstate)
    if type_b == "boardstate":
        # we need to extend the boardstate
        a = boardstate_to_extended_boardstate(str(boardstate))
    elif type_b == "extended boardstate":
        # boardstate is already extended, shorten it and extend it again
        a = boardstate_to_extended_boardstate(
            extended_boardstate_to_boardstate(str(boardstate)))
    # if neither of these an error will be thrown
    # Remove starting asterisk and split a
    a = a[1:].split("/")
    output = [[i for i in item] for item in a]
    return output


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
    # Removes starting asterisk
    return b[1:].split("/")[row][column]


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


def generate_bag(current_bag):
    'Takes a 13-long bag and adds a new piece to the end of it'
    if len(current_bag) == 14:
        return current_bag
    # Make list of all the types of pieces
    # If the current bag is empty, generate a new one
    if current_bag == "":
        return generate_new_bag()
    # Current bag is not empty
    available_pieces = find_available_pieces(current_bag)
    if available_pieces == []:
        # If there are no available pieces, start a new bag with a random piece
        return current_bag + random.choice([p for p in "IJLOSZT"])
    else:
        # If there are available pieces, choose one randomly
        return current_bag + random.choice(available_pieces)


def find_available_pieces(current_bag):
    'Returns the possible options for the next piece, given a bag sequence'
    assert len(current_bag) == 13
    # Finding the last bag in the sequence
    latest_bag = []
    for piece in current_bag:
        # If the piece is repeated, it means there is a new bag
        if piece in latest_bag:
            # This is a new bag now, we don't care about the old one
            latest_bag = [piece]
        else:
            # Add to the latest bag with the piece
            latest_bag.append(piece)
    # Returns the available pieces, which are all the pieces that are not in the latest bag
    return [p for p in "IJLOSZT" if p not in latest_bag]


def generate_new_bag():
    'Generates a 14-long sequence of two bags'
    output_list = []
    for _ in range(2):
        piece_list = [p for p in "IJLOSZT"]
        for _ in range(7):
            # If there is only one piece left, output it and break
            if len(piece_list) == 1:
                output_list.append(piece_list[0])
                break
            a = random.choice(piece_list)
            # Add a random piece to the output list
            output_list.append(a)
            # Remove that piece from the current bag
            piece_list.remove(a)
    return "".join(output_list)


def display_as_text(notation):
    notation = boardstate_to_extended_boardstate(notation)
    for row in (notation.split("/")):  # reverse list
        print(row)

# TODO: Refactor


def check_type_notation(notation):
    'Takes a (valid) notation and returns its type, or False if it\'s unrecognizable.'
    n_list = [i for i in notation]
    # FIXME: len == 4 no longer applies, change this
    if len(n_list) == 4:
        return "piece notation"
    elif ":" in n_list:
        return "piece-board notation"
    elif "*" in n_list:
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

    def __init__(self, t, screen, piece_notation="", boardstate="*", bag="", hold=""):
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
        self.piece_board_notation = self.piece.value + ":" + self.boardstate

    def update_pb_notation(self):
        self.piece_board_notation = construct_piece_board_notation(
            self.piece.value, self.boardstate)

    def display_board(self):
        'Displays the current board through Turtle'
        # Creates a temporary variable to display the current piece/boardstate
        boardstate = update_boardstate(self.boardstate, self.piece)
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
        piece_message = self.piece.type + \
            str(self.piece.orientation) + str(self.piece.x) + str(y_value-1)
        return self.check_if_valid(piece_message)

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
        # Create a new piece moved left one cell
        piece_message = self.piece.type + \
            str(self.piece.orientation) + \
            str(self.piece.x-1) + str(self.piece.y)
        return self.check_if_valid(piece_message)

    def move_piece_right(self):
        # Create a new piece moved right one cell
        piece_message = self.piece.type + \
            str(self.piece.orientation) + \
            str(self.piece.x+1) + str(self.piece.y)
        return self.check_if_valid(piece_message)

    def check_if_valid(self, piece_message):
        b = update_boardstate(self.boardstate, Piece(piece_message))
        if b in ['out of bounds', 'occupied cell']:
            return None
        # Piece message is valid
        self.piece.update(piece_message)
        self.update_pb_notation()
        return True

    def rotate_piece(self, direction):
        #self.piece_board_notation = self.piece.value + ":/" + self.boardstate
        p, b = rotate_and_update2(
            self.piece_board_notation, direction)
        self.piece.update(p)
        self.boardstate = b
        self.update_pb_notation()

    def lock_piece(self):
        b = update_boardstate(self.boardstate, self.piece)
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


def update_boardstate(boardstate, piecestate: Piece):
    'Takes a boardstate and a Piece, and returns the boardstate with the piece in it, or False if it is impossible'
    # Gets a list of offsets from the Piece
    offset_list = find_offset_list(piecestate)
    # Finds the center x and y coordinates
    center_x, center_y = find_center(piecestate)
    # Combining offset and center list to find the list of the actual coordinates
    coord_list = [(x_offset + center_x, y_offset + center_y)
                  for (x_offset, y_offset) in offset_list]
    # Creates a temporary extended boardstate
    nbs = boardstate_to_extended_boardstate(boardstate)
    # Loops over each tile to check whether they are allowed
    for x_loc, y_loc in coord_list:
        # If the x/y coordinates are higher/lower than the size of the board
        if x_loc < 0 or x_loc > 9 or y_loc < 0 or y_loc > 39:
            return "out of bounds"
        # If the cell is empty
        if access_cell(boardstate, y_loc, x_loc) == ".":
            # Updates the cell with the piece type (e.g. T)
            nbs = change_cell(nbs, y_loc, x_loc, piecestate.type)
        else:
            return "occupied cell"
    # Turn back into abbreviated boardstate
    return extended_boardstate_to_boardstate(nbs)


def find_center(piecestate: Piece):
    'Given a Piece, returns the coordinates of its actual center (x, y)'
    if piecestate.type == "O":
        # If piece is an O-piece, just check the spawn orientation (there's only 1)
        shape = pieces["O"][0]
    else:
        shape = pieces[piecestate.type][piecestate.orientation]
    blx, bly = findBLC(shape)
    # The x-offset from the actual x of the piece to the center is 2-blx, same for y
    # Therefore, the center is x+2-blx
    return piecestate.x + 2 - blx, piecestate.y + 2 - bly


def find_offset_list(piecestate: Piece):
    'Given a Piece, returns a list of offsets of each filled tile from the center [(x1, y1), (x2, y2)]'
    # TODO: Might be more efficient (time-wise) to use a lookup table, as there are only 28 possibilities of shapes
    # Accesses global variable pieces
    shape = pieces[piecestate.type][piecestate.orientation]
    offset_list = []
    # Alternative list comprehension (might not be super readable)
    # return [[(cell-2, 2-r) for cell in range(5) if shape[r][cell] == "0"] for r in range(5)]
    for r in range(5):
        for cell in range(5):
            if shape[r][cell] == "0":
                offset_list.append((cell-2, 2-r))
    return offset_list


def update_boardstate_from_pb_notation(pb_notation):
    'Takes a piece-board notation and returns the updated board notation'
    p1, b1 = separate_piece_board_notation(pb_notation)
    return update_boardstate(b1, Piece(p1))


def findBLC(shape):  # finding bottom left corner of a shape
    'Given a shape, finds its bottom left corner relative to a 5x5 grid (helper function to update_boardstate)'
    for r in range(5):
        for c in range(5):
            if shape[4-r][c] == "0":
                return (c, r)


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
        b = update_boardstate(board_notation, Piece(new_piece_message))
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


# silly test function for random gameplay (game might be ok)
a = generate_bag("")
print(a)
try:
    directions = ["CW", "CCW", "180"]
    for _ in range(20):
        b = Board(t, screen, "", "*", a)
        b.display_board()
        sleep(0.5)
        for _ in range(20):
            b.rotate_piece(random.choice(directions))
            b.display_board()
            b.change_x(random.randint(-5, 5))
            b.display_board()
            a = ""
            while a is not None:
                a = b.move_piece_down()
                b.display_board()
                sleep(0.05)
            b.lock_piece()
            print(b.bag.value)
            b.display_board()
except KeyboardInterrupt:
    print(b.piece_board_notation)
