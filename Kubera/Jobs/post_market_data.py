import time

import telegram.ext
from telegram import TelegramError

from Model.db import DBEngine
from Model.share import Share
from Utils.logging import get_logger as log


def post_market_data(context: telegram.ext.CallbackContext):
    # connect to database
    log().info('post market data job started')
    total_users = 0
    tickers = []
    user_id = 0
    db = DBEngine()
    row = db.custom_command('SELECT DISTINCT id FROM watchlist')
    # for each id
    for r in row:
        s = 'Here is your watchlist update for today:\n\n'
        user_id = r[0]

        rowx = db.custom_command('SELECT ticker FROM watchlist WHERE id=' + str(user_id))
        # for each ticker that belongs to the user
        for x in rowx:
            tickers.append(x[0])
        # print(tickers)
        for ticker in tickers:
            share = Share(ticker)
            s += '<b>' + share.name + ' (' + share.ticker + ')</b>\nOpen: ' + str(share.open) + \
                 '\nLow: ' + str(share.low) + '\nHigh: ' + str(share.high) + \
                 '\nClose: ' + str(share.price) + '\nPrev Close: ' + \
                 str(share.previous_close) + '\n50MA: ' + str(share.fifty_day_ma) + \
                 '\nVolume: ' + str(share.volume)+'\n\n'
        try:
            context.bot.send_message(chat_id=user_id, text=s, parse_mode='HTML')
            total_users += 1
            tickers.clear()
            time.sleep(1)
        except TelegramError:
            tickers.clear()
            continue

    log().info('market data sent to ' + str(total_users) + ' users')
