from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

from Kubera.share import Share
import Controllers.global_states as states
from Utils.logging import get_logger as log
import pandas as pd
import datetime

GETSUMMARY = range(1)


class DividendSummary:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        ds_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(
                self.get_ticker, pattern='^' + str(states.DIVIDENDINFO) + '$')],
            states={
                GETSUMMARY: [
                    MessageHandler(Filters.text, self.get_dividend_summary)
                ],
            },
            fallbacks=[]
        )
        self.__dp.add_handler(ds_handler)

    @staticmethod
    def get_ticker(update, context):
        user = update.effective_user
        log().info("User %s pressed the dividend summary button.", user.first_name)
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Enter ticker symbol (e.g D05)")
        return GETSUMMARY

    @staticmethod
    def get_dividend_summary(update, context):
        ticker = update.message.text
        user = update.effective_user
        log().info("User %s entered ticker value %s.", user.first_name, ticker)

        years = 5

        share = Share(ticker)

        if not share.is_valid:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            log().info("User %s entered an invalid ticker value %s.", user.first_name, ticker)
            return ConversationHandler.END

        a = share.get_dividend_summary(datetime.datetime.now().year, datetime.datetime.now().year - years)
        s = '<b>' + share.name + '</b>\n\n'

        for item in a:
            s += '<b>' + str(item.year) + ' (' + str(item.total) + ')</b>' + '\n'
            i = 1
            for pay_date, pay_amount in zip(item.pay_date, item.amount):
                if pay_date == '-':
                    continue
                s += '‣ ' + pd.to_datetime(pay_date).strftime('%d %B') + ': ' + str(pay_amount).replace('SGD', 'SGD ') +'\n'
                i += 1
            s += '\n'

        update.message.reply_text(s, parse_mode='HTML')
        return ConversationHandler.END
