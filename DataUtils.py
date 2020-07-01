def getAVG(list):
    a = sum(list)
    return a / len(list)


def getVAR(list):
    avg = getAVG(list)
    sum = 0
    for i in list:
        sum += (i - avg) * (i - avg)
    return sum / len(list)


def omega(x, avg, var):
    if var == 0:
        return 1
    temp = (x - avg) / var
    if temp > 1.29:
        temp = 1.129
    elif temp < -1.29:
        temp = 0.871
    else:
        temp = 1 + temp / 10
    return temp
    # print(temp)


l = [1, 2, 3, 4, 5, 6]
pj = getAVG(l)
fc = getVAR(l)
for i in l:
    omega(i, pj, fc)
