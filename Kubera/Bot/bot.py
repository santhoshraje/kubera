# telegram api
from telegram.ext import Updater
# utils
from Utils.logging import get_logger as log
# controllers
from Controllers.main_menu import MainMenu
from Controllers.about import About
from Controllers.update_watchlist_button import UpdateWatchlist
from Controllers.dividend_summary import DividendSummary
# jobs
from Jobs.post_market_data import post_market_data
from Jobs.dividend_check import check_dividend
# config
from Bot.config import BotConfig
# db
from Model.db import DBEngine
# tools
import datetime


class Bot:
    def __init__(self):
        self.config = BotConfig(dev=True)
        log().info('🟢 KUBERA version ' + self.config.version + ' started')
        # db engine
        DBEngine()
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
        # controllers
        MainMenu(self.dp)
        UpdateWatchlist(self.dp)
        # DividendSummary(self.dp)
        About(self.dp)
        # jobs
        # 5:15 PM singapore time
        # self.job_queue.run_daily(post_market_data, datetime.time(hour=9, minute=15), (0, 1, 2, 3, 4))
        # 9:00 AM singapore time
        self.job_queue.run_daily(check_dividend, datetime.time(hour=1, minute=15), (0, 1, 2, 3, 4))
        # self.job_queue.run_once(check_dividend, 0)

        # start bot
        self.updater.start_polling()
        self.updater.idle()

    @staticmethod
    def error(update, context):
        log().warning('"%s"', context.error)
