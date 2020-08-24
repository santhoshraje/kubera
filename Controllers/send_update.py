import time

from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

from config import BotConfig
from db_engine import DBEngine

from telegram.error import TelegramError

from Utils.logging import get_logger as log

AUTH, MSG, CONFIRM, RESPONSE = range(4)


class SendUpdate:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__message = ''

    def __start(self, update, context):
        update.message.reply_text('Please enter admin password')
        return AUTH

    def __authenticated(self, update, context):
        update.message.reply_text('Please enter update message to send to users')
        return MSG

    def __store_message(self, update, context):
        self.__message = update.message.text
        return CONFIRM

    def __confirmation(self, update, context):
        update.message.reply_text('You entered: \n\n' + self.__message + '\n\nReady to send?')
        return RESPONSE

    def __yes(self, update, context):
        # send to users
        for user in DBEngine().get_items():
            try:
                context.bot.send_message(chat_id=user, text=self.__message, parse_mode='HTML')
                log().info('Message has been sent to %s', user)
                time.sleep(1)
            except TelegramError as e:
                log().warning(e)
                log().warning('User %s has blocked the bot', user)
                DBEngine().delete_item(user)
                log().info('User %s has been removed from the database', user)
                continue

        # send message
        update.message.reply_text('Update sent to all users')
        return ConversationHandler.END

    def __handler(self):
        password = BotConfig().admin_password

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('update', self.__start)],

            states={
                AUTH: [MessageHandler(Filters.regex('^'+password+'$'), self.__authenticated)],
                MSG: [MessageHandler(Filters.all, self.__store_message)],
                CONFIRM: [MessageHandler(Filters.all, self.__confirmation)],
                RESPONSE: [MessageHandler(Filters.regex('^yes$'), self.__yes),
                           MessageHandler(Filters.regex('^no$'), self.__authenticated)],

            },

            fallbacks=[]
        )
        self.__dp.add_handler(conv_handler)
