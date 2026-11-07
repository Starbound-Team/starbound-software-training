# Lists are mutable: you can change the object itself
a = [1, 2, 3]
b = a                    # both names point at the same list
print(id(a) == id(b))    # True

b += [4]                 # changes the list in place
print(a)                 # [1, 2, 3, 4]  -- a sees the change
print(id(a) == id(b))    # True, still the same object


# Strings are immutable: you can't change them, only make new ones
s = "hello"
t = s                    # both names point at the same string
print(id(s) == id(t))    # True

t += " world"            # builds a NEW string and points t at it
print(s)                 # hello  -- s is untouched
print(id(s) == id(t))    # False, t now points somewhere else
print(s, t)

try:
    s[0] = "j"           # fine for a list, not allowed for a string
except TypeError as e:
    print("TypeError:", e)


# Same thing when passing to a function
def add_item(things):
    things += ["new"]

def add_text(text):
    text += " new"

my_list = ["old"]
add_item(my_list)
print(my_list)           # ['old', 'new']  -- the caller's list changed

my_text = "old"
add_text(my_text)
print(my_text)           # old  -- the caller's string did not
