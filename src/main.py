'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- Sometimes order ids are not in the orderMap but do still exist.
    * is it that the id is not being added?
    * or is the order not being removed?
- Get rid of all agent stuff, try just running DATAlob
- Make it print every add and remove of order
'''

if __name__ == '__main__':
    
    from PyLOBsim import DataModel
    from PyLOBsim import Market
    from PyLOB import OrderBook
    import os
    import pprint
    
    os.chdir('/Users/User/Downloads')
    
    theMarket = Market(True, 'DBKd', '2013-04-22_EU_pitch_short')
    
    traderSpec = [('MM', 100),
                  ('HFT', 1),
                  ('FBYR', 50),
                  ('FSLR', 50)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    theMarket.run('1', 1000000, traderSpec, dumpFile, 0.0004)
    theMarket.plotPrices()
    
    
    
    