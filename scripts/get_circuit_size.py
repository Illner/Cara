# Import
import sys

# Variables
size = 0
a = 0
o = 0
l = 0

with open(sys.argv[1], "r") as file:
    for line in file.readlines():
        temp = line.split(" ")
        if line.startswith("A"):
            a += 1
            if len(temp) >= 3:
                size += int(temp[1])

        elif line.startswith("O"):
            o += 1
            if len(temp) >= 4:
                size += int(temp[2])

        elif line.startswith("L"):
            l += 1

print(f"Size: {size}")
print(f"A: {a}, O: {o}, L: {l}")
