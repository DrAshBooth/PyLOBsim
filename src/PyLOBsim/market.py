'''
Created on 16 Apr 2013

@author: Ash Booth
'''
import sys
import random
from PyLOB import OrderBook
from datareader import DataModel

from traders import MarketMaker, HFT, FBuyer, FSeller, Opportunistic

class Market(object):
    '''
    classdocs
    '''

    def __init__(self, usingData, filename=None):
        '''
        Constructor
        '''
        self.usingData = usingData
        self.dataModel = None
        self.inDatafile = filename
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
        if self.usingData:
            self.dataModel = DataModel('MTSe  ')
            self.dataModel.readFile(self.inDatafile, verbose)
        if verbose :
            for t in range(n_agents):
                name = 'B%02d' % t
                print(self.traders[name])
                
    
    def tradeStats(self, expid, dumpfile, time):
        '''
        Dumps CSV statistics on exchange data and trader population to file for 
        later analysis.
        '''
        trader_types = {}
        for t in self.agents:
            ttype = self.traders[t].ttype
            if ttype in trader_types.keys():
                t_balance = (trader_types[ttype]['balance_sum'] + 
                             self.traders[t].balance)
                n = trader_types[ttype]['n'] + 1
            else:
                t_balance = self.traders[t].balance
                n = 1
            trader_types[ttype] = {'n':n, 'balance_sum':t_balance}

        dumpfile.write('%s, %06d, ' % (expid, time))
        for ttype in sorted(list(trader_types.keys())):
                n = trader_types[ttype]['n']
                s = trader_types[ttype]['balance_sum']
                dumpfile.write('%s, %d, %d, %f, ' % (ttype, s, n, s / float(n)))

        dumpfile.write('\n');
    
    def run(self, sessId, endTime, traderSpec, dumpFile, agentProb):
        '''
        One day run of the market
        '''
        
        exchange = OrderBook()
        
        # To keep track of what the state of the book would have been without
        # the agents, we use a data only LOB. We don't care about the output 
        # from this. 
        dataOnlyLob = OrderBook() 

        self.populateMarket(traderSpec, True)

        processVerbose = False
        respondVerbose = False
        bookkeepVerbose = False
        
        time = 0

        while time < endTime:
            timeLeft = (endTime - time) / endTime
            #print('%s; t=%08.2f (%4.1f) ' % (sessId, time, timeLeft*100))
            trades = []
            if random.random() > agentProb:
                # Get action from data
                action, day_ended = self.dataModel.getNextAction(exchange)
                fromData = True
            else:
                # Get action from agents
                tid = random.choice(self.traders.keys())
                action = self.traders[tid].getAction(time, timeLeft, exchange)
                fromData = False
                
            if action != None:
                atype = action['type']
                if atype == 'market' or atype =='limit':
                    if fromData:
                        # Add to data book for refference
                        dataOnlyLob.processOrder(action, fromData, False)
                        # Use relative pricing to add to exchange
                        do_ba = dataOnlyLob.getBestAsk()
                        do_bb = dataOnlyLob.getBestBid()
                        if do_ba and do_bb:
                            mid_price = do_bb + (do_ba-do_bb)/2
                            deviation = do_
                        res_trades, orderInBook = exchange.processOrder(action, 
                                                                    fromData, 
                                                                    processVerbose)
                    if res_trades:
                        for t in res_trades:
                            trades.append(t['price'])
                elif action['type'] == 'cancel':
                    if fromData:
                        dataOnlyLob.cancelOrder(action['side'], action['idNum'])
                    exchange.cancelOrder(action['side'], action['idNum'])
                elif action['type'] == 'modify':
                    if fromData:
                        dataOnlyLob.modifyOrder(action['idNum'], action)
                    exchange.modifyOrder(action['idNum'], action)

                # Does the originating trader need to be informed of limit 
                # orders that has been put in the book?
                if orderInBook and not fromData:
                    self.traders[tid].orderInBook(orderInBook)
                    
                for trade in trades:
                    # Counter-parties update order lists and blotters
                    if trade['party1'][0] != -1:
                        self.traders[trade['party1'][0]].bookkeep(trade,
                                                                  trade['party1'][1],
                                                                  trade['party1'][2],
                                                                  bookkeepVerbose)
                    if trade['party2'][0] != -1:
                        self.traders[trade['party2'][0]].bookkeep(trade, 
                                                                  trade['party2'][1],
                                                                  trade['party2'][2],
                                                                  bookkeepVerbose)
                    # Traders respond to whatever happened
                    for t in self.traders.keys():
                        self.traders[t].respond(time, exchange, 
                                                trade, respondVerbose)
            time += 1

        # end of an experiment -- dump the tape
        exchange.tapeDump('transactions.csv', 'w', 'keep')
 
        # write trade_stats for this experiment NB end-of-session summary only
        self.tradeStats(sessId, dumpFile, time)



