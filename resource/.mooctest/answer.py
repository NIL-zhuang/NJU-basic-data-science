import math
for t in range(int(input())):
    i = 2
    n = int(input()) - 1
    size = 1
    while n > i-1:
        n -= i
        i *= 2
        size += 1
    b = bin(n)[2:]
    fours = (size-len(b))*"4"
    print(fours + b.replace("1","7").replace("0","4"))