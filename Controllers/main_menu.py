from telegram.ext import CommandHandler

from telegram import InlineKeyboardButton, KeyboardButton
from telegram import ReplyKeyboardMarkup

import Controllers.global_states as states

# utilities
from Utils.logging import get_logger as log
from Utils.check_user import does_user_exist as check
# configuration
from config import BotConfig


class MainMenu:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__menu_text = ''

    # handlers
    def __handler(self):
        menu_handler = CommandHandler("start", self.__show_menu)
        self.__dp.add_handler(menu_handler)

    # functions
    def __show_menu(self, update, context):
        user = update.effective_user

        if check(str(user.id)):
            log().info("Existing user %s started the conversation.", user.first_name)
        else:
            log().info("New user %s started the conversation.", user.first_name)

        keyboard = [
            # [KeyboardButton("Show me upcoming dividend payouts", callback_data=str(states.DIVIDENDUP))],
            [KeyboardButton("Show me a summary of dividends paid")],
            [KeyboardButton("Calculate my expected dividends")],
            [KeyboardButton("Send feedback")],
            [KeyboardButton("Cancel")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        # Send message with text and appended InlineKeyboard
        update.message.reply_text("Hello " + user.first_name + ". I am Kubera, a robot trading assistant. I am "
                                                               "designed to help you be a better trader. You will "
                                                               "automatically receive trading tips as they become "
                                                               "available.\n\nHow can I help you today?", parse_mode='HTML', reply_markup = reply_markup)

        context.bot.send_message(chat_id=BotConfig().admin_id, text='hello world')
