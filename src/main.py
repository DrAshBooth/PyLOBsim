'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- Last run gave error:
Day 8
Traceback (most recent call last):
  File "/Users/user/git/PyLOBsim/src/main.py", line 41, in <module>
    symbol, numDays=25)
  File "/Users/user/git/PyLOBsim/src/PyLOBsim/historical.py", line 108, in getVWAPs
    props.append([v/float(totalVol) for v in vols])
ZeroDivisionError: float division by zero
'''

if __name__ == '__main__':
    
    from PyLOBsim import Market
    from PyLOBsim import VWAP
    
    import os
    
    os.chdir('/Users/user/git/PyLOBsim/src/Data')
    
    startTime = 28800000 # 08:00
    endTime = 59400000 # 16:30
    
    symbol ='DBKd'
    
#     theMarket = Market(True, symbol, '2013-04-22_EU_pitch_short')
#     traderSpec = [('MM', 100),
#                   ('HFT', 1),
#                   ('FBYR', 50),
#                   ('FSLR', 50)]
#     
#     fname = 'balances.csv'
#     dumpFile = open(fname, 'w')
# 
#     theMarket.initiateDataModel(True)
#     theMarket.run('1', start_time, end_time, traderSpec, dumpFile, 0.01)
# 
#     theMarket.plotPrices()

    vwap_model = VWAP()
    numBins = 17
    proportions = vwap_model.getVWAPs(startTime, endTime, numBins, 
                                      symbol, numDays=25)
    
    print "Final proportions...", proportions
    
    
    
    