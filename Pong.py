import turtle


def create_turtle():
    t = turtle.Turtle()
    t.speed(0)
    t.color("white")
    t.penup()
    return t


def create_turtle_at(x, y):
    t = create_turtle()
    t.goto(x, y)
    t.shape("square")
    return t


def create_paddle(x, y):
    p = create_turtle_at(x, y)
    p.shapesize(stretch_wid=5, stretch_len=1)
    return p


def collision(x1, x2, b, p):
    return (x1 < b.xcor() < x2) and (p.ycor() + 40 > b.ycor() > p.ycor() - 40)


def scoreboard(p, s1, s2):
    p.clear()
    p.write("Player A: {} Player B: {}".format(s1, s2), align="center", font=("Courier", 24, "normal"))


window = turtle.Screen()
window.title("Pong Game")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Global
y_max = 290
y_min = -290
x_max = 390
x_min = -390

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = create_paddle(x_min + 30, 0)

# Paddle B
paddle_b = create_paddle(x_max - 40, 0)

# Ball
ball = create_turtle_at(0, 0)
ball.dx = 2
ball.dy = 2

# Pen
pen = create_turtle()
pen.hideturtle()
pen.goto(0, y_max - 30)
scoreboard(pen, 0, 0)


# Movement
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# Keyboard Binding
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")

# Main
while True:
    window.update()

    # Move Ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border Checking
    if ball.ycor() > y_max:
        ball.sety(y_max)
        ball.dy *= -1

    if ball.ycor() < y_min:
        ball.sety(y_min)
        ball.dy *= -1

    if ball.xcor() > x_max:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        scoreboard(pen, score_a, score_b)

    if ball.xcor() < x_min:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        scoreboard(pen, score_a, score_b)

    # Paddle and Ball Collisions
    if collision(x_max - 50, x_max - 40, ball, paddle_b):
        ball.setx(x_max - 50)
        ball.dx *= -1

    if collision(x_min + 40, x_min + 50, ball, paddle_a):
        ball.setx(x_min + 50)
        ball.dx *= -1
