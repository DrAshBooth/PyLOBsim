'''
Created on 15 Apr 2013

@author: Ash Booth
'''

if __name__ == '__main__':
    
    from PyLOBsim import DataModel
    from PyLOBsim import Market
    from PyLOB import OrderBook
    import os
    import pprint
    
    os.chdir('/Users/User/Downloads')
    
    theMarket = Market(True, '2013-04-22_EU_pitch_short')
    
    traderSpec = [('MM', 100),
                  ('HFT', 1),
                  ('FBYR', 50),
                  ('FSLR', 50)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    theMarket.run('1', 10000, traderSpec, dumpFile, 0.4)
    theMarket.plotPrices()
    
    
    
    