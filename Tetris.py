from cmath import pi
import storage
import display
from random import choice, seed, shuffle
from typing import List, Tuple, Any, Generator
from turtle import Screen, Turtle, update
from time import sleep, time


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}
    grid = [["black" for _ in range(10)] for _ in range(40)]
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
        return f'*{("........../"*40)[:-1]}'
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
        # Checking if row is a garbage row (e.g. "g6")
        if row[0] == "g":
            garbage_index = int(row[1])
            type_of_piece = row[2] if len(row) == 3 else "."
            assert garbage_index >= 0 and garbage_index <= 9
            # g6 becomes xxxxxx.xxx as the . is in index 6
            message = "x" * garbage_index + \
                type_of_piece + "x" * (9 - garbage_index)
            # Appends the message to the outputlist
            output_list.append(message)
            continue
        output_list2 = []
        for index in range(len(row)):
            item = row[index]
            if item.isnumeric() == True:
                num_of_empty_cells = int(row[index])
                output_list2.extend("." for _ in range(num_of_empty_cells))
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
        notation = f'{notation}/..........'
    return f'*{notation}'


def extended_boardstate_to_boardstate(extended_boardstate: str):
    output_list = []
    # Check if board is empty and return empty board
    if extended_boardstate == f'*{("........../"*40)[:-1]}':
        return "*"
    # Remove starting asterisk
    if extended_boardstate[0] == "*":
        extended_boardstate = extended_boardstate[1:]
    for row in extended_boardstate.split("/"):
        if row == "..........":
            # If row is empty, add an empty row to the output list
            output_list.append("")
            continue
        # Checking if it is a garbage row:
        if "x" in row:
            # Converts row to a list, finds the index of the non-garbage cell,
            # and appends "g" and the index to the outputlist (e.g g2 for xx.xxxxxxx)
            index = 0
            # Default piece type is ., which isn't shown
            piece_type = ""
            for i, cell in enumerate(row):
                if cell != "x":
                    # Finds the non garbage cell
                    index = i
                    if cell != ".":
                        # Sets the piece type to the contents of the cell
                        piece_type = cell
                    break
            else:
                # All cells are x, which shouldn't happen
                raise ValueError(
                    f"Filled garbage row in boardstate: {extended_boardstate}")
            message = "g" + str(index) + piece_type
            output_list.append(message)
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
    notation = boardstate_to_extended_boardstate(notation)
    # Remove starting asterisk
    notation = notation[1:]
    output_list = []
    rows = len(notation.split("/"))
    for row in notation.split("/"):
        if row == "":
            output_list.extend("black" for _ in range(10))
        for index in range(len(row)):
            item = row[index]
            # Whether it's S or . check color dict and append the respective colour
            output_list.append(storage.colours_dict[item])
    indices = [(x, y) for x in range(rows) for y in range(10)]
    try:
        items_list = [(indices[i], output_list[i]) for i in range(rows * 10)]
    # TODO: Add a more specific except here
    except:
        print(output_list)
        raise ValueError(
            f"Invalid board notation. Length of output_list: {len(output_list)}")
    return dict(items_list)


def type_of_boardstate(boardstate):
    if type(boardstate) == list:
        return "list form"
    return "extended boardstate" if "." in boardstate else "boardstate"


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
    output = [list(item) for item in a]
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


def produce_bag_generator(generator_seed: str = "") -> Generator[str, None, None]:
    # sourcery skip: simplify-empty-collection-comparison
    'Creates a generator for bags, which will return seeded bags\nIf generator seed is kept as default (empty str), it will produce random, unseeded bags'
    if generator_seed == "":
        yield generate_new_bag()
    else:
        seed(generator_seed)
    while True:
        pieces = list("IJLOSZT")
        shuffle(pieces)
        yield "".join(pieces)


def generate_new_bag():
    'Generates a 14-long sequence of two bags'
    output_list = []
    for _ in range(2):
        piece_list = list("IJLOSZT")
        for _ in range(7):
            # If there is only one piece left, output it and break
            if len(piece_list) == 1:
                output_list.append(piece_list[0])
                break
            a = choice(piece_list)
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
    # sourcery skip: merge-else-if-into-elif, reintroduce-else, use-next
    'Takes a (valid) notation and returns its type, or False if it\'s unrecognizable.'
    n_list = list(notation)
    if len(n_list) >= 4:
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
        if len(n_list) > 13 and len(n_list) < 21:
            return "bag notation"
        else:
            return False


def _get_data_from_replay_line(item: str):
    'Given a line from a replay notation, return the action and the delay in a tuple'
    # float(0) is used to appease mypy
    default_time = float(0)
    i = item.split(" ")[0]
    if len(item.split(" ")) == 1:
        # Setting a default delay value
        time = default_time
    else:
        time = float(item.split(" ")[1])
        time = float(default_time) if time == " " else float(time)
    return i, time


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
    def __init__(self, seed=""):
        self.gen = produce_bag_generator(seed)
        initial_bag = next(self.gen) + next(self.gen) + next(self.gen)
        self.value = initial_bag

    def update(self):
        piece = self.value[0]
        if len(self.value) <= 14:
            self.value = self.value[1:] + next(self.gen)
        else:
            self.value = self.value[1:]
        return piece


class Board():
    'A Tetris board, with a turtle, screen, and data'

    def __init__(self, t, screen, piece_notation="", boardstate="*", bag_seed="", hold="", hold_locked=False):
        self.t = t
        self.screen = screen
        self.boardstate = boardstate
        self.extended_boardstate = boardstate_to_extended_boardstate(
            self.boardstate)
        self.seed = bag_seed
        self.bag = Bag(bag_seed)
        self.hold = hold
        # Boolean for whether the hold is locked or not
        self.hold_locked = hold_locked
        # Weird how you can call functions written after __init__
        if piece_notation == "":
            self.piece = Piece(self.spawn_next_piece(init=True))
        else:
            self.piece = Piece(piece_notation)
        # Non-dynamic init piece board notation
        self.piece_board_notation = f'{self.piece.value}:{self.boardstate}'
        # Initializes an empty replay notation
        self.replay_notation = "start"
        # Initializes the last kick number (for t-spin detection)
        self.last_kick_number = 0
        # Initializes the history of line clears
        self.line_clear_history = ""
        # Starts the clock immediately
        self.start_time = time()
        self.game_over = False

    def hold_piece(self):
        if self.hold_locked:
            # If hold is locked, function shouldn't work
            return False
        # Hold can work, check if hold is empty
        if self.hold == "":
            self.hold = self.piece.type
            self.hold_locked = True
            self.spawn_next_piece()
            # (updates piece board notation in here already)
        else:
            current_piece = self.piece.type
            held_piece = self.hold
            if held_piece in ["L", "J", "S", "T", "I"]:
                x, y = 3, 22
            elif held_piece in ["Z", "O"]:
                x, y = 4, 22
            self.piece.update(held_piece + "0" + str(x) + str(y))
            self.hold = current_piece
            self.hold_locked = True
            self.update_pb_notation()
        return True

    def update_pb_notation(self):
        self.piece_board_notation = construct_piece_board_notation(
            self.piece.value, self.boardstate)

    def display_board(self, pb="", queue="", hold="", hold_locked=""):
        'Displays the current board through Turtle'
        if pb != "":
            p, b = separate_piece_board_notation(pb)
            boardstate = update_boardstate(b, Piece(p))
            if boardstate in ["out of bounds", "occupied cell"]:
                # Meaning the game is over
                raise ValueError(
                    f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
            draw_grid(boardstate, self.t, self.screen)
            # Displays the hold slot and next queue
            # TODO: Change this to non-temporary functions
            display.temp_draw_hold_slot(hold, hold_locked, self.t)
            display.temp_draw_next_queue(queue, self.screen, self.t)
            return True

        # Creates a temporary variable to display the current piece/boardstate
        boardstate = update_boardstate(self.boardstate, self.piece)
        if boardstate in ["out of bounds", "occupied cell"]:
            # Meaning the game is over
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        draw_grid(boardstate, self.t, self.screen)
        # Displays the hold slot and next queue
        # TODO: Change this to non-temporary functions
        display.temp_draw_hold_slot(self.hold, self.hold_locked, self.t)
        display.temp_draw_next_queue(self.bag.value, self.screen, self.t)
        return True

    def spawn_next_piece(self, init=""):
        new_piece_type = self.bag.update()
        # Adjusting spawn coordinates based on piece
        if new_piece_type in ["L", "J", "S", "T", "I"]:
            x, y = 3, 22
        elif new_piece_type in ["Z", "O"]:
            x, y = 4, 22
        if init != "":
            return f'{new_piece_type}0{x}{y}'
        self.piece.update(f'{new_piece_type}0{x}{y}')
        # Checks if the piece can spawn
        b = update_boardstate(self.boardstate, self.piece)
        if b == 'occupied cell':
            # Piece spawn overlaps something, game is over
            self.game_over = True
            return False
        self.update_pb_notation()
        return True

    def move_piece_down(self, subfunction=False):
        if self.piece.y < 1:
            # Piece is too low (touching ground) to be moved down
            return False
        piece_message = self.piece.type + \
            str(self.piece.orientation) + \
            str(self.piece.x) + str(self.piece.y-1)
        # Updates replay notation if this is being called by itself
        if not subfunction:
            self.update_replay_notation("d1")
        return self.check_if_valid(piece_message)

    def change_x(self, value: int):
        '''Moves the piece left or right by a certain amount of cells \n
        Will stop if the piece cannot move \n
        Does not validate the input of cells needed to move'''
        if value > 0:
            func = self.move_piece_right
        elif value < 0:
            func = self.move_piece_left
        else:
            # Value is 0 or not an integer, exit the function
            # No error is thrown
            return False
        # Loop absolute value of the number of cell times
        for _ in range(abs(value)):
            # Call the move_piece_left/right func
            # Piece, board, and piece-board notation are updated in here
            # As this is calling another function, subfunction is set to True
            flag = func(subfunction=True)
            self.display_board()
            # Flag is True if it is successful, False if unsuccessful
            if flag is False:
                # Piece cannot be moved left/right anymore, stop the function
                break
        return True

    def move_piece_left(self, subfunction=False):
        # Create a new piece moved left one cell
        if self.piece.x < 1:
            # Piece cannot be moved left
            # because it will be out of bounds
            return False
        piece_message = self.piece.type + \
            str(self.piece.orientation) + \
            str(self.piece.x-1) + str(self.piece.y)
        # Updates replay notation if this is being called by itself
        if not subfunction:
            self.update_replay_notation("r")
        return self.check_if_valid(piece_message)

    def move_piece_right(self, subfunction=False):
        # Create a new piece moved right one cell
        if self.piece.x > 8:
            # Piece cannot be moved right
            # because it will be out of bounds (handled here)
            return False
        piece_message = self.piece.type + \
            str(self.piece.orientation) + \
            str(self.piece.x+1) + str(self.piece.y)
        # Updates replay notation if this is being called by itself
        if not subfunction:
            self.update_replay_notation("r")
        return self.check_if_valid(piece_message)

    def check_if_valid(self, piece_message):
        b = update_boardstate(self.boardstate, Piece(piece_message))
        if b in ['out of bounds', 'occupied cell']:
            return False
        # Piece message is valid
        # Updates piece and board notation
        self.piece.update(piece_message)
        self.update_pb_notation()
        return True

    def rotate_piece(self, direction: str):  # sourcery skip: class-extract-method
        #self.piece_board_notation = self.piece.value + ":/" + self.boardstate
        pb, kick_number = rotate_and_update(
            self.piece_board_notation, direction)
        # Updates last kick number
        self.last_kick_number = kick_number
        p, b = separate_piece_board_notation(pb)
        # Check if piece cannot rotate
        if p == self.piece.value:
            # Piece cannot rotate, return False
            # (piece and board have not changed)
            return False
        # Piece has rotated
        self.piece.update(p)
        self.boardstate = b
        self.update_pb_notation()
        self.update_replay_notation(direction)
        return True

    def lock_piece(self):
        b = update_boardstate(self.boardstate, self.piece)
        if self.piece.y >= 20:
            # Game is over if piece locks over 21st row (do things and then set game_over to True)
            b, number_of_cleared_lines, list_of_cleared_lines = check_line_clears(
                b)
            pc_message = "pc" if b == "*" else "False" # Check for perfect clear
            tspin = check_t_spin(self.piece_board_notation,
                                 self.replay_notation, self.last_kick_number)
            self.line_clear_history += f"{number_of_cleared_lines} {tspin} {pc_message}\n"
            # Displays the board
            self.display_board()
            self.boardstate = b
            self.hold_locked = False
            self.game_over = True
            return False
        if b in ["out of bounds", "occupied cell"]:
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        b, number_of_cleared_lines, list_of_cleared_lines = check_line_clears(
            b)
        pc_message = "pc" if b == "*" else "False" # Check for perfect clear
        tspin = check_t_spin(self.piece_board_notation,
                                self.replay_notation, self.last_kick_number)
        self.line_clear_history += f"{number_of_cleared_lines} {tspin} {pc_message}\n"
        self.boardstate = b
        # Spawns next piece and updates self.piece
        self.spawn_next_piece()
        # Unlocks hold
        self.hold_locked = False
        self.update_pb_notation()
        # Inverts the game over check (returns True if check is False)
        self.update_replay_notation("lock")
        return True

    def move_down_as_much_as_possible(self):
        # Checks the first down movement
        output = self.move_piece_down(subfunction=True)
        if output is False:
            return False
        # Move down until it is impossible
        flag = True
        while flag:
            flag = self.move_piece_down(subfunction=True)
        self.update_replay_notation("d")
        return True

    def hard_drop(self):
        # Will update replay notation as 'd [newline] lock, not as harddrop'
        flag1 = self.move_down_as_much_as_possible()
        flag2 = self.lock_piece()
        # Returns False if moving down at all was impossible
        return flag1 and flag2

    def move_piece_leftmost(self):
        # Checks the first left movement
        output = self.move_piece_left(subfunction=True)
        if output is False:
            # Returns False if moving left at all was impossible
            return False
        flag = True
        while flag:
            flag = self.move_piece_left(subfunction=True)
        self.update_replay_notation("L")
        return True

    def move_piece_rightmost(self):
        # Checks the first right movement
        output = self.move_piece_right(subfunction=True)
        if output is False:
            # Returns False if moving left at all was impossible
            return False
        flag = True
        while flag:
            flag = self.move_piece_right(subfunction=True)
        self.update_replay_notation("R")
        return True

    def receive_garbage(self, column: int, amount: int):
        'Given a column and an amount of garbage, updates the boardstate'
        # example: g0x5
        garbage = "x"*column + "." + "x"*(9-column)
        # Removes starting asterisk
        # Multiplies the garbage row with the amount
        b = "*" + amount * (garbage + "/") + self.boardstate[1:]
        # Check if blocks are pushed over the 40th row
        if len(b[1:].split("/")) > 40:
            self.game_over = True
        self.boardstate = b
        self.update_pb_notation()
        # Formats the message (e.g. g0x5)
        replay_message = f"g{column}x{amount}"
        # Updates the replay notation
        self.update_replay_notation(replay_message)
        return True

    def load_replay(self, replay: str, seed) -> Tuple[List[str], List[Any], List[Any], List[Any], List[Any]]:
        'Given a replay, simulates it and returns a list of piece-board notations, and a list of delays'
        # FIXME: Incorrectly loads replays (seeding issue?)
        timestamp_list = []
        b1 = Board(self.t, self.screen, "", "*", seed)
        pb_notation_list = [f"{b1.piece_board_notation}"]
        next_queue_list = []
        hold_list = []
        hold_locked_list = []
        for item in replay.split("\n"):
            if item == "start":
                # First line should always be start
                continue
            i, timestamp = _get_data_from_replay_line(item)
            b1.update_pb_notation()
            b1.do_action(i)
            pb_notation_list.append(b1.piece_board_notation)
            next_queue_list.append(b1.bag.value)
            hold_list.append(b1.hold)
            hold_locked_list.append(b1.hold_locked)
            timestamp_list.append(timestamp)
        return pb_notation_list, timestamp_list, next_queue_list, hold_list, hold_locked_list

    def play_replay(self, replay: str, seed):
        pb_list, timestamp_list, next_queue_list, hold_list, hold_locked_list = self.load_replay(
            replay, seed)
        t = time()
        for i, timestamp in enumerate(timestamp_list):
            # Sleep until the timestamp is correct
            while True:
                c = time()
                if c - t >= timestamp:
                    break
            # Then display the board
            self.display_board(
                pb_list[i], next_queue_list[i], hold_list[i], hold_locked_list[i])
        # When replay is finished
        return True

    def do_action(self, i: str):
        flag = False
        # Ignores empty lines (does nothing)
        # Checking the different cases
        if i in {"CW", "CCW", "180"}:
            flag = self.rotate_piece(i)
        elif i == "l":
            flag = self.move_piece_left()
        elif i == "r":
            flag = self.move_piece_right()
        elif i == "L":
            flag = self.move_piece_leftmost()
        elif i == "R":
            flag = self.move_piece_rightmost()
        # d -> moving down as much as possible
        elif i == "d":
            flag = self.move_down_as_much_as_possible()
        # d(n) -> moving down n times
        elif i[0] == "d":
            # Repeat n times moving the piece down (does not check for collision)
            flag = self.move_piece_down()
            for _ in range(int(i[1])):
                self.move_piece_down()
        elif i == "hd":
            flag = self.hard_drop()
        elif i == "lock":
            flag = self.lock_piece()
        elif i == "hold":
            flag = self.hold_piece()
        elif i[0] == "g":
            # e.g. g0x5
            # i[1] is the column, i[3] is the amount of garbage
            self.receive_garbage(int(i[1]), int(i[3]))
        return flag

    def do_actions_from_input(self, input: str):
        'Given an input of a string separated by newlines, performs actions accordingly'
        # CW/CCW/180 -> rotates current piece
        # l/r -> moves current piece left/right
        # L/R -> moves current piece as much left/right as possible
        # d -> moves current piece down as much as possible
        # hd -> d + lock
        # d(n) -> moves current piece by n tiles
        # lock -> locks current piece
        # hold -> holds current piece
        # g0x5 -> receives 5 rows of garbage in column 0
        # TODO: Change the format to be (time since start)
        # separated by a space, and then (time) -> time since last action
        input_list = input.split("\n")
        for item in input_list:
            i, delay = _get_data_from_replay_line(item)
            sleep(delay)
            self.do_action(i)
            self.display_board()

    def get_current_delay(self) -> float:
        'Returns the delay from the time of the start time in seconds (float)'
        # Creates a deep copy of the attribute
        t = float(self.start_time)
        c = time()
        # Returns the delay as a float (rounded to 3 d.p.)
        delay = round(c - t, 2)
        # Trying to correct for processing time
        processing_delay = 0.1
        return 0 if delay < processing_delay else delay

    def update_replay_notation(self, action_notation: str):
        delay = self.get_current_delay()
        # Hide delay is delay = 0 (understood)
        if delay == 0:
            self.replay_notation += f'\n{action_notation}'
        else:
            # Delay is automatically casted to a string
            # Add the action and the delay to a new line in the replay notation
            self.replay_notation += f'\n{action_notation} {delay}'


def init_screen():
    screen = Screen()
    # screen = Screen() takes about 11 seconds on my computer for some reason
    screen.bgcolor("black")
    screen.setup(width=600, height=600)
    screen.title("Tetris")
    t = Turtle()
    screen.tracer(0)
    return t, screen


class Game():
    def __init__(self, mode="vs ai", players=2, replay=""):
        self.mode = mode
        self.players = players
        # T is unused
        t, self.screen = init_screen()
        self.t_list = [Turtle() for _ in range(self.players)]
        # FIXME: A turtle appears in the middle of the screen, hide all turtles
        self.board_list = [Board(t, self.screen) for t in self.t_list]
        self.main_board = self.board_list[0]
        # TODO: Write replay notation (gets appended to in input)

    def display_screens(self):
        for board in self.board_list:
            # TODO: Add support for displaying multiple boards
            board.display_board()

    def mainloop(self, func=lambda:None):
        'Displays all screens while the main board is still going.\nfunc: An optional function that this function will continously print the output of'
        self.input()
        while self.main_board.game_over == False:
            if func != (lambda:None):
                print(func())
            self.display_screens()
        

    def restart_board(self):
        "Restarts main board with the same seed as before"
        self.main_board = Board(
            self.main_board.t, self.screen, "", "*", self.main_board.seed)

    def input(self):
        b = self.board_list[0]
        keybinds = {
            "Up": lambda: b.rotate_piece("CW"),
            "Down": b.move_piece_down,
            "Left": b.move_piece_left,
            "Right": b.move_piece_right,
            "Shift_L": b.hold_piece,
            "c": b.hold_piece,
            "z": lambda: b.rotate_piece("CCW"),
            "a": lambda: b.rotate_piece("180"),
            "space": b.hard_drop,
            "r": self.restart_board,
        }
        for key, action in keybinds.items():
            # should be working keybinds?
            self.screen.onkey(action, key)
        self.screen.listen()


def update_boardstate(boardstate, piecestate: Piece):
    'Takes a boardstate and a Piece, and returns the boardstate with the piece in it, or False if it is impossible'
    # Immediate check whether the piece is out of bounds (to save time)
    if piecestate.x < 0 or piecestate.x > 9 or piecestate.y < 0 or piecestate.y > 39:
        return "out of bounds"
    # Check whether the piece is an O piece and set its orientation to 0 (doesn't matter in updating boardstate)
    if piecestate.type == "O":
        piecestate = Piece("O0" + str(piecestate.x) + str(piecestate.y))
    # Gets a list of offsets from the Piece
    offset_list = find_offset_list(piecestate)
    # Finds the center x and y coordinates
    center_x, center_y = _find_center(piecestate)
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


def _find_center(piecestate: Piece):
    'Given a Piece, returns the coordinates of its actual center (x, y)'
    if piecestate.type == "O":
        # If piece is an O-piece, just check the spawn orientation (there's only 1)
        shape = storage.pieces["O"][0]
    blx, bly = _findBLC(piecestate)
    # The x-offset from the actual x of the piece to the center is 2-blx, same for y
    # Therefore, the center is x+2-blx
    return piecestate.x + 2 - blx, piecestate.y + 2 - bly


def find_offset_list(piecestate: Piece):
    'Given a Piece, returns a list of offsets of each filled tile from the center [(x1, y1), (x2, y2)]'
    # TODO: Might be more efficient (time-wise) to use a lookup table, as there are only 28 possibilities of shapes
    # Accesses global variable pieces
    # Alternative list comprehension (might not be super readable)
    # return [[(cell-2, 2-r) for cell in range(5) if shape[r][cell] == "0"] for r in range(5)]
    ## Previous code:
    # for r in range(5):
    #     for cell in range(5):
    #         if shape[r][cell] == "0":
    #             offset_list.append((cell-2, 2-r))
    # return offset_list
    return storage.offset_list_table[piecestate.type][piecestate.orientation]
    


def update_boardstate_from_pb_notation(pb_notation):
    'Takes a piece-board notation and returns the updated board notation'
    p1, b1 = separate_piece_board_notation(pb_notation)
    return update_boardstate(b1, Piece(p1))


def _findBLC(piece: Piece):
    'Given a shape, finds its bottom left corner relative to a 5x5 grid (helper function to update_boardstate)'
    if piece.type == "O":
        return (1, 1)
    return storage.blc_table[piece.type][piece.orientation]


def _find_difference2(piece: Piece, new_piece: Piece):
    'Takes the type of piece and orientation (e.g. T0) of two pieces and returns their difference in x and y coordinates'
    # FIXME: Hacky fix, might not work
    if piece.type == "O":
        # If piece is an O-piece, make the orientation 0 because all orientations are the same
        # (for the purpose of this function)
        piece.update(piece.type + "0" + str(piece.x) + str(piece.y))
        new_piece.update(new_piece.type + "0" +
                         str(new_piece.x) + str(new_piece.y))
    x, y = _findBLC(piece)
    x2, y2 = _findBLC(new_piece)
    return x2 - x, y2 - y


def _find_kick_table(old_piece: Piece, new_piece: Piece):
    'Given a old piece and a new piece, returns the appropriate kick table'
    # Table for 180 kicks (from tetr.io) if difference in orientation is 2 or -2
    if old_piece.orientation - new_piece.orientation in [2, -2]:
        return storage.flip_table
    # Table for I piece kicks
    elif new_piece.type == "I":
        return storage.i_table
    else:
        # Table for JLSZT piece kicks
        assert new_piece.type in "JLSZT"
        return storage.jlszt_table


def _get_coord_from_kick(x_or_y, kick_tuple):
    'Given a string "x" or "y" and a kick tuple (e.g.) (0, -1), return the corresponding coordinate'
    if x_or_y == "x":
        # Tup is "(0, -1)" and [1:-1].split(", ") makes it into [0, -1] which is the x and y offsets
        return int(kick_tuple[1:-1].split(", ")[0])
    elif x_or_y == "y":
        return int(kick_tuple[1:-1].split(", ")[1])
    else:
        raise ValueError(f"Bad argument, x_or_y is '{x_or_y}'")


def _generate_coords_list(new_piece: Piece, table):
    'Given a piece and a kick table, generate all coordinates of the new piece with kick offsets applied'
    # Get_coord_from table gets the x and y coordinates from the tuple
    return [(int(new_piece.x) + _get_coord_from_kick("x", tup), int(new_piece.y) + _get_coord_from_kick("y", tup)) for tup in table]


def _check_kick_tables(old_piece_notation, new_piece_notation, board_notation):
    '''Takes a piece notation, board notation, direction and returns the piece notation 
    after checking kicktables, or False if rotation is impossible. Also returns the number
    of the kick that was used, or False if rotation is impossible'''
    # Create new Pieces for future reference
    old_piece = Piece(old_piece_notation)
    new_piece = Piece(new_piece_notation)
    # If the piece is O, the rotation will always work, so return the new piece notation
    if new_piece.type == "O":
        return new_piece_notation, 0
    # First, check the original notation if it works
    b = update_boardstate(board_notation, new_piece)
    if b not in ["out of bounds", "occupied cell"]:
        # If there is no problem, return immediately
        return new_piece_notation, 0
    # If it doesn't work, check the kicks
    # Gets a message for the directions that will be looked up later
    direction_message = str(old_piece.orientation) + str(new_piece.orientation)
    # Finds the corresponding kick table
    table = _find_kick_table(old_piece, new_piece)[direction_message]
    # Generate a list with the new coordinates, offsetted with each of the kicks
    # [1:] is to remove first kick (0, 0) that has already been checked
    coords_list = _generate_coords_list(new_piece, table)[1:]
    # Uses a kick_counter (via enumerate) to keep track of which kick this is on (starts on 1st kick)
    for kick_counter, (new_x, new_y) in enumerate(coords_list, start=1):
        # Generate a piece message with the new orientation, and x and y values
        new_piece_message = new_piece.type + \
            str(new_piece.orientation) + str(new_x) + str(new_y)
        b = update_boardstate(board_notation, Piece(new_piece_message))
        if b not in ["out of bounds", "occupied cell"]:
            return new_piece_message, kick_counter
    # This means all kicks have been checked, and none work
    # Return false, meaning rotation is impossible
    return False, False


def _find_rotation_factor(rotation_direction):
    'Given a rotation direction (text), returns the rotation factor associated with that.'
    # Converts the rotation direction into a number used later
    if rotation_direction == "CW":
        return 1
    elif rotation_direction == "CCW":
        return 3
    elif rotation_direction == "180":
        return 2
    else:
        raise ValueError(f"Bad rotation_direction: '{rotation_direction}")


def _find_piece_message(piece: Piece, new_direction: int):
    'Takes a Piece and new direction, and returns the new piece message with updated x and y coordinates'
    new_piece = Piece(piece.type + str(new_direction) +
                      str(piece.x) + str(piece.y))
    # Finds the difference in the two shapes
    x_diff, y_diff = _find_difference2(piece, new_piece)
    # Finds the new x and y coordinates
    new_x, new_y = str(int(piece.x)+x_diff), str(int(piece.y)+y_diff)
    # Returns the new piece message
    return piece.type+str(new_direction)+new_x+new_y


def rotate_and_update(pb_notation, direction):
    '''Takes a piece-board notation and a direction of rotation, \n
    and returns a new piece-board notation with the current piece rotated'''
    piece_n, b = separate_piece_board_notation(pb_notation)
    piece_n = Piece(piece_n)
    rotation_factor = _find_rotation_factor(direction)
    # Finds the new direction based on the original direction and the rotation
    new_direction = (int(piece_n.orientation) + rotation_factor) % 4
    piece_message = _find_piece_message(piece_n, new_direction)
    final_piece_notation, kick_number = _check_kick_tables(
        piece_n.value, piece_message, b)
    # If the piece cannot be rotated (all kicks are checked or it is an O piece)
    if final_piece_notation == False:
        # Make the piece notation the original value
        final_piece_notation = piece_n.value
    return construct_piece_board_notation(final_piece_notation, b), kick_number


def check_line_clears(b_notation):
    'Given a board notation, check whether there are any line clears, and return a tuple of (new board notation, number of lines cleared, which lines were cleared (a list of indices of the original board notation))'
    # Removes starting asterisk and turns it into a list of rows
    b_notation = b_notation[1:].split("/")
    # Makes a copy of board_notation for iteration
    b_notation_copy = list(b_notation)
    filled_rows = []
    for index, row in enumerate(b_notation_copy):
        # Checking for garbage rows first
        # TODO: Clarify
        # Skip empty rows
        if row == "":
            continue
        if row[0] == "g":
            if len(row) != 3 or row[2] == ".":
                # Skip the row
                continue
            # No empty spaces, meaning this is a filled row
            filled_rows.append(index)
            b_notation.remove(row)
        for cell in row:
            # Empty spaces, whether in a garbage row or a normal row
            if cell.isnumeric() == True:
                # Skip this row
                break
        else:
            # No empty spaces, meaning this is a filled row
            filled_rows.append(index)
            # If there are duplicate rows, will remove one of them (both will be removed anyway)
            b_notation.remove(row)
    # Return new board notation, number of rows cleared, which rows were cleared
    # TODO: Determine whether (which rows were cleared) will actually be used or should be removed
    return "*" + "/".join(b_notation), len(filled_rows), filled_rows


def _access_corners(p: Piece, b: str) -> List[bool]:
    'Given a t-Piece, and the board it is in, this accesses and returns the four corners around the center\nReturns True if there is something there and False if the cell is empty'
    center_x, center_y = _find_center(p)
    # Corner offsets (from center) in a clockwise direction from the top left
    offset_list = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
    output_list = []
    # Check each offset to see if it's filled
    for x_offset, y_offset in offset_list:
        new_x, new_y = center_x+x_offset, center_y+y_offset
        # If cell is a wall (considered filled)
        if new_x < 0 or new_x > 9 or new_y < 0:
            output_list.append(True)
        # If cell is empty
        elif access_cell(b, new_y, new_x) == ".":
            output_list.append(False)
        else:
            output_list.append(True)
    return output_list


def _check_corners(p: Piece, b: str):
    filled_list = _access_corners(p, b)
    orientation = p.orientation
    # Magic to access the front and back two corners (e.g. orientation 2, front = 2 and 3, back = 0 and 1)
    front_two_corners = [filled_list[orientation],
                         filled_list[(orientation+1) % 4]]
    back_two_corners = [
        filled_list[(orientation+2) % 4], filled_list[(orientation+3) % 4]]
    # Check if the front two corners are filled and at least one in the back in empty
    if front_two_corners == [True, True] and True in back_two_corners:
        return "t-spin"
    elif True in front_two_corners and back_two_corners == [True, True]:
        return "t-spin mini"
    else:
        return False


def check_t_spin(pb_notation, replay_notation, last_kick_number):
    'Given a piece-board notation and replay notation, return whether this was a t-spin ("t-spin"), t-spin mini ("t-spin mini"), or not a t-spin (False)'
    p, b = separate_piece_board_notation(pb_notation)
    p = Piece(p)
    # Verifies that the piece is a t-piece and that the last movement was a rotation
    # replay notation.split("\n")[-1] will be {action} {delay}, so finds the action
    if p.type != "T" or replay_notation.split("\n")[-1].split(" ")[0] not in {'CW', 'CCW', '180'}:
        return False
    message = _check_corners(p, b)
    # Message will be t-spin, t-spin mini, or False
    if message == "t-spin mini" and last_kick_number == 4:
        # If the last kick is 4, this is a t-spin, not a t-spin mini (e.g. STSD)
        return "t-spin"
    return message


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


def slideshow(slides, t, screen):
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
