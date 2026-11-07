# A for loop works on anything iterable, not just lists

for x in [1, 2, 3]:             # list
    print(x, end=" ")           # 1 2 3
print()

for x in (1, 2, 3):             # tuple
    print(x, end=" ")           # 1 2 3
print()

for ch in "hey":                # string: one character at a time
    print(ch, end=" ")          # h e y
print()

for i in range(3):              # range: the C-style counting loop
    print(i, end=" ")           # 0 1 2
print()

ages = {"alice": 30, "bob": 25}
for name in ages:               # dict: gives the keys
    print(name, end=" ")        # alice bob
print()

for name, age in ages.items():  # dict items: (key, value) pairs, unpacked
    print(name, age, end=" | ") # alice 30 | bob 25 |
print()

for i, ch in enumerate("hey"):  # enumerate: index and item together
    print(f"{ch} is at pos {i}")     # 0 h | 1 e | 2 y |
print()

names = ["alice", "bob"]
scores = [90, 85]
for name, score in zip(names, scores):  # zip: two sequences side by side
    print(name, score, end=" | ")       # alice 90 | bob 85 |
print()

for x, y in [(0, 0), (3, 4)]:   # any list of pairs can be unpacked
    print(x, y, end=" | ")      # 0 0 | 3 4 |
print()

with open("for_types.py") as f:
    for line in f:              # file: one line at a time
        print(line, end="")     # # A for loop works on anything iterable, ...
        break                   # just the first line
