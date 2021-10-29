# external
import pandas as pd
from pandas_datareader import data
from millify import millify
# utils
from Utils.get_data import get_data
from Utils.logging import get_logger as log
# config
from Bot.config import BotConfig
# Objects
from Model.dividend_summary import DividendSummary as Ds
import re
import time


class Share:
    def __init__(self, ticker):
        # check if index
        if '^' in ticker:
            # change to upper case
            self.ticker = ticker.upper()
            # ticker value to be used with yahoo finance api
            self.yahoo_ticker = self.ticker
        else:
            # remove non alpha numeric characters and change to upper case
            self.ticker = re.sub(r'\W+', '', ticker).upper()
            # ticker value to be used with yahoo finance api
            self.yahoo_ticker = self.ticker + ".SI"
        # get ticker data
        self.is_valid = True
        self.data = self.__data()
        # general information
        self.name = self.__name()
        self.market_cap = self.__market_cap()
        self.book_value = self.__book_value()
        self.price = self.__price()
        self.volume = self.__volume()
        self.open = self.__open()
        self.market = self.__market()
        self.type = self.__type()
        self.low = self.__low()
        self.high = self.__high()
        # moving averages
        self.fifty_day_ma = self.__fiftydayma()
        self.two_hundred_day_ma = self.__twohundereddayma()
        # percent change from open
        self.percent_changed = self.__percent_changed()
        # change from open
        self.change = self.__change()
        self.previous_close = self.__previous_close()
        self.day_range = self.__day_range()

    def __data(self):
        try:
            return data.get_quote_yahoo(self.yahoo_ticker)
        except IndexError:
            self.is_valid = False
            return None
        except KeyError:
            self.is_valid = False
            return None
        except ConnectionError as e:
            print(str(e))
            time.sleep(10)
            self.__data()

    def __name(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return self.data['shortName'].to_string(index=False)
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
            return millify(float(self.data['regularMarketVolume'].to_string(index=False)))
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
            ma = float(self.data['fiftyDayAverage'].to_string(index=False))
            return float("{:.2f}".format(ma))
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

    def __day_range(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return self.data['regularMarketDayRange'].to_string(index=False)
        except KeyError:
            return 'unavailable'

    def __high(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return float(self.data['regularMarketDayHigh'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __low(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return float(self.data['regularMarketDayLow'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __previous_close(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return float(self.data['regularMarketPreviousClose'].to_string(index=False))
        except KeyError:
            return 'unavailable'

    def __market(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return self.data['market'].to_string(index=False)
        except KeyError:
            return 'unavailable'

    def __type(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            return re.sub(r'\W+', '', self.data['quoteType'].to_string(index=False)).lower()
        except KeyError:
            return 'unavailable'

    def __percent_changed(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            change = float(self.data['regularMarketChangePercent'].to_string(index=False))
            return float("{:.2f}".format(change))
        except KeyError:
            return 'unavailable'

    def __change(self):
        # if ticker data is unavailable
        if self.is_valid is False:
            return 'unavailable'

        try:
            change = float(self.data['regularMarketChange'].to_string(index=False))
            return float("{:.2f}".format(change))
        except KeyError:
            return 'unavailable'

    def get_dividend_summary(self, start, end=0):
        df = get_data(BotConfig().dividend_url, self.ticker)
        a = []

        if end == 0:
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
        return 'Name:' + self.name + ' (' + self.ticker + ')\nLatest price: ' + str(
            self.price) + '\nMarket Cap: ' + str(
            self.market_cap) + '\nBook Value Per Share (MRQ): SGD' + str(self.book_value)
