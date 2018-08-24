nth = 4.578125
nthCounter = 0
nthListF = []
nthList = []
for i in range(204):
    nthListF.append(nthCounter)
    nthList.append(int(nthCounter))
    nthCounter += nth
print(nthList)
print("\n")
print(nthListF)
nth = 4
nthCounter = 0
for i in range(204):
    if  i in nthList: print(i)
