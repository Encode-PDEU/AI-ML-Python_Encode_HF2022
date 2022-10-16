import time
from turtle import Screen
from scoreboard import Scoreboard
from snake import Snake
from food import Food
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width = 600, height = 600)
screen.bgcolor("black")
screen.title("Snake game")
screen.tracer(0)

snake = Snake()
food = Food()
score = Scoreboard()

screen.update()
is_on = True

while is_on:
    screen.update()
    time.sleep(0.1)
    snake.mov()

    if snake.head.distance(food) < 15:
        food.refresh()
        snake.entend()
        score.increase_score()
        
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 260 or snake.head.ycor() < -280:
        is_on = False
        score.game_over()

    for seg in snake.snakes[1:]:
        # if seg == snake.head:
        #     pass
        if snake.head.distance(seg) < 10:
            is_on = False
            score.game_over()        
screen.exitonclick()       