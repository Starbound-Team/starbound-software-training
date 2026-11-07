# An iterable is something you can loop over (a list, a string, ...)
# An iterator is a bookmark into it: it remembers where you are
# and hands you the next item when asked

numbers = [10, 20, 30]          # iterable

it = iter(numbers)              # ask the list for a bookmark
print(next(it))                 # 10
print(next(it))                 # 20
print(next(it))                 # 30

try:
    next(it)                    # nothing left
except StopIteration:
    print("StopIteration: the bookmark is at the end")


# This is exactly what a for loop does for you:
#     for x in numbers:
#         print(x)
it = iter(numbers)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x, end=" ")           # 10 20 30
print()


# A list can be looped over many times: every loop gets a fresh bookmark
print(list(numbers))            # [10, 20, 30]
print(list(numbers))            # [10, 20, 30]

# An iterator can't: there is only one bookmark, and it stays at the end
it = iter(numbers)
print(list(it))                 # [10, 20, 30]
print(list(it))                 # []

# zip and enumerate give you iterators, so the same thing happens to them
pairs = zip("ab", [1, 2])
print(list(pairs))              # [('a', 1), ('b', 2)]
print(list(pairs))              # []

# A list is not a bookmark itself, so next() on it fails
try:
    next(numbers)
except TypeError as e:
    print("TypeError:", e)
