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


def resizeIslandFrames(islandDfs):
    for i in range(len(islandDfs)):
        if i == 1: break
        island = islandDfs[i]
        #make the dataframe only as long as the longest session
        #islandCount = island.count()
        #longestSession = 0
        #for j in range(len(islandCount)):
        #    if islandCount[j] > longestSession:
        #        longestSession = islandCount[j]

        #island = island.drop(island.index[longestSession:])
    #resample the data 
        #get shortest col
        shortestCol = 100000
        for col in island.columns:
            if island[col].count() < shortestCol: 
                shortestCol = island[col].count()
        #resample a col using the shortestCol
        for col in island.columns:
            diff = island[col].count()-shortestCol
            if diff != 0:
                nth = int(island[col].count()/diff)
                #print(len(island[col]))
                for increment in range(0,len(island[col]),nth):
                    if not (increment >= len(island[col])-1):
                        print(increment, ":",len(island[col]))
                        #avg = (island[col][increment]+island[col][increment-1]+island[col][increment+1])/3
                        #print(avg)
                #print("%s = %s - %s with a nth of %s"%(diff,island[col].count(),shortestCol,nth))
                    


        #island = island.interpolate(time="%s"%(longestCol))
        #give the dataframe a name   
        island.name = times[0].iloc[i+1]['island']
        islandDfs[i] = island
    return islandDfs

#process/clean raw data
for i in range(len(sessions)):
    sessions[i] = splitIslands(sessions[i],times[i])
islandDfs = islandDataframe(sessions,times)
islandDfs = resizeIslandFrames(islandDfs)
#for island in islandDfs:
    #island.plot()
    #print(island.name, ":\n",island)

#plt.show()
#myList = []
##for i in range(10):
#    myList.append(0)
#for i in range(0,len(myList),3):
#    print(i)