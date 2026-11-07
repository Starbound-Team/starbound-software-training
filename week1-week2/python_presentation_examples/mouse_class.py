# The same mouse as mouse.c, written as a class
class Mouse:
    a = 3
    def __init__(self, x=0, y=0):       # runs on Mouse(...), fills in the fields
        self.x = x                  # self is like the Mouse *self pointer in C
        self.y = y
        self.clicks = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def click(self):
        self.clicks += 1
        print("click at", self.x, self.y)

    def __str__(self):              # what print() shows for a Mouse
        return f"Mouse at ({self.x}, {self.y}), {self.clicks} clicks"


a = Mouse(0, 0)
b = Mouse(0, 0)
c = Mouse()

a.move(5, 3)
a.click()                           # click at 5 3
b.click()                           # click at 0 0  (b has its own data)
print(a)                            # Mouse at (5, 3), 1 clicks
print(b)                            # Mouse at (0, 0), 1 clicks

# a.click() is short for this, just like a.append(4) and list.append(a, 4)
Mouse.click(a)                      # click at 5 3


# Inheritance: a gaming mouse is a mouse with extra buttons
class GamingMouse(Mouse):
    def __init__(self, x, y, side_buttons):
        super().__init__(x, y)      # set up the regular mouse part first
        self.side_buttons = side_buttons

    def press_side(self, n):        # the extension: only gaming mice have this
        print("side button", n, "of", self.side_buttons)

    def click(self):                # override: replaces Mouse's click for gaming mice
        super().click()             # do the normal click first
        print("  RGB flash!")       # then the extra part


g = GamingMouse(0, 0, 4)
g.move(1, 1)                        # inherited from Mouse, not rewritten
g.click()                           # click at 1 1, then RGB flash! (overridden)
g.press_side(2)                     # side button 2 of 4
print(g)                            # Mouse at (1, 1), 1 clicks  (Mouse's __str__)
print(isinstance(g, Mouse))         # True: a gaming mouse is still a mouse

try:
    a.press_side(2)                 # a plain mouse has no side buttons
except AttributeError as e:
    print("AttributeError:", e)

