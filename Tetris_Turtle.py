import random
from turtle import Screen, Turtle
from numpy.random import seed, randint


#Screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=300, height=600)
screen.title("Tetris")

game_on = True

#I
I = Turtle()
X = Turtle()
X1 = Turtle()
X.shape("square")
X.shapesize(stretch_wid=5, stretch_len=1)
X1.shape("square")
X1.shapesize(stretch_wid=1, stretch_len=5)
I.shape("square")
I.color("cyan")
I.shapesize(stretch_wid=5, stretch_len=1)
I.penup()
I.goto(0,250)

#O
O = Turtle()
Y = Turtle()
Y.shape("square")
Y.shapesize(stretch_wid=2, stretch_len=2)
O.shape("square")
O.color("yellow")
O.shapesize(stretch_wid=2, stretch_len=2)
O.penup()
O.goto(0,250)

shapes = [I, O]
random_shape = random.choice(shapes)

#up key
def turn(object):
    if object.shapesize() == X.shapesize():
        object.shapesize(stretch_wid=1, stretch_len=5)
    elif object.shapesize() == X1.shapesize():
        object.shapesize(stretch_wid=5, stretch_len=2)
    elif object.shapesize() == Y.shapesize():
        object.shapesize(stretch_wid=2, stretch_len=2)


if game_on == True:
    screen.listen()
    screen.onkey(turn(random_shape), "Up")

screen.exitonclick()