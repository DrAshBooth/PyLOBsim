'''
Created on 16 Apr 2013

@author: Ash Booth
'''
import sys
import random
from PyLOB import OrderBook

from traders import MarketMaker, HFT, FBuyer, FSeller, Opportunistic

class Market(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.traders = {}
        
    def populateMarket(self, tradersSpec, verbose):
        '''
        Creates the traders from traders_spec. 
        Returns tuple (buyers, sellers).
        '''
        def traderType(agentType, name):
            if agentType == 'MM':
                return MarketMaker('MM', name, 0.00)
            elif agentType == 'HFT':
                    return HFT('HFT', name, 0.00)
            elif agentType == 'FBYR':
                    return FBuyer('FBYR', name, 0.00)
            elif agentType == 'FSLR':
                    return FSeller('FSLR', name, 0.00)
            elif agentType == 'OPTC':
                    return Opportunistic('OPTC', name, 0.00)
            else:
                sys.exit("FATAL: don't know agent type %s\n" % agentType)

        n_agents = 0
        for agentType in tradersSpec:
            ttype = agentType[0]
            for a in range(agentType[1]):
                tname = 'B%02d' % n_agents  # Trader i.d. string
                self.traders[tname] = traderType(ttype, tname)
                n_agents += 1
        if n_agents < 1:
            print 'WARNING: No agents specified\n'
        if verbose :
            for t in range(n_agents):
                name = 'B%02d' % t
                print(self.traders[name])
    
    def run(self, sessId, startTime, endTime, traderSpec, dumpFile):
        '''
        One day run of the market
        '''
        
        exchange = OrderBook()

        self.populateMarket(traderSpec, False)
        
        duration = float(endTime - startTime)
        lastUpdate = -1.0
        time = startTime

        ordersVerbose = False
        lobVerbose = False
        processVerbose = False
        respondVerbose = False
        bookkeepVerbose = False

        while time < endTime:
            timeLeft = (endTime - time) / duration
            #print('%s; t=%08.2f (%4.1f) ' % (sessId, time, timeLeft*100))
            trade = None

            # Get an order (or None) from a randomly chosen trader
            tid = random.choice(self.traders.keys())
            order = self.traders[tid].getorder(time, timeLeft, exchange)

            if order != None:
                # Send order to exchange
                trades, orderInBook = exchange.processOrder(order, 
                                                            processVerbose)
                # Does the originating trader need to be informed of limit 
                # orders that has been put in the book?
                if orderInBook:
                    self.traders[tid].orderInBook(orderInBook)
                for trade in trades:
                    # Counter-parties update order lists and blotters
                    self.traders[trade['party1'][0]].bookkeep(trade,
                                                              trade['party1'][1],
                                                              trade['party1'][2],
                                                              bookkeepVerbose)
                    self.traders[trade['party2'][0]].bookkeep(trade, 
                                                              trade['party2'][1],
                                                              trade['party2'][2],
                                                              bookkeepVerbose)
                    # Traders respond to whatever happened
                    for t in self.traders.keys():
                        self.traders[t].respond(time, exchange, 
                                                trade, respondVerbose)

            time += 1

#        # end of an experiment -- dump the tape
#        exchange.tape_dump('transactions.csv', 'w', 'keep')
#
#        # write trade_stats for this experiment NB end-of-session summary only
#        trade_stats(sessId, traders, tdump, time, exchange.publish_lob(time, lob_verbose))