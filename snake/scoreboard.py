from turtle import Turtle, color

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.current_score = 0
        self.goto(0,270)
        self.color("white")
        self.write(f"Score: {self.current_score}", align="center", font=("Arial",22,"normal"))   
        self.hideturtle() 
        
    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", align="center", font=("Arial",22,"normal"))   
    def increase_score(self):
        self.current_score += 1
        self.clear()
        self.write(f"Score: {self.current_score}", align="center", font=("Arial",22,"normal")) 