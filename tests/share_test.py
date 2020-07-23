from Kubera.share import Share
import pandas as pd


def main():
    share = Share('qwac')

    a = share.get_dividend_summary(2020, 2015)
    s = ''

    if share.is_valid is False:
        print('invalid ticker')

    if a is None:
        print('Dividend data not available')
        return

    for item in a:
        s += str(item.year) + ' (' + str(item.total) + ')' + '\n'
        i = 1
        for pay_date, pay_amount in zip(item.pay_date, item.amount):
            if pay_amount is '-':
                continue
            s += '‣ ' + pd.to_datetime(pay_date).strftime('%d %B') + ': ' + str(pay_amount).replace('SGD', 'SGD ') + '\n'
            i += 1
        s += '\n'
    print(s)
    # s.get_data(2019)
    # s.get_dividend_breakdown(2019)
    # dividends = s.get_dividend_payout(datetime.datetime.now().year, datetime.datetime.now().year - 5)

    # for key, value in dividends.items():
    #     print(key, value)


main()
