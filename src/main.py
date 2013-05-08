'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- Changing the price of the 'action' causes KeyError, this seems weird to me
'''

if __name__ == '__main__':
    
    from PyLOBsim import Market
    import os
    
    os.chdir('/Users/user/git/PyLOBsim/src/Data')
    
    theMarket = Market(True, 'DBKd', '2013-04-22_EU_pitch_short')
    
    traderSpec = [('MM', 100),
                  ('HFT', 1),
                  ('FBYR', 50),
                  ('FSLR', 50)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    start_time = 28802147
    end_time = 59400001
    
    theMarket.genDataMap(start_time, end_time, True)
    
    theMarket.run('1', start_time, end_time, traderSpec, dumpFile, 0.01)

    theMarket.plotPrices()
    
    
    
    