# Python's `and` returns one of its operands, not True/False
print(3 and 5)        # 5      (3 is truthy, so it gives back the second one)
print(0 and 5)        # 0      (0 is falsy, so it stops and gives back 0)
print(repr("" and "hi"))  # ''  (empty string is falsy)
print([1] and "hi")   # hi

if(3 and 5):
    print("conditions still work")

# It only looks boolean when the operands are booleans
print(True and False)  # False
print(bool(3 and 5))   # True  (convert explicitly if you want a bool)


# Short-circuit: if the left side is falsy, the right side never runs
def check(name, value):
    print("  evaluating", name)
    return value

print(check("left", 0) and check("right", 5))   # only "left" runs, result 0
print(check("left", 3) and check("right", 5))   # both run, result 5

# Common use: guard before touching something that might not exist
items = []
print(items and items[0])   # [] -- items[0] never runs, so no IndexError


# `or` is the mirror image: it stops at the first TRUTHY value
print(3 or 5)              # 3   (3 is truthy, so it stops right away)
print(0 or 5)              # 5   (0 is falsy, so it moves on)
print(repr(0 or ""))       # ''  (nothing truthy, so you get the last one)
print(0 or "" or 7 or 9)   # 7   (first truthy one wins; 9 is never looked at)

print(check("left", 3) or check("right", 5))    # only "left" runs, result 3
print(check("left", 0) or check("right", 5))    # both run, result 5

# Common use: a default value
user_input = ""
name = user_input or "anonymous"
print(name)                # anonymous

# Careful: 0 is a perfectly good number, but it is falsy too
n = 0
print(n or 10)             # 10, not 0!
