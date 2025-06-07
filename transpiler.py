# In your transpiler.py
def transpile_program(self, statements):
    imports = "import turtle\n"
    imports += "t = turtle.Turtle()\n\n"
    body = "\n".join([self.transpile(stmt) for stmt in statements])
    return f"{imports}{body}\nturtle.done()"  # Add turtle.done() to keep window open