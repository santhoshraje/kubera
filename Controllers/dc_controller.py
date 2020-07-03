from telegram.ext import ConversationHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

import Controllers.states as states

from Kubera.share import Share

from Utils.logging import get_logger as log


class DCController:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.stock_name = 0
        self.amount = 0

    def __handler(self):
        dc_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.show_options, pattern='^' + str(states.DIVIDENDCALC) + '$')],
            states={
                states.DIVIDENDCALCFIRST: [
                    CallbackQueryHandler(self.get_ticker_amt, pattern='^' + str(states.DIVIDENDCALCAMT) + '$'),
                    CallbackQueryHandler(self.get_ticker_shares, pattern='^' + str(states.DIVIDENDCALCSHARES) + '$')
                ],
                states.DIVIDENDCALCAMTSTATE: [
                    # message handler
                    MessageHandler(Filters.text, self.calculate_by_amt_first)
                ],
                states.DIVIDENDCALCSHARESSTATE: [
                    # message handler
                    MessageHandler(Filters.text, self.calculate_by_shares_first)
                ],
                states.DIVIDENDCALCAMTSTATEFINAL: [
                    # message handler
                    MessageHandler(Filters.text, self.calculate_by_amt_second)
                ],
                states.DIVIDENDCALCSHARESSTATEFINAL: [
                    # message handler
                    MessageHandler(Filters.text, self.calculate_by_shares_second)
                ],
            },
            fallbacks=[]
        )
        self.__dp.add_handler(dc_handler)

    @staticmethod
    def show_options(update, context):
        user = update.effective_user
        log().info("User %s pressed the dividend calculator button.", user.id)
        # answer query
        query = update.callback_query
        query.answer()
        # new keyboard
        keyboard = [
            [InlineKeyboardButton("🔵 Calculate by amount",
                                  callback_data=str(states.DIVIDENDCALCAMT))],
            [InlineKeyboardButton("⚪ Calculate by shares",
                                  callback_data=str(states.DIVIDENDCALCSHARES))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="You can calculate expected dividends by entering either the number of shares bought or the amount "
                 "paid for the shares",
            reply_markup=reply_markup
        )
        return states.DIVIDENDCALCFIRST

    def calculate_by_amt_first(self, update, context):
        self.stock_name = update.message.text
        user = update.effective_user
        log().info("User %s entered ticker value %s", user.id, self.stock_name)
        try:
            share = Share(self.stock_name)
        except AttributeError:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            return ConversationHandler.END
        update.message.reply_text("Enter purchase amount in SGD")
        return states.DIVIDENDCALCAMTSTATEFINAL

    def calculate_by_shares_first(self, update, context):
        self.stock_name = update.message.text
        user = update.effective_user
        log().info("User %s entered ticker value %s", user.id, self.stock_name)
        try:
            share = Share(self.stock_name)
        except AttributeError:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            return ConversationHandler.END
        update.message.reply_text("Enter number of shares")
        return states.DIVIDENDCALCSHARESSTATEFINAL

    def calculate_by_amt_second(self, update, context):
        self.amount = update.message.text
        user = update.effective_user
        log().info("User %s entered amount %s", user.id, self.amount)
        share = Share(self.stock_name)
        tmp = int(int(self.amount) / float(share.price) / 100)
        no_of_shares = tmp * 100
        dividends = share.get_total_dividend_payout(2019, 2) * no_of_shares
        update.message.reply_text("Expected dividends based on last year's data: SGD " + str(
            dividends) + "\n\n Use /start to go back to main menu")
        return ConversationHandler.END

    def calculate_by_shares_second(self, update, context):
        self.amount = update.message.text
        user = update.effective_user
        log().info("User %s entered amount %s", user.id, self.amount)
        share = Share(self.stock_name)
        dividends = share.get_total_dividend_payout(2019, 2) * int(self.amount)
        update.message.reply_text("Expected dividends based on last year's data: SGD " + str(
            dividends) + "\n\n Use /start to go back to main menu")
        return ConversationHandler.END

    @staticmethod
    def get_ticker_amt(update, context):
        user = update.effective_user
        log().info("User %s wants to calculate using amount.", user.id)
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Enter ticker symbol (e.g D05)")
        return states.DIVIDENDCALCAMTSTATE

    @staticmethod
    def get_ticker_shares(update, context):
        user = update.effective_user
        log().info("User %s wants to calculate using shares.", user.id)
        query = update.callback_query
        query.answer()
        query.edit_message_text(
            text="Enter ticker symbol (e.g D05)")
        return states.DIVIDENDCALCSHARESSTATE
