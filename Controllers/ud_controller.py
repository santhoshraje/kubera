import Controllers.states as states

from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler

import requests
import pandas as pd

from Kubera.share import Share


class UDController:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        ud_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(
                self.get_upcoming_dividends, pattern='^' + str(states.DIVIDENDUP) + '$')],
            states={
            },
            fallbacks=[]
        )
        self.__dp.add_handler(ud_handler)

    @staticmethod
    def get_upcoming_dividends(update, context):
        message = ''
        query = update.callback_query
        query.answer()
        query.edit_message_text(text='Fetching data. Please wait.')

        url = "https://www.dividends.sg/dividend/coming"
        html = requests.get(url).text
        df = pd.read_html(html)[0]

        tickers = df['Ticker'].tolist()

        for ticker in tickers:
            try:
                x = Share(ticker)
            except AttributeError as e:
                print(ticker + 'has no yahoo data' + str(e))
                continue

            x.get_upcoming_dividends()
            message += '<b>' + x.name + ' (' + x.ticker_raw + ')</b>\nMarket Cap: ' + \
                       x.market_cap + '\nBook Value: ' + x.book_value + '\nLatest price: ' + x.price + \
                       '\nPayout amount: ' + x.payout_amount + '\nPayout date: ' + x.payout_date + '\n\n'
            context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=message, parse_mode='html',
                                     silent=True)
            message = ''

        return ConversationHandler.END
