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
        query.edit_message_text(text='Generating data...')

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
            tmp += '<b>' + a.name.lstrip() + ' (' + a.ticker_raw + ')</b>\nMarket Cap: ' + a.market_cap \
                    + '\nBVPS (MRQ): ' + a.book_value + '\nPrice: ' + a.price + \
                    '\nAmount: ' + str(a.payout_amount) + '\nYield: ' + a.yield_data + '\nDate: ' + a.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        tmp = ''
        for b in array_2:
            tmp += '<b>' + b.name.lstrip() + ' (' + b.ticker_raw + ')</b>\nMarket Cap: ' + b.market_cap \
                    + '\nBVPS (MRQ): ' + b.book_value + '\nPrice: ' + b.price + \
                    '\nAmount: ' + str(b.payout_amount) + '\nYield: ' + b.yield_data + '\nDate: ' + b.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        tmp = ''
        for c in array_3:
            tmp += '<b>' + c.name.lstrip() + ' (' + c.ticker_raw + ')</b>\nMarket Cap: ' + c.market_cap \
                    + '\nBVPS (MRQ): ' + c.book_value + '\nPrice: ' + c.price + \
                    '\nAmount: ' + str(c.payout_amount) + '\nYield: ' + c.yield_data + '\nDate: ' + c.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        tmp = ''
        for d in array_4:
            tmp += '<b>' + d.name.lstrip() + ' (' + d.ticker_raw + ')</b>\nMarket Cap: ' + d.market_cap \
                    + '\nBVPS (MRQ): ' + d.book_value + '\nPrice: ' + d.price + \
                    '\nAmount: ' + str(d.payout_amount) + '\nYield: ' + d.yield_data + '\nDate: ' + d.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        tmp = ''
        for e in array_5:
            tmp += '<b>' + e.name.lstrip() + ' (' + e.ticker_raw + ')</b>\nMarket Cap: ' + e.market_cap \
                    + '\nBVPS (MRQ): ' + e.book_value + '\nPrice: ' + e.price + \
                    '\nAmount: ' + str(e.payout_amount) + '\nYield: ' + e.yield_data + '\nDate: ' + e.payout_date + '\n\n'
        context.bot.send_message(chat_id=update.callback_query.message.chat.id, text=tmp, parse_mode='html', silent=True)

        return ConversationHandler.END
