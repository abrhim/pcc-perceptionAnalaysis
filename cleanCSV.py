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

print(data)
for col in data:
    print(col)
    if col == "time": 
        continue
    else:
        data.loc[data[col] < 20, col] = numpy.NaN
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

#Step 3.5: get the number of non-NaN values for each column as a series. 
print("\n#Step 3.5: get the number of non-NaN values for each column as a series.")
nValues = data.drop(columns = "time").count().rename("N")
print(nValues)

#Step 3.7: Get average for each column and save it as a Series.
print("\n#Step 3.7: Get average for each column and save it as a Series.")
dialAvgs = data.mean()[1:]
dialAvgs = dialAvgs.rename("dialAvgs")
print(dialAvgs)

#Step 4: for each dial create an average without it
print("\n#Step 4: for each dial create an average without it")
newIndices= dict(enumerate(data.index))
columns = data.columns[1:]
lastColumnIndex = len(columns)
for col in columns:
    columnName = "Avg-"+col[6:8] if len(col) == 8 else "Avg-"+col[6]
    myList = []
    tempData = data.drop(columns=col)
    for index, row in tempData.iterrows():
        tempRow = row[1:lastColumnIndex]
        mean = tempRow.mean()
        myList.append(mean)
    myCol = pd.Series(myList).rename(index= newIndices)
    data[columnName] = myCol

print(data)

#Step 4.1 check why the NaN's are popping up
print("\n#Step 4.1 check why the NaN's are popping up\nUncomment data.to_csv to save the dataFrame")
#data.to_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/day2CHECK.csv")

#Step 4.9 for each average, find the standard deviation
print("\n#Step 4.9 for each average and dial, find the standard deviation")

dataStd = data.drop(columns="time").std()
dialStd = dataStd[:int(len(dataStd)/2)].rename("dialStd")
avgStd = dataStd[int(len(dataStd)/2):].rename("avgStd")
indexDict = dict(zip(avgStd.index.tolist(),dialStd.index.tolist()))
avgStd = avgStd.rename(indexDict)
print(indexDict)
print(dialStd)
print(avgStd)

#Step 5: correlate the data with it's avg-self
print("\n #Step 5: correlate the data with it's avg-self")
#corrData = pd.read_csv("/Users/Abram/Desktop/my.csv")
corrData=data.corr()
print(corrData)

#Step 6: Traverse the Correlated Data and grab only the R values between the dial and it's average
print("\n#Step 6: Traverse the Correlated Data and grab only the R values between the dial and it's average")
rowLabels = corrData.index
myList = []
for i in range(len(rowLabels)):
    if i > lastColumnIndex: break
    else: 
        if i == 0: continue
        myList.append(corrData.iloc[i,i+lastColumnIndex])
indexLabels = corrData.index[1:len(myList)+1]
rValues = pd.Series(myList, index = indexLabels).rename("r")
print(rValues)

#Step 7: put the Stds, N's, and r's all into a single table.
print("\n#Step 7: put the Stds, N's, and R's all into a single table.")

result = pd.concat([rValues, nValues, dialStd, dialAvgs, avgStd], sort = False, axis = 1)

print(result)

result.to_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/day1table.csv")