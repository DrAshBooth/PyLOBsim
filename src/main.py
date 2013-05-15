'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- DAY is ending way to early
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
                                      symbol, numDays=20)
    
    print "Final proportions...", proportions
    
    
    
    