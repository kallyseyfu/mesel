import turtle
def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title('Mesel Turtle Graphics')
    screen.bgcolor('white')
    screen.tracer(0)
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    t.color('blue')
    t.penup()
    t.goto(0, 0)
    t.pendown()
    try:
        for _ in range(0, 5):
            t.forward(100.0)
            t.right(144.0)
        t.penup()
        screen.update()
        screen.exitonclick()
    except turtle.Terminator:
        pass
    finally:
        try:
            screen.mainloop()
        except:
            pass

if __name__ == '__main__':
    main()