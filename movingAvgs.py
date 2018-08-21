import pandas as pd
import numpy
import sys
import os
from panalysis import *
from compareIslands import *
import matplotlib.pyplot as plt

sessionOne = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day1.csv"
timeOne = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time1.csv"

sessionTwo = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day2.csv"
timeTwo = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time2.csv"

sessionThree = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day3.csv"
timeThree = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time3.csv"

sessionFour = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionData/day4.csv"
timeFour = "/Users/Abram/Documents/PCC/perceptionAnalyzer/sessionTimes/time4.csv"

#TODO: for each session --> truncate each session to the length of the shortest island for each session. 
#Step 1: read CSV Times for each session, and break the islands into a different dataframe. 
#        Each session is a list of dataframes, each dataframe being an island. 
#Step 2: See which session has the shortest time for each island, and 'compress' each session's island time to the shortest.
#TODO:          HOW DO I COMPRESS THE ISLANDS?




splitIslands(pd.read_csv(sessionFour),pd.read_csv(timeFour))
#to make graphs of sessions, uncomment below!

#sessions = [pd.read_csv(sessionOne),pd.read_csv(sessionTwo),pd.read_csv(sessionThree),pd.read_csv(sessionFour)]
#times = [pd.read_csv(timeOne),pd.read_csv(timeTwo),pd.read_csv(timeThree),pd.read_csv(timeFour)]
#averages = getAvgDataframe(sessions,times)
#averages.plot()
#plt.show()









