import pandas as pd
import requests


def get_data(url, ticker):
    """
    Given a url, pull data from that url and return it
    as a dataframe
    :param url: url to get data from
    :param ticker: stock ticker
    :return: pandas dataframe
    """
    url = url + ticker
    html = requests.get(url).text
    try:
        df = pd.read_html(html)[0]
    except ValueError:
        return None
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    df.columns = df.columns.str.replace(' ', '')
    return df
