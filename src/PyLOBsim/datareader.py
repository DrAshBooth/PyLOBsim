'''
Created on 19 Apr 2013

@author: Ash Booth

Python Module for reading TCP PITCH (Depth of Book) Data a from BATS / ChiX 
exchange generates: limit/ market orders and cancel opperations for use with
PyLOB (https://github.com/ab24v07/PyLOB).

A Full description of the message format of the TCP PITCH data is available at
http://cdn.batstrading.com/resources/participant_resources/BATS_Europe_PITCH_Specification.pdf

Message types we care bout:
A - add order message                Limit Order
a - add order message - long form    Limit Order
E - order executed                   Market Order
e - order executed - long form       Market Order
X - order cancel
x - order cancel - long form

'''

import sys
from test.test_iterlen import len
from BinTrees import RBTree
 
class DataModel(object):
    
    def __init__(self, symbol):
        self.infile = []
        self.numEntries = None
        self.currIndex = -1
        self.symbol = symbol
        self.missedMOs = 0
    
    def readFile(self, filename, verbose):
        try:
            if verbose: print "started reading file: {}".format(filename)
            reader = open(filename,'r')
            if verbose: print "file in memory, loading lines into list"
            a = 1
            for line in reader:
                if a > 100000: break # REMEMBER TO TAKE THIS OUT
                line = line[1:]
                self.infile.append(line)
                a +=1
            self.numEntries = len(self.infile)
            if verbose: print "lines read"
        except IOError:
            sys.exit('Cannot open input file: {}'.format(filename))
            
    def getNextAction(self, lob):
        quote = {}
        for i in range(self.currIndex, self.numEntries):
            self.currIndex += 1
            if self.currIndex>(len(self.infile)-1): 
                return None, True
            line = self.infile[self.currIndex]
            messageType = line[8]
            idNum = line[9:21]
            if messageType == 'A':  # Order added
                if line[28:34] == self.symbol:
                    quote['type'] = 'limit'
                    quote['idNum'] = idNum
                    if line[21] == 'B':
                        quote['side'] = 'bid'
                    elif line[21] == 'S':
                        quote['side'] = 'ask'
                    else:
                        sys.exit("side not recognised in short add")
                    quote['qty'] = int(line[22:28])
                    quote['price'] = float(line[34:40] + '.' + line[40:44])
                    quote['tid'] = -1
                    break
            elif messageType == 'a':
                if line[32:38] == self.symbol:  # Order added - long format
                    quote['type'] = 'limit'
                    quote['idNum'] = idNum
                    if line[21] == 'B':
                        quote['side'] = 'bid'
                    elif line[21] == 'S':
                        quote['side'] = 'ask'
                    else:
                        sys.exit("side not recognised in short add")
                    quote['qty'] = int(line[22:32])
                    quote['price'] = float(line[38:50] + '.' + line[50:57]) #change
                    quote['tid'] = -1
                    break
            elif messageType == 'E':
                if lob.asks.orderExists(idNum):
                    # Counterparty was ask
                    # market bid order
                    quote['type'] = 'market'
                    quote['side'] = 'bid'
                    quote['qty'] = int(line[21:27]) 
                    quote['tid'] = -1
                    break
                elif lob.bids.orderExists(idNum):
                    # Counterparty was a bid
                    # market ask order
                    quote['type'] = 'market'
                    quote['side'] = 'ask'
                    quote['qty'] = int(line[21:27]) 
                    quote['tid'] = -1
                    break
                else:
                    # Counterparty has already been hit.
                    # not sure what to do about this yet
                    self.missedMOs += 1
            elif messageType == 'e':
                if lob.asks.orderExists(idNum):
                    # Counterparty was ask
                    # market bid order
                    quote['type'] = 'market'
                    quote['side'] = 'bid'
                    quote['qty'] = int(line[21:31]) 
                    quote['tid'] = -1
                    break
                elif lob.bids.orderExists(idNum):
                    # Counterparty was a bid
                    # market ask order
                    quote['type'] = 'market'
                    quote['side'] = 'ask'
                    quote['qty'] = int(line[21:31]) 
                    quote['tid'] = -1
                    break
                else:
                    # Counterparty has already been hit.
                    # not sure what to do about this yet
                    self.missedMOs += 1
            elif messageType == 'X':
                if lob.asks.orderExists(idNum):
                    # complete cancel or a modify?
                    currentOrder = lob.asks.getOrder(idNum)
                    currentQty = currentOrder.qty
                    num2cancel = int(line[21:27])
                    if num2cancel>=currentQty:
                        quote['type'] = 'cancel'
                        quote['side'] = 'ask'
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'ask'
                        quote['idNum'] = idNum
                        quote['price'] = currentOrder.price
                        quote['qty'] = currentQty - num2cancel
                        quote['tid'] = -1
                    break
                elif lob.bids.orderExists(line[9:21]):
                    # complete cancel or a modify?
                    currentOrder = lob.bids.getOrder(idNum)
                    currentQty = currentOrder.qty
                    num2cancel = int(line[21:27])
                    if num2cancel>=currentQty:
                        quote['type'] = 'cancel'
                        quote['side'] = 'bid'
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'bid'
                        quote['idNum'] = idNum
                        quote['price'] = currentOrder.price
                        quote['qty'] = currentQty - num2cancel
                        quote['tid'] = -1
                    break
            elif messageType == 'x':
                if lob.asks.orderExists(idNum):
                    # complete cancel or a modify?
                    currentOrder = lob.asks.getOrder(idNum)
                    currentQty = currentOrder.qty
                    num2cancel = int(line[21:31])
                    if num2cancel>=currentQty:
                        quote['type'] = 'cancel'
                        quote['side'] = 'ask'
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'ask'
                        quote['idNum'] = idNum
                        quote['price'] = currentOrder.price
                        quote['qty'] = currentQty - num2cancel
                        quote['tid'] = -1
                    break
                elif lob.bids.orderExists(line[9:21]):
                    # complete cancel or a modify?
                    currentOrder = lob.bids.getOrder(idNum)
                    currentQty = currentOrder.qty
                    num2cancel = int(line[21:31])
                    if num2cancel>=currentQty:
                        quote['type'] = 'cancel'
                        quote['side'] = 'bid'
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'bid'
                        quote['idNum'] = idNum
                        quote['price'] = currentOrder.price
                        quote['qty'] = currentQty - num2cancel
                        quote['tid'] = -1
                    break
        if not quote:
            return None, False
        else:
            return quote, False

def shrinkData(filename, symbol, verbose):
    try:
        if verbose: print "started reading file: {}".format(filename)
        reader = open(filename,'r')
    except IOError:
        sys.exit('Cannot open input file: {}'.format(filename))
    else:
        if verbose: print "file in memory, opening outfile"
        writer = open(filename+'_short','w')
#         a = 1
        ids = RBTree()
        for line in reader:
#             if a > 100000: break # REMEMBER TO TAKE THIS OUT
            line = line[1:]
            messageType = line[8]
            idNum = line[9:21]
            if messageType == 'A':
                if line[28:34] == symbol:
                    ids.insert(idNum, idNum)
                    writer.write(line)
            elif messageType == 'a':
                if line[32:38] == symbol:
                    ids.insert(idNum, idNum)
                    writer.write(line)
            elif messageType == 'E':
                if idNum in ids:
                    writer.write(line)
            elif messageType == 'e':
                if idNum in ids:
                    writer.write(line)
            elif messageType == 'X':
                if idNum in ids:
                    writer.write(line)
            elif messageType == 'x':
                if idNum in ids:
                    writer.write(line)
#             a +=1
        if verbose: print "done"
        reader.close()
        writer.close()

if __name__=="__main":
    shrinkData(sys.argv[0], sys.argv[1], True)
            
            
            
            
            
            
            
            