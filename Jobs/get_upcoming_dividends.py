import pandas as pd
import requests
from Kubera.share import Share
import pickle
import telegram.ext
from config import BotConfig
from db_engine import DBEngine
from pandas.util import hash_pandas_object


def get_upcoming_dividends(context: telegram.ext.CallbackContext):
    page = requests.get(BotConfig().upcoming_dividends_url).text
    df = pd.read_html(page)[0]
    hash_value = hash_pandas_object(df).sum()
    # hash check
    try:
        with open('hash.pickle', 'rb') as hash_file:
            b = pickle.load(hash_file)
        # check if latest hash value matches with old one
        if b == hash_value:
            return
        else:
            # update hash value in the local file
            with open('hash.pickle', 'wb') as hash_file:
                pickle.dump(hash_value, hash_file)
    # no hash file found
    except FileNotFoundError:
        with open('hash.pickle', 'wb') as hash_file:
            pickle.dump(hash_value, hash_file)

    df.columns = df.columns.str.replace(' ', '')
    db = DBEngine()
    db.clear_table('dividends')

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

        db.add_item('dividends', ['name', 'ticker', 'market_cap', 'price', 'payout', 'yield', 'date'],
                    [name, ticker, market_cap, price, payout, yield_value, date])

