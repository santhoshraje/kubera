# external
import pandas as pd
from pandas_datareader import data
from millify import millify
# utils
from Utils.get_data import get_data
from Utils.logging import get_logger as log
# config
from config import BotConfig
# Objects
from Kubera.dividend_summary import DividendSummary as Ds
import re


class Share:
    def __init__(self, ticker):
        # remove non alpha numeric characters and change to upper case
        self.ticker = re.sub(r'\W+', '', ticker).upper()
        # ticker value to be used with yahoo finance api
        self.yahoo_ticker = self.ticker + ".SI"
        # get ticker data
        self.is_valid = True
        self.data = self.__data()
        # general information
        self.market_cap = self.__market_cap()
        self.book_value = self.__book_value()
        self.name = self.__name()
        self.price = self.__price()
        self.volume = self.__volume()
        self.open = self.__open()
        # moving averages
        self.fifty_day_ma = self.__fiftydayma()
        self.two_hundred_day_ma = self.__twohundereddayma()

    def __data(self):
        try:
            return data.get_quote_yahoo(self.yahoo_ticker)
        except IndexError:
            self.is_valid = False
            return None
        except KeyError:
            self.is_valid = False
            return None

    def __name(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return self.data['longName'].to_string(index=False)
        except KeyError:
            return 'unavailable'

    def __price(self):
        # if ticker data is unavailable
        if not self.is_valid:
            return 'unavailable'

        try:
            return float(self.data['price'].to_string(index=False))
        except KeyError:
            log().warning('price data not available for %s', self.ticker)
            return 'unavailable'

    def __market_cap(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return millify(float(self.data['marketCap'].to_string(index=False)))
        except KeyError:
            return 'unavailable'

    def __volume(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return float(self.data['regularMarketVolume'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __book_value(self):
        # if ticker data is unavailable
        if not self.is_valid:
            return 'unavailable'

        try:
            return float(self.data['bookValue'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __fiftydayma(self):
        # if ticker data is unavailable
        if not self.is_valid:
            return 'unavailable'

        try:
            return float(self.data['fiftyDayAverage'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __twohundereddayma(self):
        # if ticker data is unavailable
        if not self.is_valid:
            return 'unavailable'

        try:
            return float(self.data['twoHundredDayAverage'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __open(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return float(self.data['regularMarketOpen'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def get_dividend_summary(self, start, end=0):
        df = get_data(BotConfig().dividend_url, self.ticker)
        a = []

        if df is None:
            return None

        if end is 0:
            try:
                amount = df.loc[df.Year == start, 'Amount'].values.tolist()
                ex_date = df.loc[df.Year == start, 'ExDate'].values.tolist()
                pay_date = df.loc[df.Year == start, 'PayDate'].values.tolist()
                total = df.loc[df.Year == start, 'Total'].values[0]
                return Ds(start, total, amount, ex_date, pay_date)
            except IndexError:
                return None

        counter = start - end

        while counter > 0:
            year = end + counter
            try:
                amount = df.loc[df.Year == year, 'Amount'].values.tolist()
                ex_date = df.loc[df.Year == year, 'ExDate'].values.tolist()
                pay_date = df.loc[df.Year == year, 'PayDate'].values.tolist()
                total = df.loc[df.Year == year, 'Total'].values[0]
                a.append(Ds(year, total, amount, ex_date, pay_date))
            except IndexError:
                break
            counter -= 1
        return a

    def __str__(self):
        return 'Name:' + self.name + ' (' + self.ticker + ')\nLatest price: SGD' + str(
            self.price) + '\nMarket Cap: ' + str(
            self.market_cap) + '\nBook Value Per Share (MRQ): SGD' + self.book_value 
