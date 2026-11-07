# The same steps done two ways

# Object way: the list carries its own functions, reached with a dot
a = [3, 1, 2]
a.append(0)
a.sort()
print(a, a.count(1))            # [0, 1, 2, 3] 1

# Non-object way: plain functions, and you pass the list in yourself
# (like C: list_append(b, 0))
b = [3, 1, 2]
list.append(b, 0)
list.sort(b)
print(b, list.count(b, 1))      # [0, 1, 2, 3] 1

print(a == b)                   # True, same result

# a.append(0) is just shorthand: Python finds append in type(a), which is list,
# and calls it with a as the first argument
print(type(a))                  # <class 'list'>
