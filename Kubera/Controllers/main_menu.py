from telegram.ext import CommandHandler

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

import Controllers.global_states as states
# utilities
from Model.share import Share
from Utils.logging import get_logger as log
# configuration
from Bot.config import BotConfig
from Model.db import DBEngine


class MainMenu:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__menu_text = "What would you like to do today?\n\n<b>Your watchlist:\n<\b>"

    # handlers
    def __handler(self):
        menu_handler = CommandHandler("start", self.__show_menu)
        self.__dp.add_handler(menu_handler)

    # functions
    def __show_menu(self, update, context):
        tickers = {}
        first_name = update.effective_user.first_name
        user_id = update.effective_user.id
        s = "Hi " + first_name + ", what would you like to do?\n\n<b>Your watchlist:</b>\n"
        result = DBEngine().custom_command("SELECT ticker FROM watchlist WHERE id=" + str(user_id))
        for result in result:
            my_share = Share(result[0])
            tickers[my_share.ticker] = my_share.name

        for key, value in tickers.items():
            s += value + " (" + key + ")" + "\n"

        if len(tickers) == 0:
            s += "Empty! Update your watchlist to receive automatic alerts about your favourite stocks."

        keyboard = [
            [InlineKeyboardButton("Update my watchlist",
                                  callback_data=str(states.UPDATEWATCHLIST))],
            [InlineKeyboardButton("View dividend history",
                                  callback_data=str(states.DIVIDENDINFO))],
            # [InlineKeyboardButton("Bot settings",
            #                       callback_data=str(states.SETTINGS))],
            [InlineKeyboardButton("About this bot",
                                  callback_data=str(states.ABOUT))]
            # [InlineKeyboardButton("Cancel",
            #                       callback_data=str(states.MENUCANCEL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text(s, reply_markup=reply_markup, parse_mode='HTML')
        # context.bot.send_message(chat_id=, text='hello world')
