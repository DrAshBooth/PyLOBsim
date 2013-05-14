'''
Created on May 14, 2013

@author: Ash Booth

'''

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
        
    def getVWAPs(self, startTime, endTime, numBins, numDays=30):
        if numDays>self.numFiles:
            print "\nWarning, do not have enough data for %d day VWAP" % numDays
            print "capping to %d\n" % self.numFiles
            numDays = self.numFiles
            
        props = []
        lenOfDay = endTime=startTime
        binSize = lenOfDay/numBins
        
        for d in numDays:
            f = self.files[d]