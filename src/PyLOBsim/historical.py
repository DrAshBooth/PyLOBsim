'''
Created on May 14, 2013

@author: Ash Booth

'''

from datareader import DataModel
from PyLOB import OrderBook

class VWAP(object):
    
    def __init__(self):
        self.files = ['2013-05-13_EU_pitch_short', '2013-05-10_EU_pitch_short', 
                      '2013-05-09_EU_pitch_short', '2013-05-08_EU_pitch_short', 
                      '2013-05-07_EU_pitch_short', '2013-05-06_EU_pitch_short', 
                      '2013-05-03_EU_pitch_short', '2013-05-02_EU_pitch_short', 
                      '2013-05-01_EU_pitch_short', '2013-04-30_EU_pitch_short', 
                      '2013-04-29_EU_pitch_short', '2013-04-26_EU_pitch_short', 
                      '2013-04-25_EU_pitch_short', '2013-04-24_EU_pitch_short', 
                      '2013-04-23_EU_pitch_short', '2013-04-22_EU_pitch_short', 
                      '2013-04-19_EU_pitch_short', '2013-04-18_EU_pitch_short', 
                      '2013-04-17_EU_pitch_short', '2013-04-16_EU_pitch_short', 
                      '2013-04-15_EU_pitch_short', '2013-04-12_EU_pitch_short', 
                      '2013-04-11_EU_pitch_short', '2013-04-10_EU_pitch_short', 
                      '2013-04-09_EU_pitch_short', '2013-04-08_EU_pitch_short', 
                      '2013-04-05_EU_pitch_short', '2013-04-04_EU_pitch_short', 
                      '2013-04-03_EU_pitch_short', '2013-04-02_EU_pitch_short', 
                      '2013-03-28_EU_pitch_short', '2013-03-27_EU_pitch_short', 
                      '2013-03-26_EU_pitch_short', '2013-03-25_EU_pitch_short', 
                      '2013-03-22_EU_pitch_short', '2013-03-21_EU_pitch_short', 
                      '2013-03-20_EU_pitch_short', '2013-03-19_EU_pitch_short', 
                      '2013-03-18_EU_pitch_short', '2013-03-15_EU_pitch_short', 
                      '2013-03-14_EU_pitch_short', '2013-03-13_EU_pitch_short', 
                      '2013-03-12_EU_pitch_short', '2013-03-11_EU_pitch_short', 
                      '2013-03-08_EU_pitch_short', '2013-03-07_EU_pitch_short', 
                      '2013-03-06_EU_pitch_short', '2013-03-05_EU_pitch_short', 
                      '2013-03-04_EU_pitch_short', '2013-03-01_EU_pitch_short', 
                      '2013-02-28_EU_pitch_short', '2013-02-27_EU_pitch_short', 
                      '2013-02-26_EU_pitch_short', '2013-02-25_EU_pitch_short', 
                      '2013-02-22_EU_pitch_short', '2013-02-21_EU_pitch_short', 
                      '2013-02-20_EU_pitch_short', '2013-02-19_EU_pitch_short', 
                      '2013-02-18_EU_pitch_short', '2013-02-15_EU_pitch_short',
                      '2013-02-14_EU_pitch_short', '2013-02-13_EU_pitch_short', 
                      '2013-02-12_EU_pitch_short']
        self.numFiles = len(self.files)
        
    def getVWAPs(self, startTime, endTime, numBins, symbol, numDays=30):
        symbol = symbol.ljust(6)
        if numDays>self.numFiles:
            print "\nWarning, do not have enough data for %d day VWAP" % numDays
            print "capping to %d\n" % self.numFiles
            numDays = self.numFiles
            
        props = []
        lenOfDay = endTime-startTime
        binSize = lenOfDay/numBins
        
        for d in range(numDays):
            print "Day %d" % d
            f = self.files[d]
            
            dataModel = DataModel(symbol)
            dataModel.readFile(f, False)
            
            exchange = OrderBook()
            
            processVerbose = False
            
            time = startTime
            day_ended = False
            
            vols = []
            for i in range(numBins):
                vols.append(0)
            
            while not day_ended:
                
                # Get action from data
                action, day_ended = dataModel.getNextAction(exchange)
                if day_ended:
                    pass
                if action != None:
                    time = action['timestamp']
                    atype = action['type']
                    if atype == 'market' or atype =='limit':
                        res_trades, orderInBook = exchange.processOrder(action, 
                                                                        True,
                                                                        processVerbose)
                        if res_trades:
                            for t in res_trades:
                                if (time-startTime)/binSize >= len(vols):
                                    pass
                                vols[(time-startTime)/binSize] += t['qty']
                                
                    elif action['type'] == 'cancel':
                        exchange.cancelOrder(action['side'], 
                                             action['idNum'],
                                             time = action['timestamp'])

                    elif action['type'] == 'modify':
                        exchange.modifyOrder(action['idNum'], 
                                             action,
                                             time = action['timestamp'])
                        
            # Day over, work out proportions and add to props
            totalVol = sum(vols)
            props.append([v/float(totalVol) for v in vols])
            print "volumes: ", vols
            print "proportions: ", [v/float(totalVol) for v in vols], '\n'
        # Calculate average props
        sums = [0 for i in range(numBins)]
        for day in props:
            for bin_index in range(numBins):
                sums[bin_index] += day[bin_index]
        return [s/numDays for s in sums]
                

