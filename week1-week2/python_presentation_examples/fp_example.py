from functools import reduce

numbers = [1, 2, 3, 4]

def double(x):
    return x * 2

def is_even(x):
    return x % 2 == 0

def add(a, b):
    return a + b


# 1. Functions are values: you can store them and pass them around
f = double
print(f(5))                         # 10

def apply_twice(func, x):
    return func(func(x))

print(apply_twice(double, 3))       # 12  (3 -> 6 -> 12)


# 2. map: do something to every item
result = []                         # the loop way
for n in numbers:
    result.append(double(n))
print(result)                       # [2, 4, 6, 8]

print(list(map(double, numbers)))   # [2, 4, 6, 8]  the functional way
# (map gives an iterator, list() collects it)


# 3. filter: keep the items that pass a test
result = []                         # the loop way
for n in numbers:
    if is_even(n):
        result.append(n)
print(result)                       # [2, 4]

print(list(filter(is_even, numbers)))  # [2, 4]  the functional way


# 4. reduce: combine everything into one value
total = 0                           # the loop way
for n in numbers:
    total = add(total, n)
print(total)                        # 10

print(reduce(add, numbers))         # 10  the functional way
# add(add(add(1, 2), 3), 4)


# 5. Putting them together: double the even numbers, then add them up
evens = filter(is_even, numbers)    # 2, 4
doubled = map(double, evens)        # 4, 8
print(reduce(add, doubled))         # 12


# 6. lambda: a small function without a name, for one-off use
print(list(map(lambda x: x * 2, numbers)))   # [2, 4, 6, 8]


# 7. Comprehensions: how Python code usually does map and filter
print([double(n) for n in numbers])          # [2, 4, 6, 8]
print([n for n in numbers if is_even(n)])    # [2, 4]


# Nothing above changed the original list
print(numbers)                      # [1, 2, 3, 4]
