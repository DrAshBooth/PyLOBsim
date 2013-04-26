'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:


'''

import random

class Trader(object):
    '''
    Trader superclass. All Traders have:
    - a trader id
    - bank balance
    - blotter
    - list of orders to execute
    '''

    def __init__(self, ttype, tid, balance):
        self.ttype = ttype
        self.tid = tid
        self.balance = balance
        self.blotter = []
        self.outstandingOrders = {} # Dict of order currently in lob keyed of ID
        self.willing = 1
        self.able = 1
        self.lastquote = None
    
    def orderInBook(self, order):
        idNum = order['idNum']
        self.outstandingOrders[idNum] = order

    def bookkeep(self, trade, side, orderID, verbose):
        self.blotter.append(trade)  # Add trade record to trader's blotter
        qty = trade['qty']
        if orderID:
            if trade['qty'] < self.outstandingOrders[orderID]:
                # modify the order amount
                self.outstandingOrders[orderID]['qty'] -= qty
            else:
                self.outstandingOrders.remove(orderID)
        transactionPrice = trade['price']
        prevBalance = self.balance
        if side == 'bid':
            self.balance -= transactionPrice * qty
        else:
            self.balance += transactionPrice * qty
        if verbose: print('previous balance=%f, new balance=%f ' % 
                          (prevBalance, self.balance))
        
    def respond(self, time, lob, trade, verbose):
        '''
        Specify how trader responds to events in the market. This is a null 
        action, expect it to be overloaded with clever things by specific 
        algorithms
        '''
        return None

    def __str__(self):
        return ('[TID %s type %s balance %s blotter %s orders %s]' % 
                (self.tid, self.ttype, 
                 self.balance, self.blotter, 
                 self.outstandingOrders))
        
        
class MarketMaker(Trader):
    '''
    Intermediaries, that post prices on both sides of the order book and
    try to maintain their position throughout the day, making their income from
    the difference between their bid and offer price.
    ''' 
    
    def getAction(self, time, time_left, exchange):
        # What should quantity be?
        qty = 2000
        order = {'qty' : qty,
                 'type' : 'limit',
                 'tid' : self.tid}
        if random.random() < 0.5:
            # bid large order just below best bid
            bb = exchange.getBestBid()
            if bb:
                order['price'] = bb - exchange.tickSize
                order['side'] = 'bid'
                return order
        else:
            # ask large order just above best ask
            ba = exchange.getBestAsk()
            if ba:
                order['price'] = ba + exchange.tickSize
                order['side'] = 'ask'
                return order
        return None
        
    

class HFT(Trader):
    '''
    High Frequency Traders, who have a relatively low net position throughout
    the day, compared to their activity. They are similar MarketMakers, but
    have much higher trading activity and much shorter holding periods.
    '''
    
    def getAction(self, time, time_left, exchange):
        # What should quantity be?
        qty = 10
        order = {'qty' : qty,
                 'type' : 'limit',
                 'tid' : self.tid}
        if random.random() < 0.5:
            # bid small order just above best bid
            bb = exchange.getBestBid()
            if bb:
                order['price'] = bb + exchange.tickSize
                order['side'] = 'bid'
                return order
        else:
            # ask small order just below best ask
            ba = exchange.getBestAsk()
            if ba:
                order['price'] = ba - exchange.tickSize
                order['side'] = 'ask'
                return order
        return None
    

class FBuyer(Trader):
    '''
    Fundamental Buyers, who try to build a long position during the day.
    '''
    
    def getAction(self, time, time_left, exchange):
        # What should qty be?
        qty = 500
        order = None
        if random.random() < 0.1:
            order = {'qty' : qty,
                     'type' : 'market',
                     'side' : 'bid',
                     'tid' : self.tid}
        return order


class FSeller(Trader):
    '''
    Fundamental Sellers, who try to build a short position during the day.
    '''
    
    def getAction(self, time, time_left, exchange):
        # What should qty be?
        qty = 500
        order = None
        if random.random() < 0.1:
            order = {'qty' : qty,
                     'type' : 'market',
                     'side' : 'ask',
                     'tid' : self.tid}
        return order
    
    
    
    
    
    
    
        