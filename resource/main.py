questNum = int(input())

for quest in range(questNum):
    n = int(input())
    start = 4

    i = 0
    ans = 0
    while i < n:
        startStr = str(start)
        if startStr.count('7') + startStr.count('4') == len(startStr):
            i += 1
            ans = start
        start += 1

    print(ans)