from Model.share import Share
import pandas as pd
import pandas_datareader as pdr
import datetime


def main():
    share = Share('v03')
    # check if share is valid
    # if not share.is_valid:
    #     print('invalid share')
    #     return
    # # dividend summary test
    # a = share.get_dividend_summary(datetime.datetime.now().year, datetime.datetime.now().year - 5)
    # # DS object print test
    # for item in a:
    #     print(item)
    print(share.price)
    print(share.open)
    print(share.volume)
    print(share.low)
    print(share.high)
    print(share.previous_close)
    print(share.fifty_day_ma)

    # print(share.two_hundred_day_ma)


main()
