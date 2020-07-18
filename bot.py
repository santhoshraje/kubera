from telegram.ext import Updater

from Utils.logging import get_logger as log

from Controllers.main_menu import MainMenu
from Controllers.dividend_calculator import DividendCalculator
from Controllers.dividend_summary import DividendSummary
from Controllers.upcoming_dividends import UpcomingDividends
from Controllers.feedback_button import FeedbackButton
from Controllers.cancel_button import CancelButton
#jobs
from Jobs.get_upcoming_dividends import get_upcoming_dividends
#config
from config import BotConfig


class Bot:
    def __init__(self):
        self.config = BotConfig()
        log().info('kubera version ' + self.config.version + ' active')
        # loaded from config
        self.token = self.config.token
        # telegram api
        self.updater = Updater(self.token, use_context=True)
        # job queue
        self.job_queue = self.updater.job_queue
        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher
        # error handling
        self.dp.add_error_handler(self.error)
        # add controllers
        MainMenu(self.dp)
        DividendCalculator(self.dp)
        DividendSummary(self.dp)
        UpcomingDividends(self.dp)
        FeedbackButton(self.dp)
        CancelButton(self.dp)
        # add jobs
        self.job_queue.run_repeating(get_upcoming_dividends, interval=3600, first=0)
        # start bot
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def error(update, context):
        log().warning('"%s"', context.error)
