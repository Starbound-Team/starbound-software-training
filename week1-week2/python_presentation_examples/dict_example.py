# A dict maps keys to values (a hash table built into the language)
ages = {"alice": 30, "bob": 25}

print(ages["alice"])            # 30
ages["carol"] = 41              # add a new key
ages["bob"] = 26                # overwrite an existing one
print(ages)                     # {'alice': 30, 'bob': 26, 'carol': 41}

print("bob" in ages)            # True
print("dave" in ages)           # False

try:
    print(ages["dave"])         # missing key -> KeyError
except KeyError as e:
    print("KeyError:", e)

print(ages.get("dave"))         # None, no error
print(ages.get("dave", 0))      # 0, your own default


# Looping: .items() gives (key, value) tuples, so we can unpack them
for name, age in ages.items():
    print(name, "is", age)


# Counting things: no need to know the keys up front
counts = {}
for letter in "banana":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)                   # {'b': 1, 'a': 3, 'n': 2}


# Keys must be immutable: tuples work, lists don't
grid = {}
grid[(0, 0)] = "start"
grid[(-3, 7)] = "rock"          # negative coordinates are fine, unlike a C array
print(grid[(-3, 7)])            # rock

try:
    grid[[1, 2]] = "nope"
except TypeError as e:
    print("TypeError:", e)
