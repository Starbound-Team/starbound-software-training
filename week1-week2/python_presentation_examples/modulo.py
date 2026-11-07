import math

# Python: % takes the sign of the divisor (right side)
print(7 % 3)     # 1
print(-7 % 3)    # 2
print(7 % -3)    # -2

# Why? // rounds DOWN (toward -infinity), and % is whatever is left over
print(-7 // 3)              # -3
print(-7 // 3 * 3 + -7 % 3)  # -9 + 2 = -7, back where we started

# C rounds toward zero instead, so -7 / 3 is -2 and -7 % 3 is -1
# math.fmod gives the C behaviour: sign of the dividend (left side)
print(math.fmod(-7, 3))   # -1.0
print(int(-7 / 3))        # -2

# Where it matters: walking backwards around a ring of 5 slots
ring = ["A", "B", "C", "D", "E"]
pos = 0
for step in range(3):
    pos = (pos - 1) % len(ring)  # in C this goes negative; in Python it wraps
    print(pos, ring[pos])        # 4 E, 3 D, 2 C
