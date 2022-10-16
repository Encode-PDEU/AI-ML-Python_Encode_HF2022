from turtle import Turtle,Screen

screen = Screen()
Y = [(0,0),(-20,0),(-40,0)]
UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180

class Snake:

    def __init__(self):
        self.snakes = []
        self.create_snake()
        self.head = self.snakes[0]
        
    def add_tail(self, position):
        snake = Turtle(shape="square")
        snake.penup()
        snake.color("white")
        snake.goto(position)
        self.snakes.append(snake)

    def create_snake(self):
        for i in range(3):
            self.add_tail(Y[i])

    def entend(self):
        pos = self.snakes[-1].position()
        self.add_tail(pos)
    
    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def moveforward(self):
        for snake in range(len(self.snakes)-1, 0, -1):
            x = self.snakes[snake - 1].xcor()
            y = self.snakes[snake - 1].ycor()
            self.snakes[snake].goto(x,y)
        self.head.forward(20)

    def listen(self):
        screen.listen()
        screen.onkey(self.up,"Up")
        screen.onkey(self.down,"Down")
        screen.onkey(self.right,"Right")
        screen.onkey(self.left,"Left")
    
    def mov(self):
        self.moveforward()
        self.listen()

    def collison(self):
        
        return False