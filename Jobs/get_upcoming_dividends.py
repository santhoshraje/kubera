import pandas as pd
import requests
from Kubera.share import Share
import pickle
import numpy as np
import telegram.ext


def get_upcoming_dividends(context: telegram.ext.CallbackContext):
    array = []
    url = "https://www.dividends.sg/dividend/coming"
    html = requests.get(url).text
    df = pd.read_html(html)[0]

    tickers = df['Ticker'].tolist()

    for ticker in tickers:
        try:
            share = Share(ticker)
        except AttributeError:
            continue
        share.get_upcoming_dividends()
        array.append(share)

    tmp = np.array_split(array, 5)
    file_count = 1
    for x in tmp:
        f = open("Logs/upcoming" + str(file_count) + ".pickle", 'wb')
        pickle.dump(x, f)
        f.close()
        file_count += 1
