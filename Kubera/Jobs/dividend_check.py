import os
import time
import requests
import telegram.ext
from telegram import TelegramError
from Bot.config import BotConfig

from Model.db import DBEngine
from Model.share import Share
from Utils.logging import get_logger as log
import pandas as pd
import pickle


def check_dividend(context: telegram.ext.CallbackContext):
    # connect to database
    log().info('🔵 Running check_dividend job')

    user_ticker_dict = {}
    ticker_payout_dict = {}

    url = BotConfig().upcoming_dividends_url
    html = requests.get(url).text
    df = pd.read_html(html)[0]
    df.columns = df.columns.str.replace(' ', '')

    # get tickers from upcoming dividends page
    tickers = df['Ticker'].tolist()

    # check against database for notified tickers
    notified_tickers = DBEngine().get_items('dividends', 'ticker')
    for r in notified_tickers:
        if r[0] in tickers:
            tickers.remove(r[0])

    
    for ticker in tickers:
        # check if ticker is in database
        try:
            # select everything from watchlist table
            row = DBEngine().custom_command('SELECT id FROM watchlist where ticker="' + ticker + '"')
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
        # check if share is valid
        if not share.is_valid:
            continue

        payout_amount = df.loc[df.Ticker == ticker, 'Amount'].values
        # add payout amount to dictionary
        ticker_payout_dict[ticker] = payout_amount
        # print(type(payout_amounts))
    
    for ticker in user_ticker_dict:
        s = 'Dividend announced for '
        payout_amount = ''
        # get payout date
        payout_date = pd.to_datetime(str(df.loc[df.Ticker == ticker, 'NextDividend'].values[0])).strftime('%d %B %Y')
        
        s+= '<b>' + Share(ticker).name + '</b>\n\nAmount:\n'
        
        for v in ticker_payout_dict[ticker]:
            s+= str(v) + '\n'
            payout_amount += str(v) + '\n'
        s+= '\nPayment on ' + payout_date + '\n\n'
        # add item to database
        DBEngine().add_item('dividends', ['ticker', 'amount', 'date'], [ticker, payout_amount, payout_date])
        # send message to each user
        users = user_ticker_dict.get(ticker)
        for user in users:
            try:
                context.bot.send_message(chat_id=user, text=s, parse_mode='HTML')
            except TelegramError:
                continue
            time.sleep(1)
