import turtle

def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.title('Test Turtle Graphics')
    screen.bgcolor('white')
    
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    t.color('blue')
    
    # Draw a simple square
    for _ in range(4):
        t.forward(100)
        t.right(90)
    
    screen.mainloop()

if __name__ == '__main__':
    main() 