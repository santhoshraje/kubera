from Kubera.share import Share
import pandas as pd
import pandas_datareader as pdr
import datetime


def main():
    df = pd.read_csv('../data.csv')
    tickers = df['Trading Code'].to_list()
    pd.set_option('display.max_columns', None)
    ibm = pdr.get_data_yahoo(symbols='IBM', start='2015-1-1', end='2015-12-31')
    v = pdr.get_quote_yahoo()

    print(ibm.columns.values)

    # for ticker in tickers:
    #     share = Share(ticker)
    #
    #     # filter out penny stocks
    #     if share.price > 1 and share.market_cap > 200000000:
    #         if share.fifty_day_ma > share.two_hundred_day_ma:
    #             print(share.name)
    #             print(share.fifty_day_ma)
    #             print(share.two_hundred_day_ma)

    # a = share.get_dividend_summary(2020, 2015)
    # s = ''
    #
    # if share.is_valid is False:
    #     print('invalid ticker')
    #
    # if a is None:
    #     print('Dividend data not available')
    #     return
    #
    # for item in a:
    #     s += str(item.year) + ' (' + str(item.total) + ')' + '\n'
    #     i = 1
    #     for pay_date, pay_amount in zip(item.pay_date, item.amount):
    #         if pay_amount is '-':
    #             continue
    #         s += '‣ ' + pd.to_datetime(pay_date).strftime('%d %B') + ': ' + str(pay_amount).replace('SGD', 'SGD ') + '\n'
    #         i += 1
    #     s += '\n'
    # print(s)
    # print(share.fifty_day_ma)
    # print(share.two_hundred_day_ma)
    # s.get_data(2019)
    # s.get_dividend_breakdown(2019)
    # dividends = s.get_dividend_payout(datetime.datetime.now().year, datetime.datetime.now().year - 5)

    # for key, value in dividends.items():
    #     print(key, value)


main()
