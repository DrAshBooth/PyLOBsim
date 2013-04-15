'''
Created on 15 Apr 2013

@author: Ash Booth

TODO:
- bookeep is nonsense at the moment!


'''

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
        self.orders = []
        self.willing = 1
        self.able = 1
        self.lastquote = None

    def bookkeep(self, trade, order, verbose):
        self.blotter.append(trade)  # add trade record to trader's blotter
        # NB What follows is **LAZY** -- assumes all orders are quantity=1
        transactionprice = trade['price']
        if self.orders[0].otype == 'Bid':
                profit = self.orders[0].price - transactionprice
        else:
                profit = transactionprice - self.orders[0].price
        self.balance += profit
        if verbose: print('%s profit=%d balance=%d ' % 
                          (outstr, profit, self.balance))
        self.del_order(order)  # delete the order
        
    def respond(self, time, lob, trade, verbose):
        '''
        Specify how trader responds to events in the market. This is a null 
        action, expect it to be overloaded with clever things by specific 
        algorithms
        '''
        return None

    def __str__(self):
        return ('[TID %s type %s balance %s blotter %s orders %s]' % 
                (self.tid, self.ttype, self.balance, self.blotter, self.orders))
        