'''
Created on 16 Apr 2013

@author: Ash Booth
'''
import sys
import random
from PyLOB import OrderBook
from datareader import DataModel
from traders import MarketMaker, HFT, FBuyer, FSeller

class Market(object):
    '''
    classdocs
    '''

    def __init__(self, usingAgents, symbol, filename=None):
        '''
        Constructor
        '''
        self.usingAgents = usingAgents
        self.dataModel = None
        self.inDatafile = filename
        self.symbol  = symbol.ljust(6)
        self.traders = {}
        self.exchange = OrderBook()
        # To keep track of what the state of the book would have been without
        # the agents, we use a data only LOB. We don't care about the output 
        # from this. 
        self.dataOnlyLob = OrderBook()
        
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
            else:
                sys.exit("FATAL: don't know agent type %s\n" % agentType)
        if self.usingAgents:
            n_agents = 0
            for agentType in tradersSpec:
                ttype = agentType[0]
                for a in range(agentType[1]):
                    tname = 'B%02d' % n_agents  # Trader i.d. string
                    self.traders[tname] = traderType(ttype, tname)
                    n_agents += 1
            if n_agents < 1:
                print 'WARNING: No agents specified\n'
        self.dataModel = DataModel(self.symbol)
        self.dataModel.readFile(self.inDatafile, verbose)
        if self.usingAgents and verbose :
            for t in range(n_agents):
                name = 'B%02d' % t
                print(self.traders[name])
                
    
    def tradeStats(self, expid, dumpfile, time):
        '''
        Dumps CSV statistics on self.exchange data and trader population to file for 
        later analysis.
        '''
        if self.usingAgents:
            trader_types = {}
            for t in self.traders:
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
    
    def plotPrices(self):
        import pylab
        prices = []
        times = []
        print "Num of trades = ", len(self.exchange.tape)
        for tapeitem in self.exchange.tape:
            prices.append(tapeitem['price'])
            times.append(tapeitem['time'])
        pylab.plot(times,prices,'ko')
        pylab.show()
    
    def run(self, sessId, endTime, traderSpec, dumpFile, agentProb):
        '''
        One day run of the market
        ''' 

        self.populateMarket(traderSpec, False)

        processVerbose = False
        respondVerbose = False
        bookkeepVerbose = False
        
        time = 0

        while time < endTime:
            timeLeft = (endTime - time) / endTime
            #print('%s; t=%08.2f (%4.1f) ' % (sessId, time, timeLeft*100))
            trades = []
            if self.usingAgents and random.random() < agentProb:
                # Get action from agents
                tid = random.choice(self.traders.keys())
                action = self.traders[tid].getAction(time, timeLeft, self.exchange)
                fromData = False
            else:
                # Get action from data
                action, day_ended = self.dataModel.getNextAction(self.exchange)
                # RELATIVE PRICING PLEASE!!!!!
                fromData = True
                
            if action != None:
                atype = action['type']
                if atype == 'market' or atype =='limit':
#                    if fromData:
#                        # Add to data book for reference
#                        self.dataOnlyLob.processOrder(action, fromData, False)
#                        # Use relative pricing to add to self.exchange
#                        if atype == 'limit':
#                            do_ba = self.dataOnlyLob.getBestAsk()
#                            do_bb = self.dataOnlyLob.getBestBid()
#                            c_ba = self.exchange.getBestAsk()
#                            c_bb = self.exchange.getBestBid()
#                            if do_ba and do_bb and c_ba and c_bb:
#                                data_mid_price = do_bb + (do_ba-do_bb)/2
#                                deviation = ((action['price']-data_mid_price) / 
#                                             data_mid_price)
#                                current_mid_price = c_bb + (c_ba-c_bb)/2
#                                action['price'] = (current_mid_price + 
#                                                   deviation*current_mid_price)
                    res_trades, orderInBook = self.exchange.processOrder(action, 
                                                                fromData, 
                                                                processVerbose)
                    if res_trades:
                        for t in res_trades:
                            trades.append(t)
                elif action['type'] == 'cancel':
                    if fromData:
#                        self.dataOnlyLob.cancelOrder(action['side'], 
#                                                     action['idNum'], 
#                                                     time = action['timestamp'])
                        self.exchange.cancelOrder(action['side'], 
                                                  action['idNum'],
                                                  time = action['timestamp'])
                    else:
                        self.exchange.cancelOrder(action['side'], 
                                                  action['idNum'])
                elif action['type'] == 'modify':
                    if fromData:
#                        self.dataOnlyLob.modifyOrder(action['idNum'], 
#                                                     action, 
#                                                     time = action['timestamp'])
                        self.exchange.modifyOrder(action['idNum'], 
                                                  action,
                                                  time = action['timestamp'])
                    else:
                        self.exchange.modifyOrder(action['idNum'], 
                                                  action)
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
                    if self.usingAgents:
                        for t in self.traders.keys():
                            self.traders[t].respond(time, self.exchange, 
                                                    trade, respondVerbose)
            time += 1

        # end of an experiment -- dump the tape
        self.exchange.tapeDump('transactions.csv', 'w', 'keep')
 
        # write trade_stats for this experiment NB end-of-session summary only
        self.tradeStats(sessId, dumpFile, time)



