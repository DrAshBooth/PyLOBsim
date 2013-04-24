'''
Created on 15 Apr 2013

@author: Ash Booth
'''

if __name__ == '__main__':
    
    from PyLOBsim import DataModel
    from PyLOBsim import Market
    from PyLOB import OrderBook
    import os
    import pprint
    
    os.chdir('/Users/User/Downloads')
    
    #################################################
    ################### Data Only ###################
    #################################################
    
#     data_model = DataModel('MTSe  ')
#     lob = OrderBook()
#     data_model.readFile('2013-04-22_EU_pitch', True)
#     
#     day_ended = False
#     trades = []
#     while not day_ended:
#         if len(trades) > 100: break
#         action, day_ended = data_model.getNextAction(lob)
#         if action != None:
#             atype = action['type']
#             if atype == 'market' or atype =='limit':
#                 res_trades, oib = lob.processOrder(action, True, True)
#                 if res_trades:
#                     for t in res_trades:
#                         trades.append(t['price'])
#             elif action['type'] == 'cancel':
#                 lob.cancelOrder(action['side'], action['idNum'])
#             elif action['type'] == 'modify':
#                 lob.modifyOrder(action['idNum'], action)
#     
#     import pylab
#     pprint.pprint(trades)
#     pylab.plot(trades)
#     pylab.show()

    #################################################
    ################# Hybrid Model ##################
    #################################################
    
    theMarket = Market(True, '2013-04-22_EU_pitch')
    
    traderSpec = [('MM', 5), 
                  ('HFT', 5),
                  ('FBYR', 5),
                  ('FSLR', 5)]
    
    fname = 'balances.csv'
    dumpFile = open(fname, 'w')
    
    theMarket.run('1', 1000, traderSpec, dumpFile, 0.5)
    
    
    
    