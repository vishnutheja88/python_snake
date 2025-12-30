import turtle
import random

WIDTH, HEIGHT = 800, 800
STEP = 20
UPDATE_MS = 100
START_LEN = 3

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game - Turtle")
screen.bgcolor("white")
screen.tracer(0)

def make_segment(color="green"):
    seg = turtle.Turtle("square")
    seg.penup()
    seg.speed(0)
    seg.color(color)
    return seg

segments = []
for i in range(START_LEN):
    s = make_segment()
    s.goto(-i * STEP, 0)
    segments.append(s)
head = segments[0]
direction = "right"
# ----- food color-----
food = make_segment("red")
food.shapesize(0.9, 0.9)

#------score display -------
score = 0
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.goto(0, HEIGHT//2 - 40)
score_pen.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

#------ controls ------

def go_up():
    global direction
    if direction != "down":
        direction = "up"
def go_down():
    global direction
    if direction != "up":
        direction = "down"
def go_left():
    global direction
    if direction != "right":
        direction = "left"
def go_right():
    global direction
    if direction != "left":
        direction = "right"
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

#---- movement / update logic -----
game_over = False
def place_food():
    max_x = (WIDTH//2 - 40)//STEP
    max_y = (HEIGHT//2 - 40)//STEP
    while True:
        x = random.randint(-max_x, max_x) * STEP
        y = random.randint(-max_y, max_y) * STEP
        # avoid placing on the snake
        if not any(seg.distance(x, y) < STEP for seg in segments):
            food.goto(x, y)
            break

def reset_game():
    global segments, head, direction, score, game_over
    for seg in segments:
        seg.goto(1000, 1000)
    segments = []
    for rg in range(START_LEN):
        seg = make_segment()
        seg.goto(-rg * STEP, 0)
        segments.append(s)
    head = segments[0]
    direction = "right"
    score = 0
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))
    place_food()
    game_over = False
    screen.ontimer(game_loop, UPDATE_MS)

def move_snake():
    for ms in range(len(segments) - 1, 0, -1):
        x = segments[ms - 1].xcor()
        y = segments[ms - 1].ycor()
        segments[ms].goto(x,y)

    x, y = head.xcor(), head.ycor()
    if direction == "up":
        head.goto(x, y + STEP)
    elif direction == "down":
        head.goto(x, y - STEP)
    elif direction == "left":
        head.goto(x - STEP, y)
    elif direction == "right":
        head.goto(x + STEP, y)

def grow():
    tail = segments[-1]
    new_seg = make_segment()
    new_seg.goto(tail.xcor(), tail.ycor())
    segments.append(new_seg)

def check_collisions():
    global game_over, score
    hx, hy = head.xcor(), head.ycor()
    half_w, half_h = WIDTH // 2 - STEP, HEIGHT // 2 - STEP
    if hx < -half_w or hx > half_w or hy < -half_h or hy > half_h:
        game_over = True
        return
    if head.distance(food) < STEP:
        score += 1
        score_pen.clear()
        score_pen.write(f"score: {score}", align="center", font=("Arial", 16, "normal"))
        grow()
        place_food()
    for seg in segments[1:]:
        if head.distance(seg) < STEP:
            game_over = True
            return

def show_game_over():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.goto(0, 0)
    pen.write("GAME OVER \n Press SPACE to restart", align="center", font=("Arial", 30, "bold"))

    def restart():
        pen.clear()
        reset_game()
    screen.onkey(restart, "space")
    screen.listen()

def game_loop():
    if not game_over:
        move_snake()
        check_collisions()
        screen.update()
        screen.ontimer(game_loop, UPDATE_MS)
    else:
        show_game_over()

place_food()
screen.ontimer(game_loop, UPDATE_MS)
screen.mainloop()