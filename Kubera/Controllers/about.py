from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
import Controllers.global_states as states
from Bot.config import BotConfig


class About:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()
        self.__text = "<b>Kubera v" + BotConfig().version + "</b>\nKubera is a trading assistant that is designed to " \
                                                            "make your life easier.\n\n<b>Features:</b>\nWatchlist " \
                                                            "summary\nDaily updates after market close on how your " \
                                                            "watchlist " \
                                                            "performed\n\nDividend history\nDividends paid by a " \
                                                            "company over the last 5 years.\n\n<b>Supported " \
                                                            "Exchanges:</b>\nSGX\n\n<b>Data " \
                                                            "Sources</b>:\n<code>dividends.sg</code>\nYahoo " \
                                                            "Finance "

    def __handler(self):
        handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.__show_message, pattern='^' + str(states.ABOUT) + '$')],
            states={

            },
            fallbacks=[

            ]
        )
        self.__dp.add_handler(handler)

    def __show_message(self, update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(self.__text, parse_mode='HTML')
        return ConversationHandler.END
