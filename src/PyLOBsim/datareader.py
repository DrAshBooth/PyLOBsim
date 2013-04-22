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
                if a >5000: break # REMEMBER TO TAKE THIS OUT
                line = line[1:]
                self.infile.append(line)
                a +=1
            self.numEntries = len(self.infile)
            if verbose: print "lines read"
        except IOError:
            sys.exit('Cannot open input file: {}'.format(filename))
            
    def getNextAction(self, lob):
        self.currIndex+=1
        quote = {}
        idx = self.currIndex
        for i in range(self.currIndex, self.numEntries):
            self.currIndex += 1
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
                    self.missedMOs+=1
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
                    self.missedMOs+=1
            elif messageType == 'X':
                if lob.asks.orderExists(idNum):
                    # complete cancel or a modify?
                    currentQty = lob.asks.getOrder(idNum).qty
                elif lob.bids.orderExists(line[9:21]):
                    # complete cancel or a modify?
                    currentQty = lob.bids.getOrder(idNum).qty
            elif messageType == 'x':
                pass
        self.currIndex = idx
#        if not quote:
#            return None
#        else:
#            return quote

        

os.chdir('/Users/User/Downloads')

the_model = DataModel('MTSe  ')

the_model.readFile('2013-04-18_EU_pitch', False)
the_model.getNextAction()
the_model.getNextAction()
the_model.getNextAction()
the_model.getNextAction()