import pandas as pd
import numpy as np



d1 = {'col1': range(60,120,3)}
d2 = list(range(18,33))
d2 = d2[::-1]
while len(d2) < 20: 
    d2.append(np.nan)
df = pd.DataFrame(data=d1)
df['col2'] = d2


shortestCol = 100000
for col in df.columns:
    if df[col].count() < shortestCol: 
        shortestCol = df[col].count()
print(df)
for col in df.columns:
    diff = df[col].count()-shortestCol
    if diff != 0:
        print(col)
        nth = int(df[col].count()/diff)
        print("nth = %s"%(nth))
        colSeries = df[col]
        print("colSeries:\n",colSeries)
        for i in range(1,len(colSeries),nth):
            if not (i >= len(colSeries)):
                avg=(colSeries[i]+colSeries[i-1]+colSeries[i+1])/3
                print(avg)
                print(colSeries[i-1])
                colSeries.loc[i-1]= avg
                colSeries.loc[i+1] = avg
                colSeries = colSeries.drop(index=i)
        print(colSeries)        
        df[col] = colSeries
print(df)