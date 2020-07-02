s1 = input()
s2 = input()

s1Length = len(s1)
count = 0

for i in range(s1Length):
    for index in range(s1Length - 1):
        if s1[i:i + index] in s2:
            if s2.find(s1[i:i + index]) != i:
                count += 1

print(count, end='')