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
import os
import sys
from test.test_iterlen import len
from BinTrees import RBTree
 
class DataModel(object):
    
    def __init__(self, symbol):
        self.infile = []
        self.numEntries = None
        self.currIndex = -1
        self.nextUEI = 0    # Unique event identifier
        self.symbol = symbol
        self.missedMOs = 0
    
    def readFile(self, filename, verbose):
        try:
            if verbose: print "started reading file: {}".format(filename)
            reader = open(filename,'r')
            if verbose: print "file in memory, loading lines into list"
            for line in reader:
                line = line[1:]
                self.infile.append(line)
            self.numEntries = len(self.infile)
            if verbose: print "lines read"
            reader.close()
        except IOError:
            sys.exit('Cannot open input file: {}'.format(filename))
    
    def resetModel(self):
        self.currIndex = -1
        self.missedMOs = 0
        self.nextUEI = 0
            
    def getNextAction(self, lob):
        quote = {}
        if self.currIndex >= (self.numEntries-3):
            return None, True # Day has ended
        for i in range(self.currIndex, self.numEntries-1):
            self.currIndex += 1
            line = self.infile[self.currIndex]
            messageType = line[8]
            idNum = line[9:21]
            if messageType == 'A':  # Order added
                if line[28:34] == self.symbol:
                    quote['type'] = 'limit'
                    quote['timestamp'] = int(line[:8])
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
                    quote['timestamp'] = int(line[:8])
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
                    quote['timestamp'] = int(line[:8])
                    quote['qty'] = int(line[21:27]) 
                    quote['tid'] = -1
                    break
                elif lob.bids.orderExists(idNum):
                    # Counterparty was a bid
                    # market ask order
                    quote['type'] = 'market'
                    quote['side'] = 'ask'
                    quote['timestamp'] = int(line[:8])
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
                    quote['timestamp'] = int(line[:8])
                    quote['qty'] = int(line[21:31]) 
                    quote['tid'] = -1
                    break
                elif lob.bids.orderExists(idNum):
                    # Counterparty was a bid
                    # market ask order
                    quote['type'] = 'market'
                    quote['side'] = 'ask'
                    quote['timestamp'] = int(line[:8])
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
                        quote['timestamp'] = int(line[:8])
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'ask'
                        quote['timestamp'] = int(line[:8])
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
                        quote['timestamp'] = int(line[:8])
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'bid'
                        quote['timestamp'] = int(line[:8])
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
                        quote['timestamp'] = int(line[:8])
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'ask'
                        quote['timestamp'] = int(line[:8])
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
                        quote['timestamp'] = int(line[:8])
                        quote['idNum'] = idNum
                    else:
                        quote['type'] = 'modify'
                        quote['side'] = 'bid'
                        quote['timestamp'] = int(line[:8])
                        quote['idNum'] = idNum
                        quote['price'] = currentOrder.price
                        quote['qty'] = currentQty - num2cancel
                        quote['tid'] = -1
                    break
        if not quote:
            return None, False
        else:
            quote['uei'] = self.nextUEI
            self.nextUEI += 1
            return quote, False

def shrinkData(filename, symbol, verbose):
    symbol = symbol.ljust(6)
    try:
        if verbose: print "started reading file: {}".format(filename)
        reader = open(filename,'r')
    except IOError:
        sys.exit('Cannot open input file: {}'.format(filename))
    else:
        if verbose: print "file in memory, opening outfile"
        writer = open(filename+'_short','w')
        ids = RBTree()
        for line in reader:
            messageType = line[9]
            idNum = line[10:22]
            if messageType == 'A':
                if line[29:35] == symbol:
                    ids.insert(idNum, idNum)
                    writer.write(line)
            elif messageType == 'a':
                if line[33:39] == symbol:
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
        if verbose: print "done"
        reader.close()
        writer.close()

# os.chdir('/Users/user/Downloads')
# shrinkData('2013-04-22_EU_pitch', 'DBKd', True)
            
            
            
            
            
            
            
            