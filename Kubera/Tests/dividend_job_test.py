import pickle
import time
import pandas as pd
import requests
import numpy as np
# to resolve path issues
import sys
sys.path.append("/Users/santhosh/Documents/projects/kubera/Kubera")
from Model.db import DBEngine
from Model.share import Share
from Bot.config import BotConfig
import telegram.ext
from telegram import TelegramError


def main(): 
    array = []
    user_ticker_dict = {}
    ticker_payout_dict = {}

    url = BotConfig().upcoming_dividends_url
    html = requests.get(url).text
    df = pd.read_html(html)[0]
    df.columns = df.columns.str.replace(' ', '')

    # get tickers from upcoming dividends page
    tickers = df['Ticker'].tolist()

    # DBEngine().add_item('dividends','ticker','V03')
    # DBEngine().add_item('dividends','ticker','D05')

    if tickers.empty:
        return
    
    for ticker in tickers:
        # check if ticker is in database
        try:
            # select everything from watchlist table
            db = DBEngine()
            row = db.custom_command('SELECT id FROM watchlist where ticker="' + ticker + '"')
            # build a dictionary of which user has which ticker
            for r in row:
                if ticker in user_ticker_dict:
                    user_ticker_dict[ticker].append(r[0])
                else:
                    user_ticker_dict[ticker] = [r[0]]
        # ticker not found. no user has this ticker
        except:
            continue



    for ticker in user_ticker_dict:
        # get share object
        share = Share(ticker)
        # ticker = 'v03'
        # check if share is valid
        if not share.is_valid:
            continue

        payout_amount = df.loc[df.Ticker == ticker, 'Amount'].values
        # add payout amount to dictionary
        ticker_payout_dict[ticker] = payout_amount
        # print(type(payout_amounts))
    
    # print(ticker_payout_dict)
    s = ''
    for ticker in user_ticker_dict:
        s+= '<b>' + ticker + '</b>\n'
        for v in ticker_payout_dict[ticker]:
            s+= str(v) + '\n'
        users = user_ticker_dict.get(ticker)
        for user in users:
            try:
                # context.bot.send_message(chat_id=user, text=s, parse_mode='HTML')
                # print(user)
                continue
            except TelegramError:
                continue
            s = ''
            time.sleep(1)


            # print(type(x))
            # print(x[0])
            # print(type(x[0]))

        # share.payout_date = pd.to_datetime(str(df.loc[df.Ticker == ticker, 'NextDividend'].values[0])).strftime(
        #     '%d %B %Y')
        # print(share.payout_amount)
        # share.yield_data = str(df.loc[df.Ticker == ticker, 'Yield'].values[0])






  




    
    # print(tickers)

    # for ticker in tickers:
    #     share = Share(ticker)
    #     if not share.is_valid:
    #         continue

    #     share.payout_amount = str(df.loc[df.Ticker == ticker, 'Amount'].values[0])
    #     share.payout_date = pd.to_datetime(str(df.loc[df.Ticker == ticker, 'NextDividend'].values[0])).strftime(
    #         '%d %B %Y')
    #     share.yield_data = str(df.loc[df.Ticker == ticker, 'Yield'].values[0])
    #     # print(str(df.loc[df.Ticker == ticker, 'Amount']))
    #     # print(share.payout_amount)
    #     print(share.get_dividend_summary(2019))
    #     array.append(share)
    #     break

    # for x in array:
    #     print(x.ticker,x.payout_date)

    # tmp = np.array_split(array, 5)
    # file_count = 1

    # for x in tmp:
    #     f = open("upcoming" + str(file_count) + ".pickle", 'wb')
    #     pickle.dump(x, f)
    #     f.close()
    #     file_count += 1


main()
