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
    gray = pygame.Color(128, 128, 128)


color_dict = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "lime": (0, 255, 0),
    "gray": (128, 128, 128),
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
    font_obj = pygame.font.SysFont("Verdana", fontsize)
    msg_surface_obj = font_obj.render(text, False, color_dict["white"])
    msg_rect_obj = msg_surface_obj.get_rect()
    msg_rect_obj.topleft = (x, y)
    screen.blit(msg_surface_obj, msg_rect_obj)


if __name__ == "__main__":
    screen = init_screen()
    screen.fill(Color.black)
    while True:
        update_grid(rgb, screen)
        write_text(screen, "Hola", 50, 100)
        pygame.display.update()
        FPS_CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
