from telegram.ext import Updater

from Utils.logging import get_logger as log

from Controllers.menu_controller import MenuController
from Controllers.dc_controller import DCController
from Controllers.ds_controller import DSController
from Controllers.ud_controller import UDController
#jobs
from Kubera.tools import get_upcoming_dividends


class Bot:
    def __init__(self):
        log().info('Kubera v1.0 active')
        # loaded from config
        self.token = ''
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # job queue
        self.job_queue = self.updater.job_queue
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher
        # error handling
        self.dp.add_error_handler(self.error)
        # add controllers
        MenuController(self.dp)
        DCController(self.dp)
        DSController(self.dp)
        UDController(self.dp)
        # add jobs
        self.job_queue.run_repeating(get_upcoming_dividends, interval=1800, first=0)
        # start bot
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def error(update, context):
        log().warning('Update "%s" caused error "%s"', update, context.error)
