import pandas as pd
import numpy
import sys


def trimEndAndStart(df, showTimeFrame):
    startOfShow = showTimeFrame.iloc[0][1]
    endOfShow = showTimeFrame.iloc[-1][-1]
    df = df.drop(df.columns[0], axis=1)
    print(len(df.index))
    #print(endOfShow)
    if not numpy.isnan(endOfShow) and type(endOfShow) != str: 
        endOfShow = int(endOfShow)
        df=df.drop(df.index[endOfShow:])
    
    if not numpy.isnan(startOfShow) and type(startOfShow) != str:
        startOfShow = int(startOfShow)
        df = df.drop(df.index[:startOfShow], axis=0)
    print(len(df.index))
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
        print(col,": ",percentValid[col])
        if percentValid[col] < 70.0:
            df = df.drop(columns=col)
    #print(df.columns)
    return df

def getAvgs(df,sessionIndex):
    avgData = pd.DataFrame()
    columns = df.columns[1:]
    for col in columns:
        columnName = "MovingAvg-"+col[6:8] if len(col) == 8 else "MovingAvg-"+col[6]
        colAvgs = df[col].rolling(10,min_periods=0).mean()
        avgData[col] = colAvgs
    avgDataAvgs = []

    for index,row in avgData.iterrows():
        avgDataAvgs.append(row.mean())
    avgDataAvgs = pd.Series(avgDataAvgs).rename("Session %s"%(sessionIndex))
    return avgDataAvgs


def getAvgDataframe(sessions, times):
    averages=[]
    index = 0
    for session in sessions:
        #print("index:",index)
        session = trimEndAndStart(session, times[index])
        session = cleanUpErrors(session)
        session = removeErrorProneCols(session)
        #print(len(session.columns))
        sessionAvgs = getAvgs(session,index+1)
        averages.append(sessionAvgs)
        #print(sessionAvgs)
        index += 1

    avgDf = pd.DataFrame()
    for average in averages:
        if average.name == "Session 1":
            newIndices=dict(enumerate(range(134,len(average.index)+134)))
            average = average.rename(index=newIndices)
            tempList = []
            for i in range(134):
                tempList.append(numpy.NaN)
            tempList = pd.Series(tempList)
            average = tempList.append(average).rename("Session 1")
            average.to_csv("/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day1TeST.csv")
        avgDf[average.name] = average#print(sessions)
        #print(average)

    return avgDf

def splitIslands(df, times):
    for index in range(len(times.index)):
        print(times.iloc[index]['start'])