import time

import Kubera.Controllers.global_states as states

from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler

import pickle

from Kubera.Utils.logging import get_logger as log


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
            tmp += '<b>' + a.name.lstrip() + ' (' + a.ticker + ')</b>\n‣ Market Cap: ' + str(a.market_cap) \
                    + '\n‣ BVPS (MRQ): ' + str(a.book_value) + '\n‣ Price: ' + str(a.price) + \
                    '\n‣ Amount: ' + str(a.payout_amount) + '\n‣ Yield: ' + a.yield_data + '\n‣ Date: ' + a.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for b in array_2:
            tmp += '<b>' + b.name.lstrip() + ' (' + str(b.ticker) + ')</b>\n‣ Market cap: ' + str(b.market_cap) \
                    + '\n‣ Book value: ' + str(b.book_value) + '\n‣ Price: ' + str(b.price) + \
                    '\n‣ Amount: ' + str(b.payout_amount) + '\n‣ Yield: ' + b.yield_data + '\n‣ Date: ' + b.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for c in array_3:
            tmp += '<b>' + c.name.lstrip() + ' (' + str(c.ticker) + ')</b>\n‣ Market cap: ' + str(c.market_cap) \
                    + '\n‣ Book value: ' + str(c.book_value) + '\n‣ Price:' + str(c.price) + \
                    '\n‣ Amount: ' + str(c.payout_amount) + '\n‣ Yield: ' + c.yield_data + '\n‣ Date: ' + c.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for d in array_4:
            tmp += '<b>' + d.name.lstrip() + ' (' + str(d.ticker) + ')</b>\n‣ Market cap: ' + str(d.market_cap) \
                    + '\n‣ Book value: ' + str(d.book_value) + '\n‣ Price: ' + str(d.price) + \
                    '\n‣ Amount: ' + str(d.payout_amount) + '\n‣ Yield: ' + d.yield_data + '\n‣ Date: ' + d.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)
        time.sleep(0.5)

        tmp = ''
        for e in array_5:
            tmp += '<b>' + e.name.lstrip() + ' (' + str(e.ticker) + ')</b>\n‣ Market cap: ' + str(e.market_cap) \
                    + '\n‣ Book value: ' + str(e.book_value) + '\n‣ Price: ' + str(e.price) + \
                    '\n‣ Amount: ' + str(e.payout_amount) + '\n‣ Yield: ' + e.yield_data + '\n‣ Date: ' + e.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        return ConversationHandler.END
