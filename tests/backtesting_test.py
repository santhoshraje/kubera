import datetime
import time

import yfinance as yf


def main():
        period = 29
        # start = datetime.datetime.now().date() - datetime.timedelta(days=59)
        # end = datetime.datetime.now().date()
        i = period

        while i > 0:
            d = datetime.datetime.now().date() - datetime.timedelta(days=i)
            print('Now processing: ' + str(d) + '\n')
            # get 10 day sma for this date
            sma_start = d - datetime.timedelta(days=10)
            sma_end = d

            sma_data = yf.download(
                start = sma_start,
                end = sma_end,
                tickers="",
                interval="1d",
                auto_adjust=True,
                threads=True,
            )['Close'].to_list()

            # get tick data
            tick_data = yf.download(
                start = d,
                end = d + datetime.timedelta(days=1),
                tickers="",
                interval="1m",
                auto_adjust=True,
                threads=True,
            )['Close'].to_list()

            sma = sum(sma_data)/len(sma_data)
            print('SMA for period: ' + str(sma_start) + ' to ' + str(sma_end) + ': ' + str(sma))

            win = 0
            cross = 0
            for index, tick in enumerate(tick_data):

                if tick == sma:
                    cross += 1
                    # print('PRICE ABOVE SMA')
                    # print('SMA DIFFERENCE: +' + str(tick - sma))
                    try:
                        if tick_data[index + 1] > tick:
                            # print('SMA: ' + str(sma))
                            # print('tick data: ' + str(tick))
                            # print('tick_data+1: ' + str(tick_data[index + 1]))
                            win += 1
                    except IndexError as e:
                        print(e)
                # else:
                    # print('PRICE BELOW SMA')
                    # print('SMA DIFFERENCE: -' + str(sma - tick))

            print('Number of times price crossed SMA : ' + str(cross))
            print('Number of times price crossed SMA and increased: ' + str(win))
            i-=1
            time.sleep(1)



    # n = yf.download(
    #     start = datetime.datetime.now().date() - datetime.timedelta(days=59),
    #     end = datetime.datetime.now().date(),
    #     tickers="",
    #     interval="5m",
    #     auto_adjust=True,
    #     threads=True,
    # )
    #
    # m = yf.download(
    #     start = datetime.datetime.now().date() - datetime.timedelta(days=59),
    #     end = datetime.datetime.now().date(),
    #     tickers="",
    #     interval="1d",
    #     auto_adjust=True,
    #     threads=True,
    # )
    # print(n)


    # z = yf.download(
    #     start = datetime.datetime.now().date() - datetime.timedelta(days=7),
    #     end = datetime.datetime.now().date(),
    #     tickers="",
    #     interval="1d",
    #     auto_adjust=True,
    #     threads=True,
    # )['Close'].to_list()



    # count = 0
    # ten_day_sma = sum(m)/len(m)
    # five_day_sma = sum(z)/len(z)
    # for val in n:
    #     if val > ten_day_sma:
    #         count += 1
    # print(count)
    # print(len(n))

    # print('10 Day SMA: ' + str(sum(m)/len(m)))




main()
