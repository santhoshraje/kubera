from telegram.ext import ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler

import Controllers.global_states as states

from Utils.logging import get_logger as log


class CancelButton:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        cancel_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^Cancel$'), self.__end_chat)],
            states={},
            fallbacks=[]
        )
        self.__dp.add_handler(cancel_handler)

    @staticmethod
    def __end_chat(update, context):
        user = update.effective_user
        # query = update.callback_query
        # query.answer()
        log().info("User %s ended the conversation.", user.first_name)
        update.message.reply_text('Chat ended. Use /start to show the menu again.')
        return ConversationHandler.END

