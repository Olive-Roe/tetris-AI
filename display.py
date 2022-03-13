from asyncore import write
from random import randint
from turtle import Screen, Turtle

color_dict = {(0, 0, 0): "black",
              (0, 0, 255): "blue",
              (0, 255, 255): "cyan",
              (255, 0, 255): "magenta",
              (255, 165, 0): "orange",
              (255, 255, 0): "yellow",
              (255, 0, 0): "red",
              (0, 255, 0): "lime",
              (128, 128, 128): "gray",
              }


def draw_square(width, color, t):
    '''Process to draw a square on the upper right of turtle
    of color 'color' and width 'width', provided with the turtle 't'.'''
    global color_dict
    # If the color is an RGB tuple, check the color dict for the
    # appropriate name, else just use the color string.
    if type(color) == tuple:
        color = color_dict[color]
    # Speeds up black square on black background by not drawing it
    if color == "black":
        return None
    # Make the turtle the right color
    t.fillcolor(color)
    t.begin_fill()
    # Draw the square
    for _ in range(4):
        t.forward(width)
        t.right(90)
    # FIll the square
    t.end_fill()


def draw_outline(t: Turtle, screen, startX, startY, color="white"):
    # Draws outline (200x400 rectangle)
    t.setheading(0)
    t.pencolor(color)
    t.penup()
    t.goto(startX, startY)
    t.pendown()
    for _ in range(2):
        t.forward(200)
        t.left(90)
        t.forward(400)
        t.left(90)
    t.penup()


def draw_grid(rgb, t: Turtle, screen, x=0, y=0):
    '''Draws a grid, given a dictionary of colors and coordinates
    'rgb', and provided the turtle 't' and screen 'screen'.
    Optional argument x, y are the coordinates of the center of the grid.'''
    # Hide the turtle
    t.hideturtle()
    # Clear the current board
    t.clear()
    # Set the pencolor to black (black outline of squares)
    t.pencolor("black")
    startX = x-100
    startY = y-200
    # Make turtle fastest (doesn't matter with screen update)
    t.speed(0)
    # Go to the set starting location
    t.goto(startX, startY)
    t.pendown()
    # Face north
    t.setheading(0)
    # Max height = 40
    for i in range(40):
        t.goto(startX, startY+((i+1)*20))
        for j in range(10):
            draw_square(20, rgb[i][j], t)
            t.forward(20)
    # Draw white grid lines
    t.penup()
    t.goto(startX, startY)
    t.pendown()
    t.setheading(90)
    t.color("#808080")
    for _ in range(10):
        t.fd(20)
        t.right(90)
        t.fd(200)
        t.left(90)
        t.fd(20)
        t.left(90)
        t.fd(200)
        t.right(90)
    t.setheading(90)
    for _ in range(5):
        t.right(90)
        t.fd(20)
        t.right(90)
        t.fd(400)
        t.left(90)
        t.fd(20)
        t.left(90)
        t.fd(400)
    draw_outline(t, screen, startX, startY, "#808080")
    # Updates the screen when it is done
    screen.update()


def draw_hold_slot(piece: str, locked: bool):
    # TODO: Make hold slot
    pass


def temp_draw_hold_slot(piece: str, locked: bool, t: Turtle, x=0, y=0):
    t = Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.goto(x-250, y+200)
    t.setheading(0)
    t.color("white")
    t.fillcolor("black")
    t.begin_fill()
    t.pendown()
    t.forward(100)
    t.right(90)
    t.forward(50)
    t.right(90)
    t.forward(100)
    t.right(90)
    t.forward(50)
    t.right(90)
    t.end_fill()
    t.penup()
    t.penup()
    t.goto(x-200, y+160)
    FONT = ('Verdana', 12, 'normal')
    t.color('white')
    t.pendown()
    t.write(f'Hold: {piece}\nLocked: {locked}', font=FONT, align='center')
    t.penup()


def temp_draw_next_queue(bag_notation: str, screen, t: Turtle, n_of_previews=3, x=0, y=0):
    t = Turtle()
    t.hideturtle()
    t.speed(0)
    # Draw black rectangle to mask
    t.penup()
    t.setposition(x+145, y+200)
    # Face east
    t.setheading(0)
    t.color("white")
    t.fillcolor("black")
    t.begin_fill()
    t.pendown()
    t.forward(110)
    t.right(90)
    t.forward(50)
    t.right(90)
    t.forward(110)
    t.right(90)
    t.forward(50)
    t.right(90)
    t.end_fill()
    t.penup()
    FONT = ('Verdana', 12, 'normal')
    t.color('white')
    t.goto(x+200, y+180)
    t.pendown()
    t.write(
        f'Next Pieces: {bag_notation[:n_of_previews]}', font=FONT, align='center')
    t.penup()


def draw_next_queue(bag_notation: str, screen, n_of_previews=3):
    # TODO: Make next queue
    t = Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("white")
    startX = 100
    startY = 200
    t.penup()
    t.goto(startX, startY)
    t.pendown()
    # Face east
    t.setheading(2)
    t.goto(200, 200)
    t.goto(200, 180)
    t.goto(100, 180)
    t.penup()
    t.setposition(150, 180)
    FONT = ('Verdana', 2, 'normal')
    t.color('white')
    t.pendown()
    t.write('Next Pieces', font=FONT, align='center')
    t.hideturtle()
    t.penup()
    t.setposition(200, 180)
    t.setheading(3)
    t.pendown()
    t.goto(200, -120)
    t.goto(100, -120)
    screen.update()


def write_text(t: Turtle, screen, text, x=0, y=0):
    'Draws a box and displays text'
    t = Turtle()
    text = str(text)
    line_length = 12*len(text.split("\n"))
    FONT = ('Verdana', 12, 'normal')
    t.speed(0)
    t.penup()
    t.goto(x+145, y+100)
    t.pendown()
    t.color("white")
    t.fillcolor("black")
    t.begin_fill()
    t.fd(100)
    t.right(90)
    t.fd(line_length+20)
    t.right(90)
    t.fd(100)
    t.right(90)
    t.fd(line_length+20)
    t.end_fill()
    t.penup()
    t.goto(x+155, y+80)
    t.pendown()
    t.setheading(270)
    for line in text.split("\n"):
        t.write(line, font=FONT, align="left")
        t.penup()
        t.fd(12)
        t.pendown()
    t.penup()
    screen.update()


def main():
    # Testing function that won't get run,
    # feel free to modify to test your own code inside here.
    screen = Screen()
    screen.bgcolor("black")
    screen.setup(width=600, height=600)
    screen.title("Tetris")
    t = Turtle()
    screen.tracer(0)
    rgb = [['blue', 'blue', 'blue', 'cyan', 'black', 'black', 'black', 'red', 'red', 'magenta'], ['yellow', 'yellow', 'blue', 'cyan', 'black', 'black', 'red', 'red', 'magenta', 'magenta'], ['yellow', 'yellow', 'orange', 'cyan', 'black', 'black', 'black', 'lime', 'lime', 'magenta'], ['orange', 'orange', 'orange', 'cyan', 'black', 'black', 'black', 'black', 'lime', 'lime'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], [
        'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ]
    draw_grid(rgb, t, screen)
    temp_draw_next_queue("JLIOSZTSTZOLI", screen, t)
    temp_draw_hold_slot("T", True, t)
    write_text(t, screen, "woohoo\n"*randint(1, 10))
    screen.exitonclick()


if __name__ == "__main__":
    main()
