import pandas as pd
import requests
from pandas_datareader import data
from millify import millify
from Utils.logging import get_logger as log


class Share:
    def __init__(self, name):
        self.ticker_raw = name.upper()
        self.ticker = self.ticker_raw + ".SI"
        # get ticker data
        self.data = self.__data()
        # general information
        self.market_cap = self.__market_cap()
        self.book_value = self.__book_value()
        self.name = self.__name()
        self.price = self.__price()
        # dividend information
        self.payout_amount = 'unavailable'
        self.payout_date = 'unavailable'
        self.yield_data = 'unavailable'

    # mode 1 = return string
    # mode 2 = return float
    def get_total_dividend_payout(self, year, mode):
        i = 0
        total_dividends = 0
        url = "https://www.dividends.sg/view/" + self.ticker_raw
        html = requests.get(url).text
        df = pd.read_html(html)[0]
        df.columns = df.columns.str.replace(' ', '')
        for x in df.iterrows():
            if df.iloc[i].Year == year:
                tmp = df.iloc[i].Total
                total = float(tmp.replace('SGD', ''))
                if mode is 1:
                    return tmp
                else:
                    return total
            i += 1

    def get_upcoming_dividends(self):
        url = "https://www.dividends.sg/dividend/coming"
        html = requests.get(url).text
        df = pd.read_html(html)[0]
        df.columns = df.columns.str.replace(' ', '')
        # get data from page
        self.payout_amount = str(df.loc[df.Ticker == self.ticker_raw, 'Amount'].values[0])
        d = pd.to_datetime(str(df.loc[df.Ticker == self.ticker_raw, 'NextDividend'].values[0]))
        self.payout_date = d.strftime('%d %B %Y')
        self.yield_data = str(df.loc[df.Ticker == self.ticker_raw, 'Yield'].values[0])

    def __str__(self):
        return 'Name:' + self.name + ' (' + self.ticker_raw + ')\nLatest price: SGD' + str(
            self.price) + '\nMarket Cap: ' + str(
            self.market_cap) + '\nBook Value Per Share (MRQ): SGD' + self.book_value \
               + '\nPayout Amount: ' + self.payout_amount + '\nPayout date: ' + self.payout_date + '\n Yield: ' + self.yield_data + '\n'

    def __data(self):
        try:
            tmp = data.get_quote_yahoo(self.ticker)
        except IndexError:
            # log().warning('ticker data not available for %s', self.ticker)
            tmp = None

        if tmp.empty:
            return 'unavailable'

        return tmp

    def __name(self):
        try:
            tmp = self.data['longName'].to_string(index=False)
        except KeyError:
            log().warning('name not available for %s', self.ticker)
            tmp = None

        if not tmp:
            return 'unavailable'
        return tmp

    def __price(self):
        try:
            tmp = self.data['price'].to_string(index=False)
        except KeyError:
            log().warning('price data not available for %s', self.ticker)
            tmp = None

        if not tmp:
            return 'unavailable'
        return tmp

    def __market_cap(self):
        try:
            tmp = millify(float(self.data['marketCap'].to_string(index=False)))
        except KeyError:
            log().warning('market cap data not available for %s', self.ticker)
            tmp = None

        if not tmp:
            return 'unavailable'
        return tmp

    def __book_value(self):
        try:
            tmp = self.data['bookValue'].to_string(index=False)
        except KeyError:
            # log().warning('book value data not available for %s', self.ticker)
            tmp = None

        if not tmp:
            return 'unavailable'
        return tmp

