from datetime import datetime

from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
import Controllers.global_states as states
from Kubera.share import Share
from Utils.logging import get_logger as log

GETANALYSIS = range(1)


class StockAnalysis:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        handler = ConversationHandler(
            entry_points=[
                CallbackQueryHandler(self.__start, pattern='^' + str(states.ANALYSIS) + '$')
            ],
            states={
                GETANALYSIS: [
                    MessageHandler(Filters.text, self.__get_analysis)
                ],
            },
            fallbacks=[]
        )
        self.__dp.add_handler(handler)

    def __start(self, update, context):
        user = update.effective_user
        log().info("User %s pressed the stock analysis button.", user.first_name)
        user = update.effective_user
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Enter ticker symbol (e.g D05)")
        return GETANALYSIS

    def __get_analysis(self, update, context):
        ticker = update.message.text
        user = update.effective_user
        log().info("User %s entered ticker value %s.", user.first_name, ticker)

        share = Share(ticker)

        if not share.is_valid:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            log().info("User %s entered an invalid ticker value %s.", user.first_name, ticker)
            return ConversationHandler.END

        s = ''
        s += '<b>' + share.name + ' (' + share.ticker + ') Technical Analysis Report (' + str(
            datetime.now().date().strftime('%d %B %Y')) + ')</b>' + '\n\n'
        s += '<b>Indicators</b>\n\n‣ 50 MA: ' + str(share.fifty_day_ma) + '\n'
        s += '‣ 200 MA: ' + str(share.two_hundred_day_ma) + '\n'
        s += '\n<b>Possible trading strategies</b>\n\n'
        s += '<b>Golden Cross strategy</b>\n'
        if share.fifty_day_ma > share.two_hundred_day_ma:
            s += '‣ 50 Day MA is currently above 200 day MA'
        else:
            s += '‣ 50 Day MA is currently below 200 day MA'

        s += '\n\n<b>Price Crossover strategy</b>\n'

        if share.price > share.fifty_day_ma:
            s += '‣ Share price is currently above 50 MA\n'
        else:
            s += '‣ Share price is currently below 50 MA\n'

        if share.price > share.two_hundred_day_ma:
            s += '‣ Share price is currently above 200 MA\n'
        else:
            s += '‣ Share price is currently below 200 MA\n'

        update.message.reply_text(s, parse_mode='HTML')
        return ConversationHandler.END
