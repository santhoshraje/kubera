import pandas as pd


class DividendSummary:
    def __init__(self, year, total, amount, ex_date, pay_date):
        # single values
        self.year = year
        self.total = total
        # lists
        self.amount = amount
        self.ex_date = ex_date
        self.pay_date = pay_date

    def __str__(self):
        s = ''
        s += str(self.year) + ' (' + str(self.total) + ')' + '\n'
        i = 1
        for pay_date, pay_amount in zip(self.pay_date, self.amount):
            if pay_date is '-':
                continue
            s += '‣ ' + pd.to_datetime(pay_date).strftime('%d %B') + ': ' + str(pay_amount).replace('SGD',
                                                                                                    'SGD ') + '\n'
            i += 1
        return s
