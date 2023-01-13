from atk_table import attack_table
from display import init_screen
from board import Board
import AI
import mackerel_AI
import random
from time import time
from turtle import Screen, Turtle


class Game:
    def __init__(self, mode="vs ai", players=2, replay=""):
        self.mode = mode
        # modes = "vs ai", "sprint", "ultra", "cheese"
        self.players = players
        self.seed = time()
        # T is unused
        t, self.screen = init_screen(600 if players == 1 else 1200)
        self.t_list = [Turtle() for _ in range(self.players)]
        for t in self.t_list:
            t.hideturtle()
        self.board_list = [Board(t, self.screen, bag_seed=self.seed)
                           for t in self.t_list]
        if players == 1:
            self.positions = [(0, 0)]
        if players == 2:
            self.positions = [(-300, 0), (300, 0)]
        self.main_board = self.board_list[0]
        # TODO: targetting system
        self.target_boards = [1, 0]
        # TODO: Write replay notation (gets appended to in input)

    def display_screens(self):
        for index, board in enumerate(self.board_list):
            xpos, ypos = self.positions[index]
            board.display_board(x=xpos, y=ypos)

    def ai_input(self, ai="random", board=1):  # sourcery skip: remove-pass-elif
        b = self.board_list[board]
        b_list = self.board_list
        if ai == "random":
            self.random_input(1)
        elif ai == "true random":
            # move_dict = AI.find_possible_moves(b.boardstate, b.piece.type, b.hold)
            # movepath = random.choice(list(move_dict.values()))
            movepath = mackerel_AI.best_move(
                b.boardstate, b.piece.type, b.hold)
            b.do_actions_from_input("\n".join(movepath))

    def random_input(self, board):
        actions = ["CW", "CCW", "d", "l", "r", "L", "R", "hold"]
        for _ in range(3):
            self.auto_input(random.choice(actions), board)
        self.auto_input("hd", board)

    def mainloop(self, func=None):
        'Displays all screens while the main board is still going.\nfunc: An optional function that this function will continously display the output of'
        self.manual_input()
        # TODO: supports at most 2 boards
        # stops loop once at least one board is dead
        while not any(b.game_over for b in self.board_list):
            if func != None:
                self.main_board.display_message(func())
            self.display_screens()
            if self.players == 2 and self.mode == "vs ai":
                self.ai_input("random")
        # TODO: track who won, make larger class for multiple round matches

    def restart_board(self):
        "Restarts main board with the same seed as before"
        self.main_board = Board(
            self.main_board.t, self.screen, "", "*", self.main_board.seed)

    def send_garbage(self, board_index: int):
        board = self.board_list[board_index]
        clear = board.line_clear_history[-1]
        lines, b2b, combo, tspin, pc = clear.split("/")
        if int(lines) == 0:
            return False
        # translate line clear history b2b into attack table b2b
        if int(b2b) > 0:
            b2b = int(b2b) - 1
        # {number_of_cleared_lines}/{b2b}/{combo}/{tspin}/{pc_message}
        attack = attack_table(int(lines), int(b2b), int(combo), tspin, pc)
        # find target board
        target_board = self.board_list[self.target_boards[board_index]]
        # receive garbage on target board
        target_board.garbage_queue.append((random.randint(0, 9), attack))

    def auto_lock_piece(self, board_index: int):
        board = self.board_list[board_index]
        board.do_action("hd")
        if self.players > 1:
            self.send_garbage(board_index)

    def manual_input(self):
        b = self.board_list[0]
        self.auto_input("CW", 0)
        keybinds3 = {
            "Up": lambda: self.auto_input("CW", 0),
            "Down": lambda: self.auto_input("d", 0),
            "Left": lambda: self.auto_input("l", 0),
            "Right": lambda: self.auto_input("r", 0),
            "Shift_L": lambda: self.auto_input("hold", 0),
            "c": lambda: self.auto_input("hold", 0),
            "z": lambda: self.auto_input("CCW", 0),
            "a": lambda: self.auto_input("180", 0),
            "space": lambda: self.auto_input("hd", 0)
        }
        for key, action in keybinds3.items():
            # should be working keybinds?
            self.screen.onkeypress(action, key)
        self.screen.listen()

    def auto_input(self, action: str, board_index: int):
        # sourcery skip: remove-redundant-if
        "Takes an action string and board number (index of board lists), and automatically does that input"
        assert board_index < len(self.board_list)
        b = self.board_list[board_index]
        if action in {"hd", "lock"}:
            self.auto_lock_piece(board_index)
            if board_index == 0 and self.players > 1 and self.mode == "vs ai turnbased":
                self.ai_input("true random", 1)
        else:
            b.do_action(action)
