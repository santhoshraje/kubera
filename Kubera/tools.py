import pandas as pd
import requests
from Kubera.share import Share


def get_upcoming_dividends():
    array = []
    url = "https://www.dividends.sg/dividend/coming"
    html = requests.get(url).text
    df = pd.read_html(html)[0]
    tickers = df['Ticker'].tolist()
    for ticker in tickers:
        share = Share(ticker)
        share.get_upcoming_dividends()
        array.append(share)
    return array
