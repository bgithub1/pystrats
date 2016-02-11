'''
Created on Feb 8, 2016

@author: bill perlman
'''

from utility.pyfunc import readYahoo, dsInsert, asb
from pandas.stats.moments import rolling_mean
import numpy as np
from pandas.core.frame import DataFrame
import pandas as pd

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
    ''' execute strategy which enters and exit based on Moving Average crossovers
        Example:
            from pystrats.state_strats import strat_maLong_maShort as ss
            dfretfinal = ss() #strat_maLong_maShort()
            print dfretfinal
            print dfretfinal['ret'].mean()
        
    '''
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
    state = np.array([1]*n)
    
    
    #loop
    start_i = maLongDays+1
    for i in range(start_i,n):
        if (pClose[i] < pMa10[i]) & (state[i-1]==1) & (high[i] > pMa9[i]):
            state[i] = 2
        elif (state[i-1] == 2) & (low[i] > pMa2[i]):
            state[i] = 2
        elif (state[i-1]==2) & (low[i] <= pMa2[i]):
            state[i] = 1

        
    pState = np.insert(state[0:nl],0,1)
    
    # create entry conditions
    # 1. initial entry (state 1 to state 2)
    e1_2 = np.array((pState==1) & (state==2))
    e2_2 = np.array((pState==2) & (state==2))
    e2_1 = np.array((pState==2) & (state==1))
    
    dfret = DataFrame([date,pHigh,pLow,pClose,pMa10,pMa9,pMa3,pMa2]).T
    dfret.columns = ['Date','pHigh','pLow','pClose','pMa10','pMa9','pMa3','pMa2']
    
    #create daily entry prices
    dailyEntryPrices = np.array([0]*n) 
    # default entry
    dailyEntryPrices = asb(dailyEntryPrices,pMa9, e1_2)
    useCloseOnEntry = e1_2 & (low > pMa9)
    dailyEntryPrices = asb(dailyEntryPrices,close,useCloseOnEntry)
    dailyEntryPrices = asb(dailyEntryPrices,pClose, e2_2)
    dailyEntryPrices = asb(dailyEntryPrices,pClose, e2_1)
    dfret['entry'] = dailyEntryPrices
    
    # create DAILY settle prices, which are either 0 or the Close
    # dfret$Close <- close
    dailySettlePrices = np.array([0]*n)
    dailySettlePrices = asb(dailySettlePrices,close, e1_2) #<- close[w1_2]
    dailySettlePrices = asb(dailySettlePrices,close, e2_2) #dailySettlePrices[w2_2] <- close[w2_2]
    dailySettlePrices = asb(dailySettlePrices,pMa2, e2_1) #dailySettlePrices[w2_1] <- pMa2[w2_1]
    
        # adjust for situations where the high is below the pMa2, so you get out at the close
    useCloseOnExit = e2_1 & (high < pMa2)
    dailySettlePrices  = asb(dailySettlePrices,close, useCloseOnExit) #dailySettlePrices[useCloseOnExit] <- close[useCloseOnExit]
    dfret['exit'] = dailySettlePrices
    dfret['ret'] = dfret['exit']/dfret['entry'] - 1
    
    dfret['ret'].fillna(0)
    dfretfinal = dfret.dropna(0)#dfretfinal <- dfret[-badrows(dfret),]
    return dfretfinal
    
