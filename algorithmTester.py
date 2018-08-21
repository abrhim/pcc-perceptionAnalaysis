import pandas as pd
import numpy
import sys

#print(sys.argv[1])

dataFilePath = "/Users/Abram/Documents/PCC/perceptionAnalyzer/day1.csv"
showTimesFilepath = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sceneStartEndCCP1.csv"

def getMeanOfIsland(start,end):
    sumOfMeans=0
    rowCount=0
    island = data[start:end].mean()
    for col in island:   
        sumOfMeans+=col
        rowCount+=1
    islandMean = sumOfMeans/rowCount
    return islandMean

startEnd = pd.read_csv(showTimesFilepath)
startOfShow = startEnd.iloc[0][1]
endOfShow = startEnd.iloc[-1][-1]
data = pd.read_csv(dataFilePath)
data = data.drop(data.columns[0], axis=1)

print("end of Show: ",endOfShow)
print("endOfShow type: ", type(endOfShow) == numpy.int64)
data = data.drop(data.index[endOfShow:], axis=0)
print("start of Show: ",startOfShow)
print("startOfShow type: ", type(startOfShow) == numpy.int64)
if type(startOfShow) == numpy.int64 and startOfShow-1 > 0: 
    data = data.drop(data.index[:startOfShow], axis=0)

#Step 1: Eliminate error codes
print("\n#Step 1: Eliminate error codes")

#print(data)
for col in data:
    if col == "time": 
        continue
    else:
        data.loc[data[col] < 0, col] = numpy.NaN
        data.loc[data[col] > 100, col] = numpy.NaN

#Step 2: count number of valid rows per dial
print("\n#Step 2: count number of valid rows per dial")
percentValid = data.count()/len(data.index)*100
#print(percentValid)#can be accessed as a dictionary!

#Step 3: delete columns where > 30% of rows = NaN
print("\n#Step 3: delete columns where > 30% of rows = NaN")
print("Raw column count: %s"%(len(data.columns)))

for col in data:
    #print(percentValid[col])
    print(col,":",percentValid[col])
    if percentValid[col] < 70.0:
        data = data.drop(columns=col)

print("Filtered Columns Count: %s "%(len(data.columns)))

for col in data:
    if col == "time": continue
    colSeries = data[col]
    print("\n"+col)
    i = 0
    for value in colSeries:
        if i == 1:
            colSeries[1] = 1700
        if value < 20: print(i,": ",value)
        i+=1
        
    data[col] = colSeries

print(data)