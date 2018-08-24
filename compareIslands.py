import pandas as pd
import numpy
import sys
import matplotlib.pyplot as plt



sessionOne = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day1.csv").drop(columns="29")
timeOne = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time1.csv")
sessionOne.name = 'sessionOne'

sessionTwo = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day2.csv").drop(columns="29")
timeTwo = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time2.csv")
sessionTwo.name = 'sessionTwo'

sessionThree = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day3.csv").drop(columns="29")
timeThree = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time3.csv")
sessionThree.name = 'sessionThree'

sessionFour = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day4.csv").drop(columns="29")
sessionFour.name = 'sessionFour'
timeFour = pd.read_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time4.csv")

sessions = [sessionOne,sessionTwo,sessionThree,sessionFour]
times = [timeOne,timeTwo,timeThree,timeFour]

def changeIndexToDateTime(df):
    df.index=pd.to_datetime(df.time,unit='s')
    return df

def cleanUpErrors(df):
    for col in df:
        if col == "time": 
            continue
        else:
            df.loc[df[col] < 20, col] = numpy.NaN
            df.loc[df[col] > 100, col] = numpy.NaN
    return df

def removeErrorProneCols(df):
    percentValid = df.count()/len(df.index)*100
    for col in df:
        #print(col,": ",percentValid[col])
        if percentValid[col] < 70.0:
            df = df.drop(columns=col)
    #print(df.columns)
    return df

def getAvgs(df):
    avgData = pd.DataFrame()
    colList = list(df.columns)
    if 'time' in colList: 
        df = df.drop(columns='time')
    columns = df.columns
    for col in columns:
        columnName = "MovingAvg-"+col[6:8] if len(col) == 8 else "MovingAvg-"+col[6]
        colAvgs = df[col].rolling(10,min_periods=0).mean()
        avgData[col] = colAvgs
    avgDataAvgs = []
    for index,row in avgData.iterrows():
        avgDataAvgs.append(row.mean())
    return pd.Series(avgDataAvgs)

def splitIslands(df, times):
    average = getAvgs(removeErrorProneCols(cleanUpErrors(df)))
    listOfIslands = []
    longestIsland = 0
    for index in times.index:
        if numpy.isnan(times.iloc[index]['start']) or numpy.isnan(times.iloc[index]['end']):
            print("Missing data - skipping %s."%(times.iloc[index]['island']))
            continue
        island = average[int(times.iloc[index]['start']):int(times.iloc[index]['end'])]
        newIndices = dict(zip(list(island.index), list(range(len(island.index)))))
        tempSeries = average[int(times.iloc[index]['start']):int(times.iloc[index]['end'])].rename(index=newIndices)
        tempSeries = tempSeries.rename(times.iloc[index]['island'])
        if len(tempSeries) > longestIsland:
            longestIsland = len(tempSeries)
        listOfIslands.append(tempSeries)
    df2 = pd.DataFrame(index=range(longestIsland))
    for island in listOfIslands:
        df2[island.name] = island
    return df2


#make a list of dataframes, each frame for each scene
def islandDataframe(sessions,times):
    islandDfs = []
    for index in times[0].index:
        if index == 0: continue
        islandName = times[0].iloc[index]['island']
        islandSeries = []
        indexLength = 0
        indexSeries = pd.Series()
        for i in range(len(sessions)):
            tempSeries = pd.Series(sessions[i][islandName])
            islandSeries.append(tempSeries)    
            if indexLength < len(tempSeries):
                indexLength = len(tempSeries)
                indexSeries = tempSeries
        islandDf = pd.DataFrame(index=tempSeries.index)
        for i in range(len(islandSeries)):
            islandDf["rainbow%s"%(i+1)] = islandSeries[i]
        islandDfs.append(islandDf)
    return islandDfs


def compressColumns(df):
    #establish shortest column and grab its name
    shortestCol = 100000
    shortestColName = ""
    for col in df.columns:
        if df[col].count() < shortestCol: 
            shortestCol = df[col].count()
            shortestColName = col


    #remove values and avg their neighbors against it to preserve movement. 
    for col in df.columns:
        diff = df[col].count()-shortestCol
        if diff != 0:

            #generate a list to get the incrementing values
            nthF = df[col].count()/diff
            nth = int(nthF)
            colSeries = df[col]
            nthCounter = 0
            nthList = []
            
            #calculate avgs and delete rows
            for i in range(len(colSeries)):

                #count according to the incrementor, and round down. Add it to the List
                #  - if i is in List, then perform our functions on it.
                nthCounter += nthF
                nthList.append(round(nthCounter))
                if i in nthList and i < len(df[shortestColName]):
                    if i != 0 and i != len(df[shortestColName])-1:
                        avgLower = (colSeries[i]+colSeries[i-1])/2
                        avgUpper =(colSeries[i]+colSeries[i+1])/2
                        colSeries.loc[i-1]= avgLower
                        colSeries.loc[i+1] = avgUpper
                        colSeries = colSeries.drop(index=i)
                    elif i == 0:
                        avg=(colSeries[i]+colSeries[i+1])/2
                        colSeries.loc[i+1] = avg
                        colSeries = colSeries.drop(index=i)
                    else:
                        avg=(colSeries[i]+colSeries[i-1])/2
                        colSeries.loc[i-1]= avg
                        colSeries = colSeries.drop(index=i)
            if abs(colSeries.count() - df[shortestColName].count()) == 1:
                lastIndex = colSeries.last_valid_index()
                avg = (colSeries.loc[lastIndex-1] + colSeries.loc[lastIndex])/2
                colSeries.loc[lastIndex-1] = avg
                colSeries = colSeries.drop(index=lastIndex)

            #reindex the column giving it the effect as if we removed the values and smashed it to match the shortest column
            oldIndex = list(colSeries.index)
            newIndex = list(df[shortestColName].index)
            indexDict = dict(zip(oldIndex,newIndex))

            #print(colSeries.count())
            colSeries = colSeries.rename(index=indexDict)
            df[col] = colSeries
    return df


def resizeIslandFrames(islandDfs):
    for i in range(len(islandDfs)):
        #print(islandDfs[i])
        islandDfs[i].name = times[0].iloc[i+1]['island']
        islandDfs[i] = compressColumns(islandDfs[i])
        #print(islandDfs[i])

    return islandDfs

#process/clean raw data
for i in range(len(sessions)):
    sessions[i] = splitIslands(sessions[i],times[i])
islandDfs = islandDataframe(sessions,times)
for island in islandDfs:
    island.plot()

islandDfs = resizeIslandFrames(islandDfs)
for island in islandDfs:
    print(island.name)
    island.to_csv("/Users/abram/Documents/PCC/perceptionAnalyzer/islandData/%s.csv"%(island.name))

    
