import pygame
import sys
from pygame.locals import *

pygame.init()

FPS_CLOCK = pygame.time.Clock()

BOARD = [[[j for j in range(40)] for i in range(10)]]
QUEUE = ""
HOLD = ""
HOLD_LOCKED = False
TEXT = ""

rgb = [
    [
        "blue",
        "blue",
        "blue",
        "cyan",
        "black",
        "black",
        "black",
        "red",
        "red",
        "magenta",
    ],
    [
        "yellow",
        "yellow",
        "blue",
        "cyan",
        "black",
        "black",
        "red",
        "red",
        "magenta",
        "magenta",
    ],
    [
        "yellow",
        "yellow",
        "orange",
        "cyan",
        "black",
        "black",
        "black",
        "lime",
        "lime",
        "magenta",
    ],
    [
        "orange",
        "orange",
        "orange",
        "cyan",
        "black",
        "black",
        "black",
        "black",
        "lime",
        "lime",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
    [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
]


class Color:
    black = pygame.Color(0, 0, 0)
    blue = pygame.Color(0, 0, 255)
    cyan = pygame.Color(0, 255, 255)
    magenta = pygame.Color(255, 0, 255)
    orange = pygame.Color(255, 165, 0)
    yellow = pygame.Color(255, 255, 0)
    red = pygame.Color(255, 0, 0)
    lime = pygame.Color(0, 255, 0)
    grey = pygame.Color(128, 128, 128)


color_dict = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "lime": (0, 255, 0),
    "grey": (128, 128, 128),
    "white": (255, 255, 255),
}


def init_screen(width=1200, height=600):
    screen = pygame.display.set_mode((width, height))
    pygame.display.update()
    pygame.display.set_caption("Tetris")
    return screen


def draw_grid(rgb, screen, x=0, y=0):
    global BOARD
    BOARD = rgb


def update_grid(rgb, screen, x=600, y=300):
    startX = x - 100
    startY = y + 190
    lineWidth = 2
    lineColor = (128, 128, 128)  # gray
    X, Y = startX, startY
    # Draw grid
    for i in range(40):
        for j in range(10):
            pygame.draw.rect(screen, color_dict[rgb[i][j]], (X, Y, 20, 20))
            X += 20
        Y -= 20
        X = x - 100
    # Draw lines
    for x1 in range(x - 100, x + 120, 20):
        pygame.draw.line(
            screen, lineColor, (x1, startY + 20), (x1, startY - 380), lineWidth
        )
    for y1 in range(startY + 20, startY - 400, -20):
        pygame.draw.line(screen, lineColor, (startX, y1), (startX + 200, y1), lineWidth)


def write_text(screen, text, x=0, y=0, fontsize=32):
    font_obj = pygame.font.SysFont("Avenir", fontsize)
    msg_surface_obj = font_obj.render(text, False, color_dict["white"])
    msg_rect_obj = msg_surface_obj.get_rect()
    msg_rect_obj.topleft = (x, y)
    screen.blit(msg_surface_obj, msg_rect_obj)


from board_processing import create_grid, board_notation_to_dict
from time import time
from board import Board
import mackerel_AI
from atk_table import attack_table
import random


class Game:
    def __init__(self, mode="vs ai", players=2, replay=""):
        self.mode = mode
        # modes = "vs ai", "sprint", "ultra", "cheese"
        self.players = players
        self.seed = str(time())
        self.screen = init_screen(600 if players == 1 else 1200)
        self.board_list = [
            Board(None, self.screen, bag_seed=self.seed) for i in range(players)
        ]
        if players == 1:
            self.positions = [(300, 300)]
        if players == 2:
            self.positions = [(300, 300), (900, 300)]
        self.main_board = self.board_list[0]
        # TODO: targetting system
        self.target_boards = [1, 0]
        # TODO: Write replay notation (gets appended to in input)

    def display_screens(self):
        for index, board in enumerate(self.board_list):
            xpos, ypos = self.positions[index]
            rgb = create_grid(board_notation_to_dict(board.boardstate))
            update_grid(rgb, self.screen, xpos, ypos)

    def text_next_to_board(self, text, board_index):
        x, y = self.positions[board_index]
        write_text(self.screen, text, x + 10, y + 10, 18)

    def ai_input(self, ai="random", board=1):  # sourcery skip: remove-pass-elif
        b = self.board_list[board]
        if ai == "random":
            self.random_input(board) 
        elif ai == "mackerel":
            # sees 21 pieces but that's ok
            movepath = mackerel_AI.best_move(
                b.boardstate, b.piece.type, b.hold, b.bag.value
            )
            b.do_actions_from_input("\n".join(movepath), display=False)
            self.send_garbage(board)

    def random_input(self, board):
        actions = ["CW", "CCW", "d", "l", "r", "L", "R", "hold"]
        for _ in range(3):
            self.auto_input(random.choice(actions), board)
        self.auto_input("hd", board)

    def mainloop(self, func=None):
        "Displays all screens while the main board is still going.\nfunc: An optional function that this function will continously display the output of"
        # TODO: supports at most 2 boards
        # stops loop once at least one board is dead
        while True:
            if any(b.game_over for b in self.board_list):
                break
            self.display_screens()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            FPS_CLOCK.tick(60)
            # Text display on screen
            if func != None:
                self.text_next_to_board(func())
            # AI input (non turnbased)
            if self.players == 2 and self.mode == "vs ai":
                self.ai_input("random")
            # Keybinds
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.auto_input("CW", 0)
            if keys[pygame.K_DOWN]:
                self.auto_input("d", 0)
            if keys[pygame.K_LEFT]:
                self.auto_input("l", 0)
            if keys[pygame.K_RIGHT]:
                self.auto_input("r", 0)
            if keys[pygame.K_LSHIFT]:
                self.auto_input("hold", 0)
            if keys[pygame.K_RSHIFT]:
                self.auto_input("hold", 0)
            if keys[pygame.K_c]:
                self.auto_input("hold", 0)
            if keys[pygame.K_z]:
                self.auto_input("CCW", 0)
            if keys[pygame.K_a]:
                self.auto_input("180", 0)
            if keys[pygame.K_SPACE]:
                self.auto_input("hd", 0)
        # TODO: track who won, make larger class for multiple round matches

    def restart_board(self):
        "Restarts main board with the same seed as before"
        self.main_board = Board(
            self.main_board.t, self.screen, "", "*", self.main_board.seed
        )

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

    def auto_input(self, action: str, board_index: int):
        # sourcery skip: remove-redundant-if
        "Takes an action string and board number (index of board lists), and automatically does that input"
        assert board_index < len(self.board_list)
        b = self.board_list[board_index]
        if action in {"hd", "lock"}:
            self.auto_lock_piece(board_index)
            if board_index == 0 and self.players > 1 and self.mode == "vs ai turnbased":
                self.ai_input("mackerel", 1)
        else:
            b.do_action(action)


# create_grid(board_notation_to_dict(board_notation))

if __name__ == "__main__":
    screen = init_screen()
    screen.fill(Color.black)

    g = Game("vs ai turnbased")
    g.mainloop()
    # while True:
    #     update_grid(rgb, screen, 300, 300)
    #     update_grid(rgb, screen, 900, 300)
    #     write_text(screen, "Hola", 410, 110, 18)
    #     pygame.display.update()
    #     FPS_CLOCK.tick(60)
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             pygame.quit()
    #             sys.exit()
