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
             }
def draw_square(width, color, t):
  global color_dict
  if type(color) == tuple:
    color = color_dict[color]
  if color == "black":
    return None
  t.fillcolor(color)
  t.begin_fill()
  for i in range(4):
    t.forward(width)
    t.right(90)
  t.end_fill()

def draw_grid(rgb, t, screen):
  t.hideturtle()
  t.clear()
  t.pencolor("black")
  startX = -100
  startY = -200
  t.speed(0)
  t.goto(startX, startY)
  t.pendown()
  t.setheading(0)
  for i in range(20):
    t.goto(startX, startY+((i+1)*20))
    for j in range(10):
      draw_square(20, rgb[i][j], t)
      t.forward(20)
  t.pencolor("white")
  t.penup()
  t.goto(startX, startY)
  t.pendown()
  t.forward(200)
  t.left(90)
  t.forward(400)
  t.left(90)
  t.forward(200)
  t.left(90)
  t.forward(400)
  t.penup()
  screen.update()

def main():
  screen = Screen()
  screen.bgcolor("black")
  screen.setup(width=300, height=600)
  screen.title("Tetris")
  t = Turtle()
  screen.tracer(0) 
  rgb = [['blue', 'blue', 'blue', 'cyan', 'black', 'black', 'black', 'red', 'red', 'magenta'], ['yellow', 'yellow', 'blue', 'cyan', 'black', 'black', 'red', 'red', 'magenta', 'magenta'], ['yellow', 'yellow', 'orange', 'cyan', 'black', 'black', 'black', 'lime', 'lime', 'magenta'], ['orange', 'orange', 'orange', 'cyan', 'black', 'black', 'black', 'black', 'lime', 'lime'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black'], ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']]

  draw_grid(rgb, t, screen)
  draw_grid(rgb, t, screen)

  #screen.tracer(0)
  screen.mainloop()

if __name__ == "__main__":
  main()