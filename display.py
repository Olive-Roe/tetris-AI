from turtle import Screen, Turtle
import random

color_dict = {(0,0,0): "black",
              (0,0,255): "blue",
              (0,255,255): "cyan",
              (255,0,255): "magenta",
              (255,165,0): "orange",
              (255,255,0): "yellow",
              (255,0,0): "red",
              (0,255,0): "lime",
              (128,128,128): "gray",
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
  for i in range(4):
    t.forward(width)
    t.right(90)
  # FIll the square
  t.end_fill()

def draw_grid(rgb, t, screen):
  '''Draws a grid, given a dictionary of colors and coordinates 
  'rgb', and provided the turtle 't' and screen 'screen'. '''
  # Hide the turtle
  t.hideturtle()
  # Clear the current board
  t.clear()
  # Set the pencolor to black (black outline of squares)
  t.pencolor("black")
  startX = -100
  startY = -200
  # Make turtle fastest (doesn't matter with screen update)
  t.speed(0)
  # Go to the set starting location
  t.goto(startX, startY)
  t.pendown()
  # Face north
  t.setheading(0)
  #FIXME: Changed height to 40, hopefully doesn't break things
  for i in range(40):
    t.goto(startX, startY+((i+1)*20))
    for j in range(10):
      draw_square(20, rgb[i][j], t)
      t.forward(20)
  # Draws outline (200x400 rectangle)
  t.pencolor("white")
  t.penup()
  t.goto(startX, startY)
  t.pendown()
  for x in range(2):
    t.forward(200)
    t.left(90)
    t.forward(400)
    t.left(90)
  t.penup()
  # Updates the screen when it is done
  screen.update()

def draw_hold_slot(piece:str, locked:bool):
  #TODO: Make hold slot
  pass

def draw_next_queue(bag_notation:str, n_of_previews:int):
  #TODO: Make next queue
  pass

def main():
  # Testing function that won't get run,
  # feel free to modify to test your own code inside here.
  screen = Screen()
  screen.bgcolor("black")
  screen.setup(width=600, height=600)
  screen.title("Tetris")
  t = Turtle()
  screen.tracer(0)
  rgb = [['blue', 'blue', 'blue', 'cyan', 'black', 'black', 'black', 'red', 'red', 'magenta'], ['yellow', 'yellow', 'blue', 'cyan', 'black', 'black', 'red', 'red', 'magenta', 'magenta'], ['yellow', 'yellow', 'orange', 'cyan', 'black', 'black', 'black', 'lime', 'lime', 'magenta'], ['orange', 'orange', 'orange', 'cyan', 'black', 'black', 'black', 'black', 'lime', 'lime'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'],]

  draw_grid(rgb, t, screen)
  draw_grid(rgb, t, screen)

  screen.mainloop()

if __name__ == "__main__":
  main()