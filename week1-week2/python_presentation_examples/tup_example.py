def calculate(a):
    b = a + 1
    c = range(1,10)
    print(c)
    return b, c[0], c[1], "Hello"

r1, r2, r3, r4 = calculate(5)
print(r1, r2, r3, r4)

r1, r2, *r3 = calculate(5)
print(r1, r2, r3)

first, _, _, last = calculate(5)
print(first, last)

head, *_ = calculate(5)
print(head)
