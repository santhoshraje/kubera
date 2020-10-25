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
        menu_text = "Hello " + user.first_name + ". Let's make some money. How can I help you today? \n\nTap on any " \
                                                 "of the options below to learn more. Use /start to bring up this " \
                                                 "menu at any time. "

        keyboard = [
            [InlineKeyboardButton("Show me upcoming dividends",
                                  callback_data=str(states.DIVIDENDUP))],
            [InlineKeyboardButton("Show me past dividends",
                                  callback_data=str(states.DIVIDENDINFO))],
            [InlineKeyboardButton("Estimate my dividends for 2020",
                                  callback_data=str(states.DIVIDENDCALC))],
            [InlineKeyboardButton("️Send feedback",
                                  callback_data=str(states.FEEDBACK))],
            [InlineKeyboardButton("About this bot",
                                  callback_data=str(states.MENUCANCEL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='HTML')
