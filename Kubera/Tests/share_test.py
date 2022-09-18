import pandas as pd
import pandas_datareader as pdr
import datetime

import sys
sys.path.append("/Users/santhosh/Documents/projects/kubera/Kubera")
from Model.share import Share

def main():
    share = Share('d05')
    
    # check if share is valid
    # if not share.is_valid:
    #     print('invalid share')
    #     return
    # # dividend summary test
    a = share.get_dividend_summary(datetime.datetime.now().year, datetime.datetime.now().year - 5)
    # DS object print test
    for item in a:
        print(item.amount)
    # print(share.price)
    # print(share.open)
    # print(share.volume)
    # print(share.low)
    # print(share.high)
    # print(share.previous_close)
    # print(share.fifty_day_ma)
    # print(share.get_dividend_summary(datetime.datetime.now().year, datetime.datetime.now().year - 5))

    # print(share.two_hundred_day_ma)


main()
