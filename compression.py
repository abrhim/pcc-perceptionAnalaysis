import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from compareIslands import *

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

            #reindex the column giving it the effect as if we removed the values and smashed it to match the shortest column
            oldIndex = list(colSeries.index)
            newIndex = list(df[shortestColName].index)
            indexDict = dict(zip(oldIndex,newIndex))

            print(colSeries.count())
            colSeries = colSeries.rename(index=indexDict)
            df[col] = colSeries
    return df

islandDfs[2].to_csv("/Users/abram/Documents/PCC/perceptionAnalyzer/islandsDfs[0].csv")
compressColumns(islandDfs[2]).to_csv("/Users/abram/Documents/PCC/perceptionAnalyzer/islandsDfs[0]Compressed.csv")

#plt.show()