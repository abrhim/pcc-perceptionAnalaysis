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
    columns = df.columns[1:]
    for col in columns:
        columnName = "MovingAvg-"+col[6:8] if len(col) == 8 else "MovingAvg-"+col[6]
        colAvgs = df[col].rolling(10,min_periods=0).mean()
        avgData[col] = colAvgs
    avgDataAvgs = []
    for index,row in avgData.iterrows():
        avgDataAvgs.append(row.mean())
    return pd.Series(avgDataAvgs)

def splitIslands(df, times):
    average = getAvgs(removeErrorProneCols(cleanUpErrors(changeIndexToDateTime(df))))
    #print(average)
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
    df2.index=pd.to_datetime(df2.index,unit='s')
    return df2


#process/clean raw data
for i in range(len(sessions)):
    sessions[i] = splitIslands(sessions[i],times[i])
#build a df of just aotearoa from all sessions.



#make a list of dataframes, each frame for each scene
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



#edit island data
for i in range(len(islandDfs)):
    island = islandDfs[i]
    #make the dataframe only as long as the longest session
    islandCount = island.count()
    longestSession = 0
    for j in range(len(islandCount)):
        if islandCount[j] > longestSession:
            longestSession = islandCount[j]

    island = island.drop(island.index[longestSession:])
    #print("after: ", island.index)
    #resample the data 

    #give the dataframe a name   
    island.name = times[0].iloc[i+1]['island']
    #print(type(island.name))
    islandDfs[i] = island

for island in islandDfs:


    print(island.name, ":\n",island)