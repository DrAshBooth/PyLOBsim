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
    
    theMarket = Market(True, '2013-04-22_EU_pitch')
    
    traderSpec = [('MM', 5), 
                  ('HFT', 5),
                  ('FBYR', 5),
                  ('FSLR', 5)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    theMarket.run('1', 1000, traderSpec, dumpFile, 0.5)
    
    
    
    