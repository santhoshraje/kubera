import pandas as pd
import requests
from Kubera.share import Share
import pickle
import numpy as np

from config import BotConfig


def main():
    array = []
    url = BotConfig().upcoming_dividends_url
    html = requests.get(url).text
    df = pd.read_html(html)[0]
    df.columns = df.columns.str.replace(' ', '')

    tickers = df['Ticker'].tolist()

    for ticker in tickers:
        share = Share(ticker)
        print(share.name)
        if not share.is_valid:
            continue
        share.payout_amount = str(df.loc[df.Ticker == ticker, 'Amount'].values[0])
        share.payout_date = pd.to_datetime(str(df.loc[df.Ticker == ticker, 'NextDividend'].values[0])).strftime(
            '%d %B %Y')
        share.yield_data = str(df.loc[df.Ticker == ticker, 'Yield'].values[0])
        array.append(share)

    tmp = np.array_split(array, 5)
    file_count = 1

    for x in tmp:
        f = open("upcoming" + str(file_count) + ".pickle", 'wb')
        pickle.dump(x, f)
        f.close()
        file_count += 1


main()
