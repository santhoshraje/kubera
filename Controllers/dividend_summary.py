from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

from Kubera.share import Share

import Controllers.states as states

from Utils.logging import get_logger as log

GETSUMMARY = range(1)


class DSController:
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

    def get_ticker(self, update, context):
        user = update.effective_user
        log().info("User %s pressed the dividend summary button.", user.id)
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Enter ticker symbol (e.g D05)")
        return GETSUMMARY

    def get_dividend_summary(self, update, context):
        ticker = update.message.text
        user = update.effective_user
        log().info("User %s entered ticker value %s.", user.id, ticker)
        try:
            share = Share(ticker)
        except AttributeError:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            log().info("User %s entered and invalid ticker value %s.", user.id, ticker)

            return ConversationHandler.END
        year_1 = share.get_total_dividend_payout(2019, 1)
        year_2 = share.get_total_dividend_payout(2018, 1)
        year_3 = share.get_total_dividend_payout(2017, 1)
        year_4 = share.get_total_dividend_payout(2016, 1)
        year_5 = share.get_total_dividend_payout(2015, 1)

        update.message.reply_text('<b>' + share.name + '</b>\n\n<b>2019</b>: ' + str(year_1) + '\n\n<b>2018</b>: ' +
                                  str(year_2) + '\n\n<b>2017</b>: ' + str(year_3) + '\n\n<b>2016</b>: ' + str(year_4) +
                                  '\n\n<b>2015</b>: ' + str(year_5) + '\n\n use /start to go back to the main menu'
                                  , parse_mode='HTML')
        return ConversationHandler.END
