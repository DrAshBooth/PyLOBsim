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
    
    def readFile(self, filename, verbose):
        try:
            if verbose: print "started reading file: {}".format(filename)
            reader = open(filename,'r')
            if verbose: print "file in memory, loading lines into list"
            a = 1
            for line in reader:
                if a >5000: break
                line = line[1:]
                self.infile.append(line)
                a +=1
            self.numEntries = len(self.infile)
            if verbose: print "lines read"
        except IOError:
            print 
            sys.exit('Cannot open input file: {}'.format(filename))
            
    def getNextAction(self):
        self.currIndex+=1
        quote = {}
        idx = self.currIndex
        for i in range(self.currIndex, self.numEntries):
            self.currIndex += 1
            line = self.infile[self.currIndex]
            messageType = line[8]
            if messageType == 'A':  # Order added
                if line[28:34] == self.symbol:
                    quote['type'] = 'limit'
                    quote['idNum'] = line[9:21]
                    if line[21] == 'B':
                        quote['side'] = 'bid'
                    elif line[21] == 'S':
                        quote['side'] = 'ask'
                    else:
                        sys.exit("side not recognised in short add")
                    quote['qty'] = int(line[22:28])
                    quote['price'] = float(line[34:40] + '.' + line[40:44])
                    quote['tid'] = -1
#                    print "id = %s" % quote['idNum']
#                    print "side = %s" % quote['side']
#                    print "qty = %d" % quote['qty']
#                    print "price = %f\n" % quote['price']
                    break
            elif messageType == 'a':
                if line[32:38] == self.symbol:  # Order added - long format
                    relevantFound = True
                    quote['type'] = 'limit'
                    print line
            elif messageType == 'E':
                # if order id in lob.bids 
                    # market sell order
                # elif order id in lob.asks:
                    # market buy order 
                pass
            elif messageType == 'e':
                # if order id in lob.bids 
                    # market sell order
                # elif order id in lob.asks:
                    # market buy order 
                pass
            elif messageType == 'X':
                pass
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