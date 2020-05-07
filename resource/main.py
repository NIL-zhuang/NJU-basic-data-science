info0=input().split(',')
info=[int(y) for y in info0]
a=[]
b=[]
while len(info)!=0:
    a.append(max(info[0],info[-1]))
    info.remove(max(info[0],info[-1]))
    #print(a)
    #print(info)
    b.append(max(info[0], info[-1]))
    info.remove(max(info[0], info[-1]))
    #print(b)
    #print(info)
if sum(a)>sum(b):
    print(True)
else:
    print(False)