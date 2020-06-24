from telegram.ext import CommandHandler

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

import Controllers.states as states

from Utils.logging import get_logger as log


class MenuController:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__cancel_handler()
        self.__user_count = 0
        self.__menu_text = "<b>Kubera [v0.0.1]</b>\nKubera is a trading assistant that is designed to make your " \
                           "life easier. Only SGX securities are supported. \n\n<b>Features:</b>\n\n<b>Upcoming " \
                           "Dividends</b>\nDividend payouts that are coming ""soon.\n\n<b>Dividend Summary</b>" \
                           "\nDividends paid by a company over the last 5 years.\n\n<b>Dividend" \
                           "Calculator</b>\nCalculate your dividend payout.\n\n<b>Data" \
                           "sources</b>:\ndividends.sg\nYahoo Finance\n\n Use /cancel to exit the menu."
        self.__menu = None

    def __handler(self):
        menu_handler = CommandHandler("start", self.__show_menu)
        self.__dp.add_handler(menu_handler)

    def __show_menu(self, update, context):
        user = update.message.from_user
        log().info("User %s started the conversation.", user.first_name)

        keyboard = [
            [InlineKeyboardButton("🔸Upcoming Dividends",
                                  callback_data=str(states.DIVIDENDUP))],
            [InlineKeyboardButton("🔸Dividend Summary",
                                  callback_data=str(states.DIVIDENDINFO))],
            [InlineKeyboardButton("🔸Dividend Calculator",
                                  callback_data=str(states.DIVIDENDCALC))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        self.__menu = update.message.reply_text(self.__menu_text, reply_markup=reply_markup, parse_mode='HTML')

    def __cancel_handler(self):
        cancel_handler = CommandHandler("cancel", self.__end_chat)
        self.__dp.add_handler(cancel_handler)

    def __end_chat(self, update, context):
        user = update.message.from_user
        log().info("User %s ended the conversation.", user.first_name)
        self.__menu.edit_text('Chat ended. Use /start to show the menu again.')
