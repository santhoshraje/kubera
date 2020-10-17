import pandas as pd
import requests
from Kubera.share import Share
import pickle
import numpy as np
import telegram.ext
from config import BotConfig
from db_engine import DBEngine


def get_upcoming_dividends(context: telegram.ext.CallbackContext):
    url = BotConfig().upcoming_dividends_url
    html = requests.get(url).text
    df = pd.read_html(html)[0]
    df.columns = df.columns.str.replace(' ', '')
    db = DBEngine()

    tickers = df['Ticker'].tolist()

    for ticker in tickers:
        share = Share(ticker)
        if not share.is_valid:
            continue
        name = share.name
        ticker = share.ticker
        market_cap = share.market_cap
        price = str(share.price)
        payout = str(df.loc[df.Ticker == ticker, 'Amount'].values[0])
        date = pd.to_datetime(str(df.loc[df.Ticker == ticker, 'NextDividend'].values[0])).strftime('%d %B %Y')
        yield_value = str(df.loc[df.Ticker == ticker, 'Yield'].values[0])
        db.add_item('dividends', ['name', 'ticker', 'market_cap', 'price', 'payout', 'yield', 'date'], [name, ticker, market_cap, price, payout, yield_value, date])

