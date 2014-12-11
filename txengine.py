#!/usr/bin/env python

import subprocess
import os
import time
import json
import re
import json
import requests


def _curl(curl_method = 'POST', curl_headers = None, curl_data = None , curl_isDataBinary = True, curl_url = None,  curl_user_password = None, curl_params = None):

    try:
       
        
        if curl_method == 'POST': 
            r = requests.post(curl_url,data=curl_data,headers=curl_headers,params=curl_params)
        else:
            r = requests.get(curl_url,data=curl_data,headers=curl_headers,params=curl_params)
        return r  

    except:
        raise IOError("Error sending curl command")
    
class TxEngine:
    
    def setToken(self, token):
        self.token = token

    def getAccountID(self):
        response = self.getAccountInfo()
        return json.loads(response.content)['accounts'][0]['accountId']

    def setAccountID(self, accountId):
        self.accountId = accountId   
  
    def getAccountInfo(self):
        
        method = 'GET'
        header = {}
        header['Authorization'] = 'Bearer ' + self.token
        url = 'https://api-fxpractice.oanda.com/v1/accounts'
 
        isDataBinary = False 
    
        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url)
        return result

    def getInstrumentPrice(self, instrument):
        method = 'GET'
        params = {}
        params['instruments'] = instrument
        header = {}
        header['Authorization'] = 'Bearer ' + self.token
        url = 'https://api-fxpractice.oanda.com/v1/prices'
    
        isDataBinary = False 
    
        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url, curl_params = params)
        return result

    def makeMarketBuyTrade(self, instrument, units):
        method = 'POST'
        header = {}
        header['Authorization'] = 'Bearer ' + self.token
        url = 'https://api-fxpractice.oanda.com/v1/accounts/' + str(self.accountId) +'/orders'
        data = {}
        data['instrument'] = instrument
        data['units'] = units
        data['side'] = 'buy'
        data['type'] = 'market' 
    
        isDataBinary = False 
    
        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url, curl_data = data)
        return result

    def makeMarketSellTrade(self, instrument, units):
        #curl -X POST -d "instrument=EUR_USD&units=2&side=sell&type=market" "https://api-fxpractice.oanda.com/v1/accounts/9079181/orders" -H "Authorization: Bearer 03a6098a3e33c4086b672a5a6d88a2ed-90f37d499e126f47c914c6454276febd"

        method = 'POST'
        
        header = {}
        header['Authorization'] = 'Bearer ' + self.token
        
        url = 'https://api-fxpractice.oanda.com/v1/accounts/' + str(self.accountId) +'/orders'
        
        data = {}
        data['instrument'] = instrument
        data['units'] = units
        data['side'] = 'sell'
        data['type'] = 'market' 
    
        isDataBinary = False 
    
        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url, curl_data = data)
        return result
    
    def getAllOpenTrades(self):
        #curl -X GET "http://api-sandbox.oanda.com/v1/accounts/12345/trades?instrument=EUR_USD&count=2"
        method = 'GET'
        
        header = {}
        header['Authorization'] = 'Bearer ' + self.token

        #params = {}
        #params['instrument'] = instrument
        
        url = 'https://api-fxpractice.oanda.com/v1/accounts/' + str(self.accountId) +'/trades'
     
    
        isDataBinary = False 
    
        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url)
        return result

    def closeAllOpenTrades(self):
        response = self.getAllOpenTrades()
        trades = json.loads(response.content)['trades']
        for trade in trades:
            side = trade['side']
            units = trade['units']
            instrument = trade['instrument']
            if side == 'sell':
                self.makeMarketBuyTrade(instrument, units)
            elif side == 'buy':
                self.makeMarketSellTrade(instrument, units)
                
    def getCandles(self, instrument):
        #curl -X GET "http://api-sandbox.oanda.com/v1/candles?instrument=EUR_USD&count=2&candleFormat=midpoint&granularity=D&dailyAlignment=0&alignmentTimezone=America%2FNew_York
        method = 'GET'

        header = {}
        header['Authorization'] = 'Bearer ' + self.token

        params = {}
        params['instrument'] = instrument
        params['count'] = '1'
        params['candleFormat'] = 'midpoint'
        params['granularity'] = 'D'
        params['dailyAlignment'] = '0'
        params['alignmentTimezone'] = 'America/New_York'
        
        url = 'https://api-fxpractice.oanda.com/v1/candles'
     
    
        isDataBinary = False  

        result = _curl(curl_method = method, curl_headers = header, curl_isDataBinary= isDataBinary, curl_url = url, curl_params = params)
        return result
    





