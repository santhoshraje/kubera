import time

import Controllers.global_states as states

from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler

import pickle

from Utils.logging import get_logger as log


class UpcomingDividends:
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
        user = update.effective_user
        log().info("User %s pressed the upcoming dividends button.", user.first_name)
        query = update.callback_query
        query.answer()
        # query.edit_message_text(text='Fetching data...')

        f = open("Logs/upcoming1.pickle", "rb")
        array_1 = pickle.load(f)
        f.close()

        f = open("Logs/upcoming2.pickle", "rb")
        array_2 = pickle.load(f)
        f.close()

        f = open("Logs/upcoming3.pickle", "rb")
        array_3 = pickle.load(f)
        f.close()

        f = open("Logs/upcoming4.pickle", "rb")
        array_4 = pickle.load(f)
        f.close()

        f = open("Logs/upcoming5.pickle", "rb")
        array_5 = pickle.load(f)
        f.close()

        tmp = ''
        for a in array_1:
            tmp += '<b>' + a.name.lstrip() + ' (' + a.ticker_raw + ')</b>\n‣ Market Cap: ' + a.market_cap \
                    + '\n‣ BVPS (MRQ): ' + a.book_value + '\n‣ Price: ' + a.price + \
                    '\n‣ Amount: ' + str(a.payout_amount) + '\n‣ Yield: ' + a.yield_data + '\n‣ Date: ' + a.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for b in array_2:
            tmp += '<b>' + b.name.lstrip() + ' (' + b.ticker_raw + ')</b>\n‣ Market cap: ' + b.market_cap \
                    + '\n‣ Book value: ' + b.book_value + '\n‣ Price: ' + b.price + \
                    '\n‣ Amount: ' + str(b.payout_amount) + '\n‣ Yield: ' + b.yield_data + '\n‣ Date: ' + b.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for c in array_3:
            tmp += '<b>' + c.name.lstrip() + ' (' + c.ticker_raw + ')</b>\n‣ Market cap: ' + c.market_cap \
                    + '\n‣ Book value: ' + c.book_value + '\n‣ Price:' + c.price + \
                    '\n‣ Amount: ' + str(c.payout_amount) + '\n‣ Yield: ' + c.yield_data + '\n‣ Date: ' + c.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for d in array_4:
            tmp += '<b>' + d.name.lstrip() + ' (' + d.ticker_raw + ')</b>\n‣ Market cap: ' + d.market_cap \
                    + '\n‣ Book value: ' + d.book_value + '\n‣ Price: ' + d.price + \
                    '\n‣ Amount: ' + str(d.payout_amount) + '\n‣ Yield: ' + d.yield_data + '\n‣ Date: ' + d.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for e in array_5:
            tmp += '<b>' + e.name.lstrip() + ' (' + e.ticker_raw + ')</b>\n‣ Market cap: ' + e.market_cap \
                    + '\n‣ Book value: ' + e.book_value + '\n‣ Price: ' + e.price + \
                    '\n‣ Amount: ' + str(e.payout_amount) + '\n‣ Yield: ' + e.yield_data + '\n‣ Date: ' + e.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        return ConversationHandler.END
