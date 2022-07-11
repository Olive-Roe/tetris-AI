from time import time, sleep
from board_processing import create_grid, board_notation_to_dict, check_type_notation, separate_piece_board_notation, extended_boardstate_to_boardstate, boardstate_to_extended_boardstate, construct_piece_board_notation
from updating_board import update_boardstate, add_ghost_piece_and_update, rotate_and_update, check_line_clears, check_t_spin
from bag import Bag
from piece import Piece
import display
from typing import Any, Tuple, List


def draw_grid(board_notation, t, screen, x=0, y=0):
    display.draw_grid(create_grid(
        board_notation_to_dict(board_notation)), t, screen, x, y)


def _get_data_from_replay_line(item: str):
    'Given a line from a replay notation, return the action and the delay in a tuple'
    default_time: float = 0
    i = item.split(" ")[0]
    if len(item.split(" ")) == 1:
        # Setting a default delay value
        time = default_time
    else:
        time = float(item.split(" ")[1])
        time = default_time if time == " " else time
    return i, time


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


class Board:
    'A Tetris board, with a turtle, screen, and data'

    def __init__(self, t, screen, piece_notation="", boardstate="*", bag_seed="", hold="", hold_locked=False):
        self.t = t
        self.screen = screen
        self.boardstate = boardstate
        self.extended_boardstate = boardstate_to_extended_boardstate(
            self.boardstate)
        if bag_seed == "":
            self.seed = time()
            self.bag = Bag(self.seed)
        else:
            self.seed = bag_seed
            self.bag = Bag(bag_seed)
        self.hold = hold
        # Boolean for whether the hold is locked or not
        self.hold_locked = hold_locked
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
        self.line_clear_history = []
        # Initalizes the history of piece placements
        self.piece_placement_history = []
        # Initializes the number of pieces placed
        self.pieces_placed = 0
        # Initialize garbage queue
        self.garbage_queue = 0
        # Starts the clock immediately
        self.start_time = time()
        self.game_over = False

    def pps(self):
        'Returns the number of pieces per second (to 3dp) as of this function being called'
        return round(self.pieces_placed/(time()-self.start_time), 3)

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
            self.piece.update(f'{held_piece}0{x}{y}')
            self.hold = current_piece
            self.hold_locked = True
            self.update_pb_notation()
        return True

    def update_pb_notation(self):
        self.piece_board_notation = construct_piece_board_notation(
            self.piece.value, self.boardstate)

    def display_message(self, message):
        display.write_text(self.t, self.screen, message)

    def display_board(self, pb="", queue="", hold="", hold_locked="", x=0, y=0):
        'Displays the current board through Turtle'
        if pb != "":
            p, b = separate_piece_board_notation(pb)
            boardstate = add_ghost_piece_and_update(p, b), Piece(p)
            if boardstate in ["out of bounds", "occupied cell"]:
                # Meaning the game is over
                raise ValueError(
                    f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
            draw_grid(boardstate, self.t, self.screen, x, y)
            # Displays the hold slot and next queue
            # TODO: Change this to non-temporary functions
            display.temp_draw_hold_slot(hold, hold_locked, self.t, x, y)
            display.temp_draw_next_queue(queue, self.screen, self.t, x=x, y=y)
            return True

        # Creates a temporary variable to display the current piece/boardstate
        boardstate = add_ghost_piece_and_update(self.piece, self.boardstate)
        if boardstate in ["out of bounds", "occupied cell"]:
            # Meaning the game is over
            raise ValueError(
                f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
        draw_grid(boardstate, self.t, self.screen, x, y)
        # Displays the hold slot and next queue
        # TODO: Change this to non-temporary functions
        display.temp_draw_hold_slot(self.hold, self.hold_locked, self.t, x, y)
        display.temp_draw_next_queue(
            self.bag.value, self.screen, self.t, x=x, y=y)
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
        # self.piece_board_notation = self.piece.value + ":/" + self.boardstate
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
        return True

    def lock_piece(self):
        b = update_boardstate(self.boardstate, self.piece)
        if self.piece.y >= 20:
            # Game is over if piece locks over 21st row (do things and then set game_over to True)
            # TODO: clean up messy code
            if self.line_clear_history == []:
                # first piece lock
                self.line_clear_history.append("0/0/0/False/False")
            else:
                b, number_of_cleared_lines, list_of_cleared_lines = check_line_clears(
                    b)
                pc_message = "pc" if b == "*" else "False"  # Check for perfect clear
                tspin = check_t_spin(self.piece_board_notation,
                                     self.replay_notation, self.last_kick_number)
                prev_line = self.line_clear_history[-1].split("/")
                # previous values
                plines, pb2b, pcombo, ptspin, ppc = prev_line
                if number_of_cleared_lines == 0:
                    self.line_clear_history.append(f"0/{pb2b}/0/{tspin}/False")
                else:
                    # work out combo
                    combo = 0 if plines == 0 else int(pcombo) + 1
                    # work out back to back
                    b2b = int(pb2b) + \
                        1 if int(
                            number_of_cleared_lines) == 4 or tspin != "False" else 0
                    self.line_clear_history.append(
                        f"{number_of_cleared_lines}/{b2b}/{combo}/{tspin}/{pc_message}")
            self.piece_placement_history.append(self.piece.value)
            self.pieces_placed += 1
            # Displays the board
            self.display_board()
            self.boardstate = b
            self.hold_locked = False
            self.game_over = True
            return False
        # game is still going
        if self.line_clear_history == []:
            # first piece lock
            self.line_clear_history.append("0/0/0/False/False")
        else:
            if b in ["out of bounds", "occupied cell"]:
                raise ValueError(
                    f"Impossible piece lock, piece: '{self.piece.value}', board: '{self.boardstate}'")
            b, number_of_cleared_lines, list_of_cleared_lines = check_line_clears(
                b)
            pc_message = "pc" if b == "*" else "False"  # Check for perfect clear
            tspin = check_t_spin(self.piece_board_notation,
                                 self.replay_notation, self.last_kick_number)
            prev_line = self.line_clear_history[-1].split("/")
            # previous values
            plines, pb2b, pcombo, ptspin, ppc = prev_line
            if number_of_cleared_lines == 0:
                self.line_clear_history.append(f"0/{pb2b}/0/{tspin}/False")
            else:
                # work out combo
                combo = 0 if plines == 0 else int(pcombo) + 1
                # work out back to back
                b2b = int(pb2b) + \
                    1 if int(
                        number_of_cleared_lines) == 4 or tspin != "False" else 0
                self.line_clear_history.append(
                    f"{number_of_cleared_lines}/{b2b}/{combo}/{tspin}/{pc_message}")
            self.piece_placement_history.append(self.piece.value)
            self.pieces_placed += 1
            self.boardstate = b
            # Spawns next piece and updates self.piece
            self.spawn_next_piece()
            # Unlocks hold
            self.hold_locked = False
            self.update_pb_notation()
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
        return True

    def receive_garbage(self, column: int, amount: int):
        'Given a column and an amount of garbage, updates the boardstate'
        # example: g0x5
        garbage = "x"*column + "." + "x"*(9-column)
        # Removes starting asterisk
        # Multiplies the garbage row with the amount
        b = "*" + amount * f'{garbage}/' + self.boardstate[1:]
        # Check if blocks are pushed over the 40th row
        if len(b[1:].split("/")) > 40:
            self.game_over = True
        self.boardstate = b
        self.update_pb_notation()
        return True

    def load_replay(self, replay: str, seed) -> Tuple[List[str], List[Any], List[Any], List[Any], List[Any]]:
        'Given a replay, simulates it and returns a list of piece-board notations, and a list of delays'
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
            try:
                b1.do_action(i)
            except ValueError:  # Impossible piece lock
                continue  # Skip this line
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
            # i[1] is the column (0-9), i[3:] is the amount of garbage (can be more than 1 digit)
            self.receive_garbage(int(i[1]), int(i[3:]))
        self.update_replay_notation(i)
        return flag

    def do_actions_from_input(self, input: str):
        'Given an input of a string separated by newlines, performs actions accordingly'
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
