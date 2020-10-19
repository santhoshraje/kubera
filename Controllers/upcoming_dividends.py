import Controllers.global_states as states
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from Utils.logging import get_logger as log
from db_engine import DBEngine
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from datetime import datetime, timedelta

YES, NO, OPTIONS, THIRTY, SIXTY, NINETY, SHOWOPTIONS, BACKTOMENU = range(8)


class UpcomingDividends:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__db = DBEngine()

    def __handler(self):
        ud_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(
                self.show_confirmation, pattern='^' + str(states.DIVIDENDUP) + '$')],
            states={
                SHOWOPTIONS: [
                    CallbackQueryHandler(self.show_options, pattern='^' + str(YES) + '$'),
                    CallbackQueryHandler(self.show_options, pattern='^' + str(BACKTOMENU) + '$'),
                ],
                OPTIONS: [
                    CallbackQueryHandler(self.thirty_days, pattern='^' + str(THIRTY) + '$'),
                    CallbackQueryHandler(self.sixty_days, pattern='^' + str(SIXTY) + '$'),
                    CallbackQueryHandler(self.ninety_days, pattern='^' + str(NINETY) + '$'),
                ],

            },
            fallbacks=[]
        )
        self.__dp.add_handler(ud_handler)

    def show_confirmation(self, update, context):
        query = update.callback_query
        query.answer()
        keyboard = [
            [InlineKeyboardButton("Yes, show me",
                                  callback_data=str(YES))],
            [InlineKeyboardButton("No, take me back",
                                  callback_data=str(NO))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="I can show you upcoming dividend payouts from SGX listed companies", reply_markup=reply_markup)
        return SHOWOPTIONS

    def show_options(self, update, context):
        query = update.callback_query
        query.answer()
        keyboard = [
            [InlineKeyboardButton("Next 30 days",
                                  callback_data=str(THIRTY))],
            [InlineKeyboardButton("Next 60 days",
                                  callback_data=str(SIXTY))],
            [InlineKeyboardButton("Next 90 days",
                                  callback_data=str(NINETY))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="What time period would you like to see?", reply_markup=reply_markup)
        return OPTIONS

    def thirty_days(self, update, context):
        query = update.callback_query
        query.answer()
        rows = self.__db.get_items('dividends', '*')
        tmp = ''
        period = datetime.now().date() + timedelta(days=30)
        max_message_size = 4096
        message_array = []
        for row in rows:
            if datetime.strptime(row[6], '%d %B %Y').date() < period:
                n = '<b>' + row[0].lstrip() + ' (' + row[1] + ')</b>\n‣ Market Cap: ' + row[2] \
                        + '\n‣ Price: ' + row[3] + \
                        '\n‣ Amount: ' + row[4] + '\n‣ Yield: ' + row[5] + '\n‣ Date: ' + row[6] + '\n\n'
                if len(tmp) + len(n) <= max_message_size:
                    tmp += n
                else:
                    message_array.append(tmp)
                    tmp = ''
        if not message_array:
            message_array.append(tmp)

        keyboard = [
            [InlineKeyboardButton("Back",
                                  callback_data=str(YES))],
            # [InlineKeyboardButton("Back to main menu",
            #                       callback_data=str(BACKTOMENU))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for message in message_array:
            query.edit_message_text(text=message, parse_mode='html', silent=True, reply_markup=reply_markup)
        return SHOWOPTIONS

    def sixty_days(self, update, context):
        query = update.callback_query
        query.answer()
        rows = self.__db.get_items('dividends', '*')
        tmp = ''
        period = datetime.now().date() + timedelta(days=60)
        max_message_size = 4096
        message_array = []
        for row in rows:
            if datetime.strptime(row[6], '%d %B %Y').date() < period:
                n = '<b>' + row[0].lstrip() + ' (' + row[1] + ')</b>\n‣ Market Cap: ' + row[2] \
                    + '\n‣ Price: ' + row[3] + \
                    '\n‣ Amount: ' + row[4] + '\n‣ Yield: ' + row[5] + '\n‣ Date: ' + row[6] + '\n\n'
                if len(tmp) + len(n) <= max_message_size:
                    tmp += n
                else:
                    message_array.append(tmp)
                    tmp = ''
        if not message_array:
            message_array.append(tmp)

        keyboard = [
            [InlineKeyboardButton("Back",
                                  callback_data=str(YES))],
            # [InlineKeyboardButton("Back to main menu",
            #                       callback_data=str(BACKTOMENU))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for message in message_array:
            query.edit_message_text(text=message, parse_mode='html', silent=True, reply_markup=reply_markup)
        return SHOWOPTIONS

    def ninety_days(self, update, context):
        query = update.callback_query
        query.answer()
        rows = self.__db.get_items('dividends', '*')
        tmp = ''
        period = datetime.now().date() + timedelta(days=90)
        max_message_size = 4096
        message_array = []
        for row in rows:
            if datetime.strptime(row[6], '%d %B %Y').date() < period:
                n = '<b>' + row[0].lstrip() + ' (' + row[1] + ')</b>\n‣ Market Cap: ' + row[2] \
                    + '\n‣ Price: ' + row[3] + \
                    '\n‣ Amount: ' + row[4] + '\n‣ Yield: ' + row[5] + '\n‣ Date: ' + row[6] + '\n\n'
                if len(tmp) + len(n) <= max_message_size:
                    tmp += n
                else:
                    message_array.append(tmp)
                    tmp = ''
        if not message_array:
            message_array.append(tmp)

        keyboard = [
            [InlineKeyboardButton("Back",
                                  callback_data=str(YES))],
            # [InlineKeyboardButton("Back to main menu",
            #                       callback_data=str(BACKTOMENU))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for message in message_array:
            query.edit_message_text(text=message, parse_mode='html', silent=True, reply_markup=reply_markup)
        return SHOWOPTIONS
