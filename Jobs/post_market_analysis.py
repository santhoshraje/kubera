import telegram.ext
from telegram import TelegramError

from db_engine import DBEngine
from Kubera.share import Share
from millify import millify
import time
from datetime import datetime


def post_market_analysis(context: telegram.ext.CallbackContext):
    # connect to database
    db = DBEngine('test.sqlite')
    # fetch tickers
    tickers = db.get_items('stocks', 'ticker')
    # get volumes
    for ticker in tickers:
        share = Share(ticker[0])
        # ignore tickers with missing volume information
        if share.volume is 'unavailable':
            continue
        # update ticker with latest volume information
        db.update_item('stocks', 'volume', share.volume, 'ticker', ticker[0])
        time.sleep(1)

    # get top 5 results from database sorted in desc order
    rows = db.custom_command('select ticker, volume from stocks order by volume desc limit 5')
    # create string
    s = '<b> Post market analysis for ' + datetime.today().strftime('%d %B %Y') + '</b>\n\n'
    s += '<b>STI overall change: </b>' + Share('^STI').percent_changed + '\n\n'
    s += '<b>Top 5 volume stocks\n\n</b>'

    for idx, row in enumerate(rows):
        s += str(idx + 1) + '. ' + Share(row[0]).name + '(' + Share(row[0]).ticker + ')' + ' [' + str(millify(row[1])) + '] \n'

    # send message to all users
    for user in DBEngine().get_items():
        try:
            context.bot.send_message(chat_id=user, text=s, parse_mode='HTML')
            time.sleep(1)
        except TelegramError as e:
            DBEngine().delete_item(user)
            continue
