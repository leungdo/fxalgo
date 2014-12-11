from algorithm_basic import AlgorithmBasic
import txengine
import logging
import time
import datetime

# Global vars
URL = "https://api-fxpractice.oanda.com"
TOKEN = '03a6098a3e33c4086b672a5a6d88a2ed-90f37d499e126f47c914c6454276febd'

# Setup logging
logname = 'logs/trade_' + time.strftime("%Y%m%d%H%M%S") + '.log'  
logging.basicConfig(filename=logname,level=logging.DEBUG)

algo = AlgorithmBasic()
algo.setup(TOKEN)
algo.execute()

