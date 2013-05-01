'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- Changing the price of the 'action' causes KeyError, this seems weird to me
'''

if __name__ == '__main__':
    
    from PyLOBsim import Market
    import os
    
    os.chdir('/Users/User/Downloads')
    
    theMarket = Market(False, 'DBKd', '2013-04-22_EU_pitch_short')
    
    traderSpec = [('MM', 100),
                  ('HFT', 1),
                  ('FBYR', 50),
                  ('FSLR', 50)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    runLength = 10000
    
    theMarket.genDataMap(runLength, True)
    
    theMarket.run('1', runLength, traderSpec, dumpFile, 0.0004)
    theMarket.plotPrices()
    
    
    
    