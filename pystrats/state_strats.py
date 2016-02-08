'''
Created on Feb 8, 2016

@author: sarahhartman
'''

from utility.pyfunc import readYahoo, dsInsert
from pandas.stats.moments import rolling_mean
import numpy as np

def strat_maLong_maShort(
        df =  readYahoo('SPY'),
        maLongDays=10,
        maShortDays=3,
        closeCol='Close',
        highCol='High',
        lowCol='Low',
        openCol='Open',
        signOfTrade=1,
        printit=True):
    close = np.array(df[closeCol])
    high = np.array(df[highCol])
    low = np.array(df[lowCol])
    open = np.array(df[openCol])
    date = np.array(df['Date'])

    ma10 = rolling_mean(close,maLongDays)
    ma9 = rolling_mean(close,maLongDays-1)
    ma3 = rolling_mean(close,maShortDays)
    ma2 = rolling_mean(close,maShortDays-1)
    
    n = len(df)
    nl = n-1

#     pMa10 = dsInsert(ma10[0:nl],0,None)
#     pMa9 = dsInsert(ma9[0:nl],0,None)
#     pMa3 = dsInsert(ma3[0:nl],0,None)
#     pMa2 = dsInsert(ma2[0:nl],0,None)

    pMa10 = np.insert(ma10[0:nl],0,None)
    pMa9 = np.insert(ma9[0:nl],0,None)
    pMa3 = np.insert(ma3[0:nl],0,None)
    pMa2 = np.insert(ma2[0:nl],0,None)
    
    pClose = np.insert(close[0:nl],0,None)
    pHigh = np.insert(high[0:nl],0,None)
    pLow = np.insert(low[0:nl],0,None)

    # initialize state vector
    state = [1]*n
    pState = state
    
    #loop
    start_i = maLongDays+1
    for i in range(start_i,n):
        if (pClose[i] < pMa10[i]) & (state[i-1]==1) & (high[i] > pMa9[i]):
            state[i] = 2
        elif (state[i-1] == 2) & (low[i] > pMa2[i]):
            state[i] = 2
        elif (state[i-1]==2) & (low[i] <= pMa2[i]):
            state[i] = 1

        
    print(state)
   
    
strat_maLong_maShort()

#strat_maLong_maShort()