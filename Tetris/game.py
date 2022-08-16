from atk_table import attack_table
from board import Board

from random import choice, randint
from time import time
from turtle import Screen, Turtle


def init_screen(width=1200):
    screen = Screen()
    screen.bgcolor("black")
    screen.setup(width, height=600)
    screen.title("Tetris")
    t = Turtle()
    t.hideturtle()
    screen.tracer(0)
    return t, screen


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
        elif ai == "none":
            pass

    def random_input(self, board):
        actions = ["CW", "CCW", "d", "l", "r", "L", "R", "hold"]
        self.auto_input(choice(actions), board)
        self.auto_input(choice(actions), board)
        self.auto_input(choice(actions), board)
        self.auto_input("hd", board)

    def mainloop(self, func=None):
        'Displays all screens while the main board is still going.\nfunc: An optional function that this function will continously display the output of'
        self.manual_input()
        while self.main_board.game_over == False:
            if func != None:
                self.main_board.display_message(func())
            self.display_screens()
            if self.players == 2 and self.mode == "vs ai":
                self.ai_input("none")

    def restart_board(self):
        "Restarts main board with the same seed as before"
        self.main_board = Board(
            self.main_board.t, self.screen, "", "*", self.main_board.seed)

    def auto_lock_piece(self, board_index: int):
        board = self.board_list[board_index]
        board.do_action("hd")
        # check if this will fail for first lock
        clear = board.line_clear_history[-1]
        lines, b2b, combo, tspin, pc = clear.split("/")
        if int(lines) == 0:
            return False
        # translate line clear history b2b into attack table b2b
        if int(b2b) > 0:
            b2b = int(b2b) - 1
        # 0 -> 0, 1 -> 0, 2-> 1
        # {number_of_cleared_lines}/{b2b}/{combo}/{tspin}/{pc_message}
        attack = attack_table(int(lines), int(b2b), int(combo), tspin, pc)
        # find target board
        target_board = self.board_list[self.target_boards[board_index]]
        # receive garbage on target board
        # TODO: garbage queue
        target_board.receive_garbage(randint(0, 9), attack)

    def manual_input(self):
        b = self.board_list[0]
        keybinds2 = {
            "Up": lambda: b.do_action("CW"),
            "Down": lambda: b.do_action("d"),
            "Left": lambda: b.do_action("l"),
            "Right": lambda: b.do_action("r"),
            "Shift_L": lambda: b.do_action("hold"),
            "c": lambda: b.do_action("hold"),
            "z": lambda: b.do_action("CCW"),
            "a": lambda: b.do_action("180"),
            "space": lambda: self.auto_lock_piece(0)
        }
        for key, action in keybinds2.items():
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
        else:
            b.do_action(action)
