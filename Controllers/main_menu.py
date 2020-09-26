from telegram.ext import CommandHandler

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

import Controllers.global_states as states
# utilities
from Utils.logging import get_logger as log
# configuration
from config import BotConfig
from db_engine import DBEngine


class MainMenu:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__menu_text = "<b>Kubera [v" + BotConfig().version + "]</b>\nKubera is a stock trading assistant that is " \
                                                                  "designed to help you make money.\n\n<b>Supported " \
                                                                  "Exchanges</b>:\nSGX \n\n<b>Bot " \
                                                                  "Features:</b>\nUpcoming Dividends\nDividend " \
                                                                  "payouts that are coming soon.\n\nDividend " \
                                                                  "Summary\nDividends paid by a company over the last " \
                                                                  "5 years.\n\nMarket Statistics Report\nMarket " \
                                                                  "statistics for the day delivered daily " \
                                                                  "after market close.\n\n<b>Data " \
                                                                  "Sources</b>:\n<code>dividends.sg</code>\nYahoo " \
                                                                  "Finance "

    # handlers
    def __handler(self):
        menu_handler = CommandHandler("start", self.__show_menu)
        self.__dp.add_handler(menu_handler)

    # functions
    def __show_menu(self, update, context):
        user = update.effective_user
        log().info("User %s [id: %s] started the conversation.", user.first_name, user.id)
        # add new user
        DBEngine().add_item('users', 'id', user.id)
        DBEngine().update_item('users', 'first', user.first_name, 'id', user.id)
        DBEngine().update_item('users', 'last', user.last_name, 'id', user.id)
        DBEngine().update_item('users', 'username', user.username, 'id', user.id)

        keyboard = [
            [InlineKeyboardButton("🔸Upcoming Dividends",
                                  callback_data=str(states.DIVIDENDUP))],
            [InlineKeyboardButton("🔸Dividend Summary",
                                  callback_data=str(states.DIVIDENDINFO))],
            # [InlineKeyboardButton("🔸Dividend Calculator",
            #                       callback_data=str(states.DIVIDENDCALC))],
            [InlineKeyboardButton("❗️Send Feedback",
                                  callback_data=str(states.FEEDBACK))],
            [InlineKeyboardButton("❌Cancel",
                                  callback_data=str(states.MENUCANCEL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(self.__menu_text, reply_markup=reply_markup, parse_mode='HTML')
        # context.bot.send_message(chat_id=, text='hello world')
