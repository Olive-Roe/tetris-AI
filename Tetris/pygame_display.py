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
    # ghost pieces
    "navy": (0, 0, 255, 128),
    "teal": (0, 255, 255, 128),
    "purple": (255, 0, 255, 128),
    "dark orange": (255, 165, 0, 128),
    "olive": (255, 255, 0, 128),
    "maroon": (255, 0, 0, 128),
    "green": (0, 255, 0, 128),
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
    lineColor = (50, 50, 50)  # dark gray
    X, Y = startX, startY
    # Draw grid
    for i in range(40):
        for j in range(10):
            s = pygame.Surface((20, 20))
            if rgb[i][j] in [
                "navy",
                "teal",
                "purple",
                "dark orange",
                "maroon",
                "green",
                "olive",
            ]:
                s.set_alpha(128)  # ghost pieces
            s.fill(color_dict[rgb[i][j]])
            screen.blit(s, (X, Y))
            # pygame.draw.rect(screen, color_dict[rgb[i][j]], (X, Y, 20, 20))
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


def draw_piece(screen, piecetype: str, x, y, locked=False):
    if piecetype == "J":
        pygame.draw.rect(screen, color_dict["grey"], (x, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["blue"], (x + 1, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["blue"], (x - 19, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["blue"], (x - 19, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["blue"], (x + 21, y + 11, 18, 18))
    elif piecetype == "L":
        pygame.draw.rect(screen, color_dict["grey"], (x, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["orange"], (x + 1, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["orange"], (x - 19, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["orange"], (x + 21, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["orange"], (x + 21, y + 11, 18, 18))
    elif piecetype == "S":
        pygame.draw.rect(screen, color_dict["grey"], (x, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["lime"], (x + 1, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["lime"], (x + 1, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["lime"], (x + 21, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["lime"], (x - 19, y + 11, 18, 18))
    elif piecetype == "Z":
        pygame.draw.rect(screen, color_dict["grey"], (x, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["red"], (x + 1, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["red"], (x + 1, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["red"], (x - 19, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["red"], (x + 21, y + 11, 18, 18))
    elif piecetype == "T":
        pygame.draw.rect(screen, color_dict["grey"], (x, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 20, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 20, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["magenta"], (x + 1, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["magenta"], (x - 19, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["magenta"], (x + 1, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["magenta"], (x + 21, y + 11, 18, 18))
    elif piecetype == "O":
        pygame.draw.rect(screen, color_dict["grey"], (x - 10, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 10, y + 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 10, y - 10, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 10, y + 10, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["yellow"], (x - 9, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["yellow"], (x - 9, y + 11, 18, 18))
            pygame.draw.rect(screen, color_dict["yellow"], (x + 11, y - 9, 18, 18))
            pygame.draw.rect(screen, color_dict["yellow"], (x + 11, y + 11, 18, 18))
    elif piecetype == "I":
        pygame.draw.rect(screen, color_dict["grey"], (x - 10, y, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 10, y, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x - 30, y, 20, 20))
        pygame.draw.rect(screen, color_dict["grey"], (x + 30, y, 20, 20))
        if locked == False:
            pygame.draw.rect(screen, color_dict["cyan"], (x - 9, y + 1, 18, 18))
            pygame.draw.rect(screen, color_dict["cyan"], (x + 11, y + 1, 18, 18))
            pygame.draw.rect(screen, color_dict["cyan"], (x - 29, y + 1, 18, 18))
            pygame.draw.rect(screen, color_dict["cyan"], (x + 31, y + 1, 18, 18))


def update_hold(screen, hold_piece, hold_locked, board_x, board_y):
    draw_piece(screen, hold_piece, board_x - 155, board_y - 180, hold_locked)


def update_next(screen, bag_notation, board_x, board_y, n_of_previews=5):
    for i in range(n_of_previews):
        draw_piece(screen, bag_notation[i], board_x + 155, board_y - 180 + 70 * i)


def update_garbage_meter(screen, garbage_list: list[tuple], board_x, board_y):
    y = board_y + 210
    for column, amount in garbage_list:
        pygame.draw.rect(
            screen,
            Color.red,
            (board_x + 105, y - 20 * amount + 5, 5, 20 * amount - 5),
        )
        y -= 20 * amount


from board_processing import create_grid, board_notation_to_dict
from updating_board import add_ghost_piece_and_update
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
        self.target_boards = [1, 0]
        # TODO: Write replay notation (gets appended to in input)

    def display_screens(self):
        for index, board in enumerate(self.board_list):
            xpos, ypos = self.positions[index]
            boardstate = add_ghost_piece_and_update(board.piece, board.boardstate)
            if boardstate in ["out of bounds", "occupied cell"]:
                # Meaning the game is over
                raise ValueError(
                    f"Impossible piece lock, piece: '{board.piece.value}', board: '{board.boardstate}'"
                )
            rgb = create_grid(board_notation_to_dict(boardstate))

            update_grid(rgb, self.screen, xpos, ypos)
            update_hold(self.screen, board.hold, board.hold_locked, xpos, ypos)
            update_next(self.screen, board.bag.value, xpos, ypos)
            update_garbage_meter(self.screen, board.garbage_queue, xpos, ypos)

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
            screen.fill(color_dict["black"])
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
            # TODO: customisable keybinds
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
        lines, b2b, combo, tspin, pc, pblocked = clear.split("/")
        if int(lines) == 0:
            return False
        # translate line clear history b2b into attack table b2b
        if int(b2b) > 0:
            b2b = int(b2b) - 1
        # {number_of_cleared_lines}/{b2b}/{combo}/{tspin}/{pc_message}
        attack = attack_table(int(lines), int(b2b), int(combo), tspin, pc)
        if attack == 0:
            return False
        # Subtract the amount used to block incoming garbage
        attack -= int(pblocked)
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
