import telegram.ext
from telegram import TelegramError

from db_engine import DBEngine
from Kubera.share import Share
from millify import millify
import time
from datetime import datetime


def post_market_analysis(context: telegram.ext.CallbackContext):
    # connect to database
    db = DBEngine()
    # fetch tickers
    tickers = db.get_items('stocks', 'ticker')
    # update values
    for ticker in tickers:
        share = Share(ticker[0])
        # ignore tickers with missing volume information
        if share.volume == 'unavailable':
            continue
        # add volume to database
        db.update_item('stocks', 'volume', share.volume, 'ticker', ticker[0])
        # add company name to database
        db.update_item('stocks', 'name', share.name, 'ticker', ticker[0])
        # add change % to database
        db.update_item('stocks', 'change', share.change, 'ticker', ticker[0])
        time.sleep(1)

    # get top 5 results from database sorted
    volume = db.custom_command('select name, volume from stocks order by volume desc limit 5')
    gainers = db.custom_command('select name from stocks order by change desc limit 5')
    losers = db.custom_command('select name from stocks order by change asc limit 5')

    # STI change
    sti_change_raw = Share('^STI').percent_changed
    # append '%'
    sti_change = str(sti_change_raw) + '%'
    # prepend '+' if the value is positive
    if sti_change_raw > 0:
        sti_change = '+' + sti_change

    # create string
    s = '<b>Market Statistics (' + datetime.today().strftime('%d %B %Y') + ')</b>\n\n'
    s += '<b>STI overall change: </b>' + sti_change + '\n\n'
    s += '<b>Highest volumes:</b>\n'

    for idx, row in enumerate(volume):
        s += '‣ ' + row[0] + ' (' + str(millify(row[1])) + ')\n'

    s += '\n'
    s += '<b>Top gainers:</b>\n'

    for idx, row in enumerate(gainers):
        s += '‣ ' + row[0] + '\n'

    s += '\n'
    s += '<b>Top losers:</b>\n'

    for idx, row in enumerate(losers):
        s += '‣ ' + row[0] + '\n'

    # send message to all users
    for user in DBEngine().get_items('users', 'id'):
        try:
            context.bot.send_message(chat_id=user, text=s, parse_mode='HTML')
            time.sleep(1)
        except TelegramError:
            DBEngine().delete_item(user)
            continue
