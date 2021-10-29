from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
import Controllers.global_states as states
from Model.db import DBEngine
from Model.share import Share


ADD, REMOVE, SELECTOPTION, ADDSHARE, REMOVESHARE, SELECTSHARE = range(6)


class UpdateWatchlist:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.__show_options, pattern='^' + str(states.UPDATEWATCHLIST) + '$')],
            states={
                SELECTOPTION: [
                    CallbackQueryHandler(self.__add_share, pattern='^' + str(ADD) + '$'),
                    CallbackQueryHandler(self.__remove_share, pattern='^' + str(REMOVE) + '$')
                ],
                ADDSHARE: [
                    # message handler
                    MessageHandler(Filters.text, self.__add_share_final)
                ],
                REMOVESHARE: [
                    # message handler
                    CallbackQueryHandler(self.__remove_share_final),
                ],
            },
            fallbacks=[

            ]
        )
        self.__dp.add_handler(handler)

    def __show_options(self, update, context):
        query = update.callback_query
        query.answer()
        keyboard = [
            [InlineKeyboardButton("Add",
                                  callback_data=str(ADD))],
            [InlineKeyboardButton("Remove",
                                  callback_data=str(REMOVE))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Would you like to add or remove shares from your watchlist?",
            reply_markup=reply_markup
        )
        return SELECTOPTION

    def __add_share(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Enter ticker symbol (e.g D05)")
        return ADDSHARE

    def __add_share_final(self, update, context):
        tickers = {}
        user = update.effective_user
        # print(user.id)
        ticker = update.message.text
        share = Share(ticker)
        count = DBEngine().count("SELECT COUNT (*) FROM watchlist WHERE id=" + str(user.id))
        result = DBEngine().custom_command("SELECT ticker FROM watchlist WHERE id=" + str(user.id))
        # check for valid ticker
        if not share.is_valid:
            update.message.reply_text("Invalid ticker. Please use /start to go back to the main menu")
            return ConversationHandler.END
        # check if the user has hit watchlist limit
        if count >= 3:
            update.message.reply_text("You have reached your watchlist limit")
            return ConversationHandler.END
        # create dictionary of existing watchlist
        for result in result:
            my_share = Share(result[0])
            tickers[my_share.ticker] = my_share.name
        # add the incoming entry
        before = len(tickers)
        tickers[share.ticker] = share.name
        after = len(tickers)
        if before == after:
            update.message.reply_text("This stock is already on your watchlist")
            return ConversationHandler.END

        DBEngine().add_item('watchlist', ['id', 'ticker'], [user.id, share.ticker])

        s = ""
        for key, value in tickers.items():
            s += value + " (" + key + ")" + "\n"

        update.message.reply_text("Your watchlist has been updated.\n\n<b>Current watchlist:</b>\n" + s,
                                  parse_mode='HTML')
        return ConversationHandler.END

    def __remove_share(self, update, context):
        query = update.callback_query
        query.answer()
        keyboard = []
        user = update.effective_user
        result = DBEngine().custom_command("SELECT ticker FROM watchlist WHERE id=" + str(user.id))
        for result in result:
            my_share = Share(result[0])
            keyboard.append([InlineKeyboardButton(my_share.name + " (" + my_share.ticker + ")",
                                                  callback_data=my_share.ticker)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.edit_text("What would you like to remove?", reply_markup=reply_markup,
                                                parse_mode='HTML')
        return REMOVESHARE

    def __remove_share_final(self, update, context):
        tickers = {}
        user = update.effective_user
        query = update.callback_query
        query.answer()
        # print(query.data)
        DBEngine().delete_item('watchlist', 'ticker', query.data)
        result = DBEngine().custom_command("SELECT ticker FROM watchlist WHERE id=" + str(user.id))
        for result in result:
            my_share = Share(result[0])
            tickers[my_share.ticker] = my_share.name
        s = ""
        for key, value in tickers.items():
            s += value + " (" + key + ")" + "\n"
        update.callback_query.message.edit_text("Your watchlist has been updated.\n\n<b>Current watchlist:</b>\n" + s,
                                                parse_mode='HTML')
        return ConversationHandler.END
