from txengine import TxEngine
import json
import time
import datetime
from rfc3339 import rfc3339
import logging

class AlgorithmBasic:

    def setup(self, token):
        self.txEngine = TxEngine()
        self.txEngine.setToken(token)
        self.accountId  = self.txEngine.getAccountID()
        self.txEngine.setAccountID(self.accountId)
        
    def determineInitialTrade(self):
        #get low and high
        response = self.txEngine.getCandles('EUR_USD')
        print json.loads(response.content)
        low =  json.loads(response.content)['candles'][0]['lowMid']
        high =  json.loads(response.content)['candles'][0]['highMid']
        mid = (low + high)/2
        print mid

        #get current prices
        response = self.txEngine.getInstrumentPrice('EUR_USD')
        print json.loads(response.content)
        bid = json.loads(response.content)['prices'][0]['bid']
        ask = json.loads(response.content)['prices'][0]['ask']
        print "Bid: %s"%bid
        print "Ask: %s"%ask 

        if bid < mid and ask < mid:
            return "buy"
        if bid > mid and ask > mid:
            return "sell"

        #If mid is between bid and ask, find which one is closer
        bid_delta = mid - bid
        ask_delta = ask - mid

        if ask_delta >= bid_delta:
            return "sell"
        else:
            return "buy" 
        
    def execute(self):
        print "Close all open trades"
        self.txEngine.closeAllOpenTrades()

        print "Make initial trade"
        if self.determineInitialTrade == 'buy':
            response = self.txEngine.makeMarketBuyTrade('EUR_USD', '1000')
            print response.content
            price = json.loads(response.content)['price']
            print "Initial Trade: "
            print price
            SIDE = 'buy'
            numberOfTrades = 1
        else:
            response = self.txEngine.makeMarketSellTrade('EUR_USD', '1000')
            print response.content
            price = json.loads(response.content)['price']
            print "Initial Trade: "
            print price
            SIDE = 'sell'
            numberOfTrades = 1

        while True:
            response = self.txEngine.getInstrumentPrice('EUR_USD')
            print json.loads(response.content)
            bid = json.loads(response.content)['prices'][0]['bid']
            ask = json.loads(response.content)['prices'][0]['ask']
            print "#Trades %s Side %s :Price %s, Bid %s, Ask %s" %(str(numberOfTrades), SIDE, str(price), str(bid), str(ask))
            logging.info("#Trades %s Side %s :Price %s, Bid %s, Ask %s", str(numberOfTrades), SIDE, str(price), str(bid), str(ask))
            if bid > price and SIDE == 'buy':
                self.txEngine.closeAllOpenTrades()
                response = self.txEngine.makeMarketSellTrade('EUR_USD', '1000')
                price = json.loads(response.content)['price'] 
                SIDE = 'sell'
                numberOfTrades = numberOfTrades + 1
            elif ask < price and SIDE == 'sell':
                self.txEngine.closeAllOpenTrades()
                response = self.txEngine.makeMarketBuyTrade('EUR_USD', '1000')
                price = json.loads(response.content)['price'] 
                SIDE = 'buy'  
                numberOfTrades = numberOfTrades + 1   
            time.sleep(2)
