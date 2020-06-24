from telegram.ext import Updater

from Utils.logging import get_logger as log


class Bot:
    def __init__(self):
        log().info('Kubera v0.0.1 active')
        # loaded from config
        self.token = ''
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher
        # error handling
        self.dp.add_error_handler(self.error)
        # start bot
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def error(update, context):
        log().warning('Update "%s" caused error "%s"', update, context.error)
