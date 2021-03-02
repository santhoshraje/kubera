from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler

import Controllers.global_states as states

from Utils.logging import get_logger as log


class CancelButton:
    def __init__(self, dispatcher):
        self.__dp = dispatcher
        self.__handler()

    def __handler(self):
        cancel_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(self.__end_chat, pattern='^' + str(states.MENUCANCEL) + '$')],
            states={},
            fallbacks=[]
        )
        self.__dp.add_handler(cancel_handler)

    @staticmethod
    def __end_chat(update, context):
        user = update.effective_user
        query = update.callback_query
        query.answer()
        log().info("User %s ended the conversation.", user.first_name)
        query.edit_message_text('Chat ended. Use /start to show the menu again.')
        return ConversationHandler.END

