a = 3

if a == 2:
    print(10 / 0)                 # crashes: the program stops here
if a == 3:
    try:
        print(10 / 0)
    except ZeroDivisionError:
        print("can't divide by zero, carrying on")

print("end of program")           # only reached if nothing crashed
