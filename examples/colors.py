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
        t.color('red')
        t.width(5.0)
        t.forward(100.0)
        t.right(90.0)
        t.color('green')
        t.width(3.0)
        t.forward(100.0)
        t.right(90.0)
        t.color('blue')
        t.width(2.0)
        t.forward(100.0)
        t.right(90.0)
        t.color('yellow')
        t.width(1.0)
        t.forward(100.0)
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